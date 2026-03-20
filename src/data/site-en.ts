import type { NavItem } from './site';

export const englishSiteMeta = {
	japaneseName: '篠田・牧野研究室',
	englishName: 'Shinoda & Makino Lab',
	tagline: 'Haptics & Applied Physics in Synthesis',
	description:
		'We pursue breakthroughs in real-world informatics by introducing new physical effects and structures into information systems.',
	affiliations: [
		'Department of Complexity Science and Engineering, Graduate School of Frontier Sciences',
		'Department of Information Physics and Computing, Graduate School of Information Science and Technology',
		'Department of Mathematical Engineering and Information Physics, School of Engineering',
	],
};

export const englishPrimaryNav: NavItem[] = [
	{ href: '/en/', label: 'Top' },
	{ href: '/en/research-topics', label: 'Topics' },
	{ href: '/en/members', label: 'Members' },
	{ href: '/en/awards', label: 'Awards' },
	{ href: '/en/publications', label: 'Publications' },
	{ href: '/en/access', label: 'Access' },
	{ href: '/en/links', label: 'Links' },
];
