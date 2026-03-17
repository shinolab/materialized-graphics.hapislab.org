import type { AstroComponentFactory } from 'astro/runtime/server/index.js';
import { loadLocalizedContent } from './content';
import {
	assertNoSpecialPageSlugConflicts,
	collectLocalizedContentSlugEntries,
	getLocalizedContentSlugsForLocale,
} from './detail-pages';

export type SpecialPageMarkdownModule = {
	default: AstroComponentFactory;
	frontmatter?: {
		title?: string;
		description?: string;
		lead?: string;
	};
};

export const specialPageMarkdownModules = import.meta.glob(
	'../content/special-pages/*.md',
) as Record<string, () => Promise<SpecialPageMarkdownModule>>;

export const specialPageHtmlModules = import.meta.glob(
	'../content/special-pages/*.html',
	{
		query: '?raw',
		import: 'default',
	},
) as Record<string, () => Promise<string>>;

export function getSpecialPageSlugs(locale: 'ja' | 'en'): string[] {
	const entries = collectLocalizedContentSlugEntries(
		specialPageMarkdownModules,
		specialPageHtmlModules,
	);
	const slugs = getLocalizedContentSlugsForLocale(entries, locale);
	assertNoSpecialPageSlugConflicts(slugs, locale);
	return slugs;
}

export function loadSpecialPageContent(
	locale: 'ja' | 'en',
	slug: string,
) {
	return loadLocalizedContent({
		locale,
		basePath: `../content/special-pages/${slug}`,
		markdownModules: specialPageMarkdownModules,
		htmlModules: specialPageHtmlModules,
	});
}
