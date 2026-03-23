export interface TopicSummary {
	title: string;
	summary: string;
	image: string;
	imageAlt?: string;
	date?: string;
	updated?: string;
	detailPath?: string;
	detailPathEn?: string;
}

export interface SiteMeta {
	japaneseName: string;
	englishName: string;
	topbarJa: string;
	topbarEn: string;
}

export const siteMeta: SiteMeta = {
	japaneseName: 'Materialized Graphics Project',
	englishName: 'Materialized Graphics Project',
	topbarJa: 'JST CREST Symbiotic Interaction',
	topbarEn: 'JST CREST Symbiotic Interaction',
};
