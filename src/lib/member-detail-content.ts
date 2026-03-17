import type { AstroComponentFactory } from 'astro/runtime/server/index.js';
import { loadLocalizedContent } from './content';
import {
	collectLocalizedContentSlugEntries,
	getLocalizedContentSlugsForLocale,
} from './detail-pages';

export type MemberDetailMarkdownModule = {
	default: AstroComponentFactory;
	frontmatter?: {
		title?: string;
		description?: string;
		lead?: string;
	};
};

export const memberDetailMarkdownModules = import.meta.glob(
	'../content/members/*.{md,mdx}',
) as Record<string, () => Promise<MemberDetailMarkdownModule>>;

export const memberDetailHtmlModules = import.meta.glob(
	'../content/members/*.html',
	{
		query: '?raw',
		import: 'default',
	},
) as Record<string, () => Promise<string>>;

export function getMemberDetailSlugs(locale: 'ja' | 'en'): string[] {
	const entries = collectLocalizedContentSlugEntries(
		memberDetailMarkdownModules,
		memberDetailHtmlModules,
	);
	return getLocalizedContentSlugsForLocale(entries, locale);
}

export function loadMemberDetailContent(
	locale: 'ja' | 'en',
	slug: string,
) {
	return loadLocalizedContent({
		locale,
		basePath: `../content/members/${slug}`,
		markdownModules: memberDetailMarkdownModules,
		htmlModules: memberDetailHtmlModules,
	});
}
