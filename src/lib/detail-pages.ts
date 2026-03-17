import {
	englishStaticPageEntries,
	japaneseStaticPageEntries,
} from '../data/page-registry';

export interface LocalizedContentSlugEntry {
	slug: string;
	hasDefaultContent: boolean;
	hasEnglishContent: boolean;
}

const DEFAULT_SUFFIXES = ['.md', '.html'] as const;
const ENGLISH_SUFFIXES = ['.en.md', '.en.html'] as const;

function getFileName(path: string): string {
	return path.split('/').pop() ?? path;
}

function stripSuffix(
	fileName: string,
	suffixes: readonly string[],
): string | undefined {
	for (const suffix of suffixes) {
		if (fileName.endsWith(suffix)) {
			return fileName.slice(0, -suffix.length);
		}
	}
	return undefined;
}

export function collectLocalizedContentSlugEntries(
	...moduleGroups: Array<Record<string, unknown>>
): LocalizedContentSlugEntry[] {
	const entries = new Map<string, LocalizedContentSlugEntry>();

	for (const modules of moduleGroups) {
		for (const path of Object.keys(modules)) {
			const fileName = getFileName(path);
			const englishSlug = stripSuffix(fileName, ENGLISH_SUFFIXES);
			const defaultSlug =
				englishSlug === undefined ? stripSuffix(fileName, DEFAULT_SUFFIXES) : undefined;
			const slug = englishSlug ?? defaultSlug;

			if (!slug) {
				continue;
			}

			const current = entries.get(slug) ?? {
				slug,
				hasDefaultContent: false,
				hasEnglishContent: false,
			};

			if (englishSlug !== undefined) {
				current.hasEnglishContent = true;
			} else {
				current.hasDefaultContent = true;
			}

			entries.set(slug, current);
		}
	}

	return [...entries.values()].sort((a, b) => a.slug.localeCompare(b.slug));
}

export function getLocalizedContentSlugsForLocale(
	entries: LocalizedContentSlugEntry[],
	locale: 'ja' | 'en',
): string[] {
	return entries
		.filter((entry) =>
			locale === 'ja'
				? entry.hasDefaultContent
				: entry.hasDefaultContent || entry.hasEnglishContent,
		)
		.map((entry) => entry.slug);
}

export function assertNoSpecialPageSlugConflicts(
	slugs: string[],
	locale: 'ja' | 'en',
): void {
	const reserved = new Set(
		(locale === 'en' ? englishStaticPageEntries : japaneseStaticPageEntries).map(
			(entry) => entry.slug,
		),
	);

	if (locale === 'ja') {
		reserved.add('en');
	}

	for (const slug of slugs) {
		if (reserved.has(slug)) {
			throw new Error(
				`Special page slug "${slug}" conflicts with an existing route. ` +
					'Choose a different file name in src/content/special-pages/.',
			);
		}
	}
}
