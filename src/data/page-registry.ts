export interface StaticPageEntry {
	slug: string;
	currentPath: string;
	contentId: string;
	title?: string;
	description?: string;
	lead?: string;
	languageSwitchHref?: string;
}

export const japaneseStaticPageEntries: StaticPageEntry[] = [
	{
		slug: 'プロジェクト',
		currentPath: '/プロジェクト',
		contentId: 'project',
		title: 'これまでの成果',
		description: '実体化映像プロジェクトの成果と概要',
		languageSwitchHref: '/en/project-results',
	},
	{
		slug: 'メンバー',
		currentPath: '/メンバー',
		contentId: 'members',
		title: 'メンバー',
		description: 'Materialized Graphics プロジェクトの参加メンバー',
		languageSwitchHref: '/en/members',
	},
];

export const englishStaticPageEntries: StaticPageEntry[] = [
	{
		slug: 'project-results',
		currentPath: '/en/project-results',
		contentId: 'project',
		title: 'Project Results',
		description: 'Project overview and results for Materialized Graphics',
		languageSwitchHref: '/プロジェクト',
	},
	{
		slug: 'members',
		currentPath: '/en/members',
		contentId: 'members',
		title: 'Members',
		description: 'Project member directory for Materialized Graphics',
		languageSwitchHref: '/メンバー',
	},
];
