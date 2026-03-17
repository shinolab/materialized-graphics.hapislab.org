import yaml from 'js-yaml';
import publicationsYaml from '../data/publications.yml?raw';

export interface Publication {
	year: number;
	type: 'article' | 'inproceedings' | 'demos' | 'domestic' | 'Others';
	title: string;
	authors: string[];
	lang?: 'ja' | 'en';
	journal?: string;
	booktitle?: string;
	volume?: string;
	number?: string;
	pages?: string;
	doi?: string;
	note?: string;
	href?: string;
}

export const publications: Publication[] = (yaml.load(publicationsYaml) as Publication[] || [])
	.map((row) => ({
		year: typeof row.year === 'number' ? row.year : Number.parseInt(row.year as any, 10) || 0,
		type: (row.type as any) || 'Others',
		title: row.title?.trim() || '',
		authors: Array.isArray(row.authors) ? row.authors : [],
		lang:
			row.type === 'domestic'
				? 'ja'
				: row.lang === 'ja' || row.lang === 'en'
					? row.lang
					: undefined,
		journal: row.journal?.trim(),
		booktitle: row.booktitle?.trim(),
		volume: row.volume?.toString(),
		number: row.number?.toString(),
		pages: row.pages?.trim(),
		doi: row.doi?.trim(),
		note: row.note?.trim(),
		href: row.href?.trim() || (row.doi ? `https://doi.org/${row.doi.trim()}` : ''),
	}))
	.sort((left, right) => right.year - left.year);
