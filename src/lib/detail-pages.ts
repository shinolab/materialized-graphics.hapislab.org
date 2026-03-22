import {
	englishStaticPageEntries,
	japaneseStaticPageEntries,
} from '../data/page-registry';

export interface LocalizedContentSlugEntry {
	slug: string;
	hasDefaultContent: boolean;
	hasEnglishContent: boolean;
}

const DEFAULT_SUFFIXES = ['.mdx', '.md', '.html'] as const;
const ENGLISH_SUFFIXES = ['.en.mdx', '.en.md', '.en.html'] as const;

function getRelativeContentPath(
	path: string,
	relativePathPrefix: string,
): string | undefined {
	const prefixIndex = path.indexOf(relativePathPrefix);
	if (prefixIndex === -1) {
		return undefined;
	}

	return path.slice(prefixIndex + relativePathPrefix.length);
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
	relativePathPrefix: string,
	...moduleGroups: Array<Record<string, unknown>>
): LocalizedContentSlugEntry[] {
	const entries = new Map<string, LocalizedContentSlugEntry>();

	for (const modules of moduleGroups) {
		for (const path of Object.keys(modules)) {
			const relativePath = getRelativeContentPath(path, relativePathPrefix);
			if (!relativePath) {
				continue;
			}

			const englishSlug = stripSuffix(relativePath, ENGLISH_SUFFIXES);
			const defaultSlug =
				englishSlug === undefined
					? stripSuffix(relativePath, DEFAULT_SUFFIXES)
					: undefined;
			let slug = englishSlug ?? defaultSlug;

			if (slug === 'index') {
				slug = '';
			} else if (slug?.endsWith('/index')) {
				slug = slug.slice(0, -'/index'.length);
			}

			if (slug === undefined) {
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
		const topLevelSegment = slug.split('/')[0] ?? slug;

		if (reserved.has(slug)) {
			throw new Error(
				`Special page slug "${slug}" conflicts with an existing route. ` +
					'Choose a different file name in src/content/special-pages/.',
			);
		}

		if (slug.includes('/') && reserved.has(topLevelSegment)) {
			throw new Error(
				`Special page slug "${slug}" uses reserved top-level segment "${topLevelSegment}". ` +
					'Choose a different top-level directory name in src/content/special-pages/.',
			);
		}
	}
}
