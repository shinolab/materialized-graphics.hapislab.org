export interface NavItem {
    href: string;
    label: string;
}

const primaryNavByLocale = {
    ja: [
        { href: '/', label: '実体化映像による多次元インタラクション' },
        { href: '/プロジェクト', label: 'これまでの成果' },
        { href: '/メンバー', label: 'メンバー' },
    ],
    en: [
        { href: '/en/', label: 'Materialized Graphics Project' },
        { href: '/en/project-results', label: 'Project Results' },
        { href: '/en/members', label: 'Members' },
    ],
} satisfies Record<'ja' | 'en', NavItem[]>;

export function getPrimaryNav(locale: 'ja' | 'en' = 'ja'): NavItem[] {
    return primaryNavByLocale[locale];
}
