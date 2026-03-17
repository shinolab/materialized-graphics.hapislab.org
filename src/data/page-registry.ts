export interface StaticPageEntry {
	slug: string;
	currentPath: string;
	kind: 'basic' | 'members' | 'publications' | 'topics' | 'awards';
	contentId?: string;
	title?: string;
	description?: string;
	lead?: string;
	introHtml?: string;
}

export const japaneseStaticPageEntries: StaticPageEntry[] = [
	{ slug: 'research-topics', currentPath: '/research-topics', kind: 'topics', title: '研究テーマ', description: '研究テーマの紹介' },
	{ slug: 'members', currentPath: '/members', kind: 'members', title: 'メンバー', description: '研究室メンバーの一覧' },
	{ slug: 'publications', currentPath: '/publications', kind: 'publications', title: '発表論文', description: '研究室の論文一覧' },
	{ slug: 'awards', currentPath: '/awards', kind: 'awards', title: '受賞', description: '受賞実績' },
	{ slug: 'access', currentPath: '/access', kind: 'basic', contentId: 'access' },
	{ slug: 'links', currentPath: '/links', kind: 'basic', contentId: 'links' },
];

export const englishStaticPageEntries: StaticPageEntry[] = [
	{ slug: 'research-topics', currentPath: '/en/research-topics', kind: 'topics', title: 'Research Topics', description: 'Research Topics' },
	{ slug: 'members', currentPath: '/en/members', kind: 'members', title: 'Members', description: 'Member directory' },
	{ slug: 'publications', currentPath: '/en/publications', kind: 'publications', title: 'Publications', description: 'Publication list' },
	{ slug: 'awards', currentPath: '/en/awards', kind: 'awards', title: 'Awards', description: 'awards' },
	{ slug: 'access', currentPath: '/en/access', kind: 'basic', contentId: 'access' },
	{ slug: 'links', currentPath: '/en/links', kind: 'basic', contentId: 'links' },
];
