#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
import tempfile
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.parse import quote

import bibtexparser
import requests
from bibtexparser.customization import author as bibtex_author
from bibtexparser.customization import convert_to_unicode
from doi2bib3 import fetch_bibtex
from doi2bib3.backend import DOIError
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PUBLICATIONS_PATH = REPO_ROOT / "src" / "data" / "publications.yml"

FIELD_ORDER = [
    "type",
    "year",
    "authors",
    "title",
    "refId",
    "doi",
    "note",
    "href",
    "journal",
    "booktitle",
    "series",
    "publisher",
    "volume",
    "number",
    "issue",
    "pages",
    "eventDate",
    "articleno",
    "numpages",
    "address",
    "location",
    "lang",
]

COMPARISON_KEYS = {
    "year",
    "title",
    "authors",
    "doi",
    "journal",
    "booktitle",
    "volume",
    "number",
    "issue",
    "pages",
    "eventDate",
    "publisher",
    "series",
    "address",
    "location",
    "numpages",
    "articleno",
}

TYPE_MAP = {
    "article": "article",
    "book-chapter": "inproceedings",
    "conference": "inproceedings",
    "conference-paper": "inproceedings",
    "inbook": "inproceedings",
    "incollection": "inproceedings",
    "inproceedings": "inproceedings",
    "journal-article": "article",
    "proceedings-article": "inproceedings",
    "proceedings": "inproceedings",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fill missing fields in src/data/publications.yml from DOI metadata. "
            "Entries with conflicting existing data are reported and skipped unless "
            "--force is used. If a positional DOI is provided and it does not exist in "
            "the YAML yet, a new entry is inserted at the top."
        )
    )
    parser.add_argument(
        "doi",
        nargs="?",
        help="If provided, only process the matching DOI entry, or insert a new one at the top if absent.",
    )
    parser.add_argument(
        "--yaml",
        dest="yaml_path",
        type=Path,
        default=DEFAULT_PUBLICATIONS_PATH,
        help=f"Path to publications YAML (default: {DEFAULT_PUBLICATIONS_PATH})",
    )
    parser.add_argument(
        "--start-line",
        type=int,
        default=1,
        help="Only process entries whose starting YAML line is at or after this value.",
    )
    parser.add_argument(
        "--end-line",
        type=int,
        help="Only process entries whose starting YAML line is at or before this value.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Warn on conflicts and overwrite conflicting existing fields.",
    )
    parser.add_argument(
        "--backend",
        choices=("doi2bib3", "crossref"),
        default="doi2bib3",
        help="Metadata backend to use when resolving DOI data.",
    )
    parser.add_argument(
        "--crossref",
        action="store_true",
        help="Shortcut for --backend crossref.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="Timeout passed to doi2bib3.fetch_bibtex().",
    )
    args = parser.parse_args()
    if args.crossref:
        args.backend = "crossref"
    return args


def build_yaml() -> YAML:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 10000
    return yaml


def normalize_doi(value: Any) -> str:
    text = normalize_whitespace(value).lower()
    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "https://dx.doi.org/",
        "http://dx.doi.org/",
        "doi:",
    ):
        if text.startswith(prefix):
            text = text[len(prefix) :]
            break
    return text.strip()


def normalize_whitespace(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\u00a0", " ").split())


def normalize_text_for_compare(value: Any) -> str:
    text = normalize_whitespace(value)
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "{": "",
        "}": "",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return normalize_whitespace(text).casefold()


def normalize_pages(value: Any) -> str:
    text = normalize_whitespace(value)
    text = text.replace("---", "–").replace("--", "–").replace("-", "–")
    return normalize_whitespace(text)


def normalize_url(value: Any) -> str:
    text = normalize_whitespace(value)
    if not text:
        return ""
    text = text.replace("http://dx.doi.org/", "https://doi.org/")
    text = text.replace("http://doi.org/", "https://doi.org/")
    return text


def strip_author_marker(value: Any) -> str:
    text = normalize_whitespace(value)
    while text.endswith("*"):
        text = text[:-1].rstrip()
    return text


def format_bib_author(name: str) -> str:
    cleaned = normalize_whitespace(name)
    if "," not in cleaned:
        return cleaned
    last, first = [part.strip() for part in cleaned.split(",", 1)]
    return normalize_whitespace(f"{first} {last}")


def normalize_author_for_compare(value: Any) -> str:
    text = strip_author_marker(value)
    replacements = {
        ".": "",
        "\u2018": "'",
        "\u2019": "'",
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return normalize_whitespace(text).casefold()


def normalize_value_for_compare(key: str, value: Any) -> Any:
    if key == "authors":
        if isinstance(value, list):
            return [normalize_author_for_compare(item) for item in value]
        return [normalize_author_for_compare(value)]
    if key == "doi":
        return normalize_doi(value)
    if key == "pages":
        return normalize_text_for_compare(normalize_pages(value))
    if key == "year":
        text = normalize_whitespace(value)
        return int(text) if text.isdigit() else normalize_text_for_compare(text)
    return normalize_text_for_compare(value)


def values_match(key: str, existing: Any, fetched: Any) -> bool:
    return normalize_value_for_compare(key, existing) == normalize_value_for_compare(
        key, fetched
    )


def parse_bibtex_entry(bibtex: str) -> dict[str, Any]:
    database = bibtexparser.loads(bibtex)
    if not database.entries:
        raise ValueError("BibTeX could not be parsed into an entry.")

    raw_entry = dict(database.entries[0])
    entry = convert_to_unicode(dict(raw_entry))
    author_data = bibtex_author({"author": entry.get("author", "")})
    authors = [
        format_bib_author(name)
        for name in author_data.get("author", [])
        if normalize_whitespace(name)
    ]

    parsed: dict[str, Any] = {}
    mapped_type = TYPE_MAP.get(normalize_whitespace(entry.get("ENTRYTYPE")).lower())
    if mapped_type:
        parsed["type"] = mapped_type

    if entry.get("year"):
        year_text = normalize_whitespace(entry["year"])
        parsed["year"] = int(year_text) if year_text.isdigit() else year_text

    if authors:
        parsed["authors"] = authors

    for source_key, target_key in (
        ("title", "title"),
        ("journal", "journal"),
        ("booktitle", "booktitle"),
        ("volume", "volume"),
        ("number", "number"),
        ("issue", "issue"),
        ("publisher", "publisher"),
        ("series", "series"),
        ("address", "address"),
        ("location", "location"),
        ("numpages", "numpages"),
        ("articleno", "articleno"),
    ):
        value = normalize_whitespace(entry.get(source_key))
        if value:
            parsed[target_key] = value

    pages = normalize_whitespace(entry.get("pages"))
    if pages:
        parsed["pages"] = normalize_pages(pages)

    href = normalize_url(entry.get("url"))
    if href:
        parsed["href"] = href

    doi = normalize_doi(entry.get("doi"))
    if doi:
        parsed["doi"] = doi

    return parsed


def pick_first_text(values: Any) -> str:
    if isinstance(values, list):
        for value in values:
            text = normalize_whitespace(value)
            if text:
                return text
        return ""
    return normalize_whitespace(values)


def join_nonempty(parts: list[str], separator: str) -> str:
    return separator.join(part for part in parts if normalize_whitespace(part))


def format_crossref_author(author: dict[str, Any]) -> str:
    given = normalize_whitespace(author.get("given"))
    family = normalize_whitespace(author.get("family"))
    name = join_nonempty([given, family], " ")
    if name:
        return name
    return normalize_whitespace(author.get("name"))


def first_crossref_year(message: dict[str, Any]) -> int | str | None:
    for key in (
        "issued",
        "published-print",
        "published-online",
        "published",
        "created",
    ):
        date_parts = message.get(key, {}).get("date-parts")
        if not date_parts or not date_parts[0]:
            continue
        year = date_parts[0][0]
        if isinstance(year, int):
            return year
        text = normalize_whitespace(year)
        if text:
            return int(text) if text.isdigit() else text
    return None


def crossref_assertions(message: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for assertion in message.get("assertion", []):
        name = normalize_whitespace(assertion.get("name"))
        value = normalize_whitespace(assertion.get("value"))
        if name and value:
            result[name] = value
    return result


def parse_crossref_event_date(assertions: dict[str, str]) -> str:
    start = assertions.get("conference_start_date", "")
    end = assertions.get("conference_end_date", "")
    if start and end:
        return f"{start} - {end}"
    return start or end


def parse_crossref_location(
    message: dict[str, Any], assertions: dict[str, str]
) -> tuple[str, str]:
    event = message.get("event", {})
    event_location = normalize_whitespace(event.get("location"))
    if event_location:
        location = event_location
    else:
        location = join_nonempty(
            [
                assertions.get("conference_city", ""),
                assertions.get("conference_country", ""),
            ],
            ", ",
        )

    address = normalize_whitespace(message.get("publisher-location"))
    return address, location


def parse_crossref_booktitle(message: dict[str, Any], assertions: dict[str, str]) -> str:
    conference_name = assertions.get("conference_name", "")
    conference_acronym = assertions.get("conference_acronym", "")
    if conference_name:
        normalized_name = normalize_text_for_compare(conference_name)
        normalized_acronym = normalize_text_for_compare(conference_acronym)
        if conference_acronym and normalized_acronym not in normalized_name:
            return f"{conference_name} ({conference_acronym})"
        return conference_name

    container_titles = [
        normalize_whitespace(value)
        for value in message.get("container-title", [])
        if normalize_whitespace(value)
    ]
    if container_titles:
        container_title = container_titles[-1] if len(container_titles) > 1 else container_titles[0]
        container_title = container_title.removeprefix("Proceedings of the ")
        container_title = container_title.removeprefix("Proceedings of ")
        normalized_title = normalize_text_for_compare(container_title)
        normalized_acronym = normalize_text_for_compare(conference_acronym)
        if conference_acronym and normalized_acronym not in normalized_title:
            return f"{container_title} ({conference_acronym})"
        return container_title

    event_name = normalize_whitespace(message.get("event", {}).get("name"))
    if event_name:
        return event_name

    return ""


def parse_crossref_series(
    message: dict[str, Any], assertions: dict[str, str], booktitle: str
) -> str:
    event_acronym = normalize_whitespace(message.get("event", {}).get("acronym"))
    if event_acronym:
        return event_acronym

    conference_acronym = assertions.get("conference_acronym", "")
    if conference_acronym:
        return conference_acronym

    container_titles = [
        normalize_whitespace(value)
        for value in message.get("container-title", [])
        if normalize_whitespace(value)
    ]
    for title in container_titles:
        if not values_match("booktitle", title, booktitle):
            return title
    return ""


def parse_crossref_message(message: dict[str, Any]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    mapped_type = TYPE_MAP.get(normalize_whitespace(message.get("type")).lower())
    if mapped_type:
        parsed["type"] = mapped_type

    year = first_crossref_year(message)
    if year is not None:
        parsed["year"] = year

    authors = []
    for author in message.get("author", []):
        formatted_author = format_crossref_author(author)
        if formatted_author:
            authors.append(formatted_author)
    if authors:
        parsed["authors"] = authors

    title = pick_first_text(message.get("title"))
    if title:
        parsed["title"] = title

    doi = normalize_doi(message.get("DOI"))
    if doi:
        parsed["doi"] = doi

    href = normalize_url(
        message.get("URL")
        or message.get("resource", {}).get("primary", {}).get("URL")
    )
    if href:
        parsed["href"] = href

    for source_key, target_key in (
        ("publisher", "publisher"),
        ("volume", "volume"),
        ("issue", "number"),
        ("article-number", "articleno"),
    ):
        value = normalize_whitespace(message.get(source_key))
        if value:
            parsed[target_key] = value

    pages = normalize_whitespace(message.get("page"))
    if pages:
        parsed["pages"] = normalize_pages(pages)

    assertions = crossref_assertions(message)
    address, location = parse_crossref_location(message, assertions)
    if address:
        parsed["address"] = address
    if location:
        parsed["location"] = location

    event_date = parse_crossref_event_date(assertions)
    if event_date:
        parsed["eventDate"] = event_date

    if parsed.get("type") == "article":
        journal = pick_first_text(message.get("container-title"))
        if journal:
            parsed["journal"] = journal
    else:
        booktitle = parse_crossref_booktitle(message, assertions)
        if booktitle:
            parsed["booktitle"] = booktitle
        series = parse_crossref_series(message, assertions, booktitle)
        if series:
            parsed["series"] = series

    return parsed


def fetch_crossref_message(doi: str, timeout: int) -> dict[str, Any]:
    response = requests.get(
        f"https://api.crossref.org/works/{quote(doi, safe='')}",
        headers={"Accept": "application/json", "User-Agent": "doi2pub/1.0"},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    message = payload.get("message")
    if not isinstance(message, dict):
        raise ValueError("Crossref response did not contain a work message.")
    return message


def fetch_metadata(doi: str, backend: str, timeout: int) -> dict[str, Any]:
    if backend == "crossref":
        return parse_crossref_message(fetch_crossref_message(doi, timeout))

    bibtex = fetch_bibtex(doi, timeout=timeout)
    return parse_bibtex_entry(bibtex)


def detect_conflicts(
    entry: CommentedMap, fetched_fields: dict[str, Any]
) -> list[tuple[str, Any, Any]]:
    conflicts: list[tuple[str, Any, Any]] = []
    for key in COMPARISON_KEYS:
        if key not in entry or key not in fetched_fields:
            continue
        if not values_match(key, entry[key], fetched_fields[key]):
            conflicts.append((key, entry[key], fetched_fields[key]))
    return conflicts


def load_publications(yaml_path: Path) -> tuple[YAML, CommentedSeq]:
    yaml = build_yaml()
    with yaml_path.open("r", encoding="utf-8") as handle:
        data = yaml.load(handle)

    if not isinstance(data, CommentedSeq):
        raise TypeError(f"{yaml_path} does not contain a top-level YAML sequence.")

    return yaml, data


def build_snippet_yaml() -> YAML:
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 10000
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml


def build_ordered_entry(fields: dict[str, Any]) -> CommentedMap:
    ordered = CommentedMap()
    for key in FIELD_ORDER:
        if key in fields:
            ordered[key] = fields[key]
    for key, value in fields.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def render_field_block(key: str, value: Any) -> list[str]:
    snippet_yaml = build_snippet_yaml()
    snippet = CommentedMap([(key, value)])
    buffer = StringIO()
    snippet_yaml.dump(snippet, buffer)
    return [f"  {line}" for line in buffer.getvalue().splitlines()]


def render_entry_block(fields: dict[str, Any]) -> list[str]:
    snippet_yaml = build_snippet_yaml()
    snippet = build_ordered_entry(fields)
    buffer = StringIO()
    snippet_yaml.dump(snippet, buffer)
    lines = buffer.getvalue().splitlines()
    if not lines:
        return []
    return [f"- {lines[0]}", *[f"  {line}" for line in lines[1:]]]


def validate_new_entry_fields(fetched_fields: dict[str, Any]) -> None:
    missing_keys = [
        key
        for key in ("type", "year", "authors", "title")
        if key not in fetched_fields or not fetched_fields[key]
    ]
    if missing_keys:
        joined_keys = ", ".join(missing_keys)
        raise ValueError(f"metadata for new entry is missing required fields: {joined_keys}")


def find_entry_end_insert_index(
    original_lines: list[str], entry_start_line: int, next_entry_start_line: int
) -> int:
    insert_index = next_entry_start_line - 1
    while insert_index > entry_start_line - 1 and not original_lines[insert_index - 1].strip():
        insert_index -= 1
    return insert_index


def find_insert_index(
    entry: CommentedMap,
    original_lines: list[str],
    next_entry_start_line: int,
    key: str,
) -> int:
    if key in FIELD_ORDER:
        key_order = FIELD_ORDER.index(key)
        for later_key in FIELD_ORDER[key_order + 1 :]:
            if later_key in entry:
                return entry.lc.key(later_key)[0]

    return find_entry_end_insert_index(original_lines, entry.lc.line + 1, next_entry_start_line)


def find_replace_end_index(
    entry: CommentedMap,
    original_lines: list[str],
    next_entry_start_line: int,
    key: str,
) -> int:
    key_start = entry.lc.key(key)[0]
    later_key_starts = sorted(
        entry.lc.key(existing_key)[0]
        for existing_key in entry
        if existing_key != key and entry.lc.key(existing_key)[0] > key_start
    )
    if later_key_starts:
        return later_key_starts[0]
    return find_entry_end_insert_index(original_lines, entry.lc.line + 1, next_entry_start_line)


def find_top_entry_insert_index(
    publications: CommentedSeq, original_lines: list[str]
) -> int:
    for entry in publications:
        if isinstance(entry, CommentedMap):
            return entry.lc.line
    return len(original_lines)


def write_updated_text(
    yaml_path: Path,
    original_lines: list[str],
    operations: list[tuple[int, int, int, list[str]]],
) -> None:
    updated_lines = list(original_lines)
    for start_index, end_index, field_order, block_lines in sorted(
        operations,
        key=lambda item: (item[0], item[1], item[2]),
        reverse=True,
    ):
        updated_lines[start_index:end_index] = block_lines

    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=yaml_path.parent, delete=False
    ) as handle:
        handle.write("\n".join(updated_lines))
        handle.write("\n")
        temp_path = Path(handle.name)

    temp_path.replace(yaml_path)


def main() -> int:
    args = parse_args()
    if args.start_line < 1:
        raise ValueError("--start-line must be 1 or greater.")
    if args.end_line is not None and args.end_line < 1:
        raise ValueError("--end-line must be 1 or greater.")
    if args.end_line is not None and args.end_line < args.start_line:
        raise ValueError("--end-line must be greater than or equal to --start-line.")

    yaml_path = args.yaml_path.resolve()
    doi_filter = normalize_doi(args.doi) if args.doi else ""
    original_lines = yaml_path.read_text(encoding="utf-8").splitlines()
    _, publications = load_publications(yaml_path)

    stats = {
        "seen": 0,
        "eligible": 0,
        "updated": 0,
        "prepended": 0,
        "unchanged": 0,
        "conflicts": 0,
        "errors": 0,
    }
    changed = False
    operations: list[tuple[int, int, int, list[str]]] = []
    top_entry_insert_index = find_top_entry_insert_index(publications, original_lines)
    doi_exists_anywhere = bool(
        doi_filter
        and any(
            isinstance(entry, CommentedMap)
            and normalize_doi(entry.get("doi")) == doi_filter
            for entry in publications
        )
    )
    entry_start_lines = [
        entry.lc.line + 1 for entry in publications if isinstance(entry, CommentedMap)
    ]
    entry_start_lines.append(len(original_lines) + 1)

    entry_index = 0
    for entry in publications:
        if not isinstance(entry, CommentedMap):
            continue

        stats["seen"] += 1
        entry_line = entry.lc.line + 1
        next_entry_start_line = entry_start_lines[entry_index + 1]
        entry_index += 1
        doi = normalize_doi(entry.get("doi"))

        if not doi:
            continue
        if entry_line < args.start_line:
            continue
        if args.end_line is not None and entry_line > args.end_line:
            continue
        if doi_filter and doi != doi_filter:
            continue

        stats["eligible"] += 1

        try:
            fetched_fields = fetch_metadata(doi, args.backend, args.timeout)
            if "doi" not in fetched_fields:
                fetched_fields["doi"] = doi
        except (DOIError, ValueError, TypeError, requests.RequestException) as exc:
            print(
                (
                    f"[ERROR] line {entry_line} doi={doi}: failed to fetch/parse metadata "
                    f"with backend={args.backend}: {exc}"
                ),
                file=sys.stderr,
            )
            stats["errors"] += 1
            continue

        conflicts = detect_conflicts(entry, fetched_fields)
        if conflicts:
            stats["conflicts"] += 1
            for key, existing, fetched in conflicts:
                print(
                    (
                        f"[CONFLICT] line {entry_line} doi={doi}: key={key}\n"
                        f"\texisting={existing!r}\n"
                        f"\tfetched={fetched!r}"
                    ),
                    file=sys.stderr,
                )
            if not args.force:
                print(
                    f"[SKIP] line {entry_line} doi={doi}: entry was skipped due to conflicts.",
                    file=sys.stderr,
                )
                continue
            conflict_keys = ", ".join(key for key, _, _ in conflicts)
            print(
                (
                    f"[WARN] line {entry_line} doi={doi}: overwriting conflicting fields "
                    f"due to --force ({conflict_keys})."
                ),
                file=sys.stderr,
            )

        conflict_map = {key: fetched for key, _, fetched in conflicts}
        filled_keys: list[str] = []
        overwritten_keys: list[str] = []
        for key, value in fetched_fields.items():
            field_order = FIELD_ORDER.index(key) if key in FIELD_ORDER else len(FIELD_ORDER)
            if key in conflict_map:
                start_index = entry.lc.key(key)[0]
                end_index = find_replace_end_index(
                    entry, original_lines, next_entry_start_line, key
                )
                block_lines = render_field_block(key, value)
                operations.append((start_index, end_index, field_order, block_lines))
                overwritten_keys.append(key)
                continue
            if key in entry:
                continue
            insert_index = find_insert_index(entry, original_lines, next_entry_start_line, key)
            block_lines = render_field_block(key, value)
            operations.append((insert_index, insert_index, field_order, block_lines))
            filled_keys.append(key)

        if filled_keys or overwritten_keys:
            changed = True
            stats["updated"] += 1
            detail_parts: list[str] = []
            if filled_keys:
                detail_parts.append(f"filled {', '.join(filled_keys)}")
            if overwritten_keys:
                detail_parts.append(f"overwrote {', '.join(overwritten_keys)}")
            print(f"[UPDATE] line {entry_line} doi={doi}: {'; '.join(detail_parts)}.", file=sys.stderr)
        else:
            stats["unchanged"] += 1

    if doi_filter and not doi_exists_anywhere:
        stats["eligible"] += 1
        try:
            fetched_fields = fetch_metadata(doi_filter, args.backend, args.timeout)
            if "doi" not in fetched_fields:
                fetched_fields["doi"] = doi_filter
            validate_new_entry_fields(fetched_fields)
        except (DOIError, ValueError, TypeError, requests.RequestException) as exc:
            print(
                (
                    f"[ERROR] doi={doi_filter}: failed to insert a new entry with "
                    f"backend={args.backend}: {exc}"
                ),
                file=sys.stderr,
            )
            stats["errors"] += 1
        else:
            block_lines = render_entry_block(fetched_fields)
            if (
                original_lines
                and top_entry_insert_index < len(original_lines)
                and original_lines[top_entry_insert_index].strip()
            ):
                block_lines = [*block_lines, ""]
            operations.append((top_entry_insert_index, top_entry_insert_index, -1, block_lines))
            changed = True
            stats["updated"] += 1
            stats["prepended"] += 1
            print(
                (
                    f"[PREPEND] doi={doi_filter}: inserted a new entry at the top "
                    f"using backend={args.backend}."
                ),
                file=sys.stderr,
            )

    if changed:
        write_updated_text(yaml_path, original_lines, operations)

    print(
        (
            f"Processed {stats['eligible']} DOI entries "
            f"(updated={stats['updated']}, prepended={stats['prepended']}, "
            f"unchanged={stats['unchanged']}, "
            f"conflicts={stats['conflicts']}, errors={stats['errors']})."
        ),
        file=sys.stderr,
    )

    if doi_filter and doi_exists_anywhere and stats["eligible"] == 0:
        print(
            (
                f"[WARN] No DOI entry matched {doi_filter!r} within the requested line range "
                f"({args.start_line}..{args.end_line if args.end_line is not None else 'end'})."
            ),
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
