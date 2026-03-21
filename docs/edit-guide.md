# コンテンツの更新ガイド

このガイドでは, 篠田・牧野研究室ホームページの各コンテンツを更新・追加する方法について詳しく説明します.

> [!CAUTION]
> 変更を加える前に, 最新の main ブランチを取得し, 作業用のブランチで編集を行ってください.
> ```
> git switch main
> git pull origin main
> git switch -c <your-branch-name>
> ```

- Gitの操作に慣れていない場合は, GUIクライアントの使用を推奨します.
  - [VSCode](https://code.visualstudio.com/) + [GitGraph](https://marketplace.visualstudio.com/items?itemName=mhutchie.git-graph)
  - [GitKraken](https://www.gitkraken.com/)
  - [SourceTree](https://www.sourcetreeapp.com/)
  - 等々

  ## 目次

- [一般的な注意](#一般的な注意)
- [発表論文の追加 (publications.yml)](#発表論文の追加-publicationsyml)
    - [PublicationRef コンポーネントでの参照](#publicationref-コンポーネントでの参照)
- [Newsの更新](#newsの更新)
- [関連プロジェクトの更新](#関連プロジェクトの更新)
- [研究テーマの追加](#研究テーマの追加)
- [受賞リストの更新 (awards.yml)](#受賞リストの更新-awardsyml)
- [メンバーの更新](#メンバーの更新)
    - [学生 (students.yml)](#学生-studentsyml)
    - [スタッフ (staff.yml)](#スタッフ-staffyml)
    - [メンバー個別ページ](#メンバー個別ページ)
- [特殊ページの追加](#特殊ページの追加)

---

## 一般的な注意

### 画像・メディア
画像は `src/assets/` 以下に配置してください. 
ファイルサイズが大きい画像は, GitHubの容量制限を避けるため, Web用に圧縮するか, 外部ストレージに置いてリンクすることを検討してください.

Markdown/MDX 内で画像を表示する場合は, `src/assets/` 以下の画像を相対パスで指定します.
> 例: `src/content/members/example.mdx` から参照する場合: `![alt text](../../assets/path/to/image.png)`

### MDX とコンポーネント
`.mdx` ファイルでは, Astroコンポーネントをインポートして使用できます. 
例えば, クリックで拡大表示できる `MdxLightboxImage` コンポーネントが用意されています.

```mdx
import photo from "../../assets/members/example/image.png";
import MdxLightboxImage from "../../components/MdxLightboxImage.astro";

<MdxLightboxImage
  src={photo}
  alt="Example image"
  width={320}
  caption="クリックで拡大"
/>
```

### PDF ファイル
PDFファイルは研究室の共有Google Driveの `homepage-public` フォルダに配置し, その共有リンクを使用してください.

### セキュリティ
**このリポジトリに追加したデータはすべてパブリックに公開されます.** 機密情報や公開したくない個人情報は絶対に含めないでください.

---

## Markdown / MDX の書き方

コンテンツの多くは Markdown (`.md`) または MDX (`.mdx`) で記述します.

### 基本的な記法 (Markdown)
- **見出し**: `# 見出し1`, `## 見出し2`
- **強調**: `**太字**`, `*斜体*`
- **リスト**: `- 項目`, `1. 番号付き`
- **リンク**: `[テキスト](URL)`
- **画像**: `![代替テキスト](画像パス)`

### MDX 特有の機能
MDX では Markdown の中で HTML や Astro コンポーネントを使用できます. 
また, 文頭の `import` 文でコンポーネントを読み込む必要があります.

```mdx
import MyComponent from "../../components/MyComponent.astro";

# 記事のタイトル

<MyComponent parameter="value" />
```

---

## 発表論文の追加 (publications.yml)

`src/data/publications.yml` を編集します. 

### DOIからの自動生成

DOIがあるなら, スクリプトを使用して基本的な情報を自動生成できます.

この機能を使う場合, [uv](https://github.com/astral-sh/uv) をインストールしてから, 以下のコマンドを実行してください.

```
cd scripts
uv run python doi2pub.py <DOI>
```

すべての情報を取得できるわけではないので, 取得された内容を確認し, 不足しているフィールドを補完してください.

`crossref`に対応している場合 (ACMとか), `--crossref` オプションを付けると, 取得できる情報が増える(かもしれない).

### 共通の注意点 (YAML)
- 値にコロン `:` が含まれる場合は, 文字列全体をクォーテーションで囲んでください.
  - ⭕ `title: "Title: Subtitle"`
  - ❌ `title: Title: Subtitle`
- インデントは半角スペース2つで統一してください.

### 論文の種類別のテンプレート

**共通点として, `volume`, `number`, `pages`, `eventDate`, `location` などのフィールドも可能な限り追加してください.**

#### 雑誌論文 (`type: article`)
```yaml
- type: article
  year: 2025
  authors:
    - First Last
    - First Last
  title: "Paper Title"
  journal: "Journal Name"
  volume: 123
  number: 4
  pages: "567-589"
  doi: "xxx/xxxxxx" # https://doi.org/ は含めない
  note: 補足情報     # 末尾に追記されます
  href: "https://..." # DOIがある場合は自動生成されるため省略可
  refId: "unique-id" # MDXから参照する場合に指定
```

#### 査読付き国際会議論文 (`type: inproceedings`) / デモ (`type: demos`)

```yaml
- type: inproceedings # または demos
  year: 2025
  authors:
    - First Last
  title: "Conference Paper Title"
  booktitle: "Conference Name"
  pages: 123-130
  eventDate: July 8-11
  location: Tokyo, Japan
  doi: "xxx/xxxxxx"
```

#### 国内会議論文 (`type: domestic`)
```yaml
- type: domestic
  year: 2025
  authors:
    - 姓 名
  title: "タイトル"
  booktitle: "会議名"
  pages: 123-130
  eventDate: 7月8-11日
  location: 東京大学
```

### PublicationRef コンポーネントでの参照
`publications.yml` で `refId` を設定した論文は, MDXファイル内で以下のように引用形式で表示できます.

```mdx
import PublicationRef from "../../components/PublicationRef.astro";

<PublicationRef refId="your-ref-id" />
```

---

## Newsの更新

`src/content/top/news/` 内に新しい Markdown (`.md` / `.en.md`) ファイルを作成します.

```markdown
---
date: "2026-03-14"
expireDate: "2026-12-31" # 省略可
---
ニュース本文. Markdown記法が使えます.
```

---

## 関連プロジェクトの更新

`src/content/top/projects.json` (日本語) または `projects.en.json` (英語) を編集します.

```json
{
  "title": "プロジェクト名",
  "href": "https://...",
  "description": "説明文",
  "image": "/src/assets/projects/image.jpg"
}
```

---

## 研究テーマの追加

`src/content/research-topics/` に `.md`/`.mdx` ファイルを作成します. 英語版は `en.md`/`en.mdx` とします.

```mdx
---
title: 研究テーマのタイトル
titleEn: English Title (英語版がない場合の補足)
summary: 一覧ページに表示される短い概要
date: '2025-03-18'
thumbnail: /src/assets/research-topics/xxxx/thumb.png
thumbnailAlt: サムネイルの説明
---

本文をここに記述します.
```

---

## 受賞リストの更新 (awards.yml)

`src/data/awards.yml` を編集します.

```yaml
- year: 2025
  month: 3
  day: 18
  award: 賞の名前
  org: 授与団体
  recipients:
    - "受賞者名"
```

---

## メンバーの更新

### 学生 (students.yml)

`src/data/students.yml` を編集します. `grad` (卒業日) を空にすると「在籍中」, 入力すると「卒業生」として扱われます.

```yaml
- name: 姓 名
  nameEn: First Last
  email: user@example.com
  degrees:
    M:
      grad: "" # 在籍中の場合は空
      thesis: "修論タイトル"
```

### スタッフ (staff.yml)

`src/data/staff.yml` を編集します. `endDate` を指定すると「過去の在籍者」になります.

### メンバー個別ページ

`src/content/members/<slug>.md or .mdx` を作成することで, `/members/<slug>` というURLの個別ページが生成されます.

`.en.md`/`.en.mdx` とすることで英語版も作成できます.

---

## 特殊ページの追加

ルート直下に独自のURLを持つページを作成したい場合は, `src/content/special-pages/` にファイルを作成します.
例: `src/content/special-pages/my-page.mdx` -> `https://hapislab.org/my-page/`
