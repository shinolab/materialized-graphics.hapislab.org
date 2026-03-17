# 篠田・牧野研究室 ホームページ管理マニュアル

- [🚀 ローカルでのプレビュー手順](#-%E3%83%AD%E3%83%BC%E3%82%AB%E3%83%AB%E3%81%A7%E3%81%AE%E3%83%97%E3%83%AC%E3%83%93%E3%83%A5%E3%83%BC%E6%89%8B%E9%A0%86)
- [📝 コンテンツの更新方法](#-%E3%82%B3%E3%83%B3%E3%83%86%E3%83%B3%E3%83%84%E3%81%AE%E6%9B%B4%E6%96%B0%E6%96%B9%E6%B3%95)
    - [発表論文の追加](#%E7%99%BA%E8%A1%A8%E8%AB%96%E6%96%87%E3%81%AE%E8%BF%BD%E5%8A%A0)
        - [雑誌論文](#%E9%9B%91%E8%AA%8C%E8%AB%96%E6%96%87)
        - [査読付き国際会議論文](#%E6%9F%BB%E8%AA%AD%E4%BB%98%E3%81%8D%E5%9B%BD%E9%9A%9B%E4%BC%9A%E8%AD%B0%E8%AB%96%E6%96%87)
        - [デモ](#%E3%83%87%E3%83%A2)
        - [国内会議論文](#%E5%9B%BD%E5%86%85%E4%BC%9A%E8%AD%B0%E8%AB%96%E6%96%87)
    - [Newsの更新](#news%E3%81%AE%E6%9B%B4%E6%96%B0)
    - [関連プロジェクトの更新](#%E9%96%A2%E9%80%A3%E3%83%97%E3%83%AD%E3%82%B8%E3%82%A7%E3%82%AF%E3%83%88%E3%81%AE%E6%9B%B4%E6%96%B0)
    - [研究テーマの追加](#%E7%A0%94%E7%A9%B6%E3%83%86%E3%83%BC%E3%83%9E%E3%81%AE%E8%BF%BD%E5%8A%A0)
    - [受賞リストの更新](#%E5%8F%97%E8%B3%9E%E3%83%AA%E3%82%B9%E3%83%88%E3%81%AE%E6%9B%B4%E6%96%B0)
    - [メンバーの更新](#%E3%83%A1%E3%83%B3%E3%83%90%E3%83%BC%E3%81%AE%E6%9B%B4%E6%96%B0)
        - [学生](#%E5%AD%A6%E7%94%9F)
        - [スタッフ](#%E3%82%B9%E3%82%BF%E3%83%83%E3%83%95)
- [🛠GitHubでのプルリクエスト PR の送り方](#github%E3%81%A7%E3%81%AE%E3%83%97%E3%83%AB%E3%83%AA%E3%82%AF%E3%82%A8%E3%82%B9%E3%83%88-pr-%E3%81%AE%E9%80%81%E3%82%8A%E6%96%B9)
    - [GitHub CLIを使った手順 推奨](#github-cli%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E6%89%8B%E9%A0%86-%E6%8E%A8%E5%A5%A8)
    - [承認と公開](#%E6%89%BF%E8%AA%8D%E3%81%A8%E5%85%AC%E9%96%8B)


## 🚀 ローカルでのプレビュー手順

ローカルPCで変更内容を確認するための手順は以下の通り.

1. 事前準備: [Node.js](https://nodejs.org/) (v22以上推奨) のインストール
2. リポジトリのクローンと初期化: ターミナルで以下のコマンドを実行
    ```sh
    git clone https://github.com/shinolab/hapislab-org-homepage.git
    cd hapislab-org-homepage
    npm i
    ```
3. **開発サーバーの起動**:
   ```sh
   npm run dev
   ```
4. ターミナルに表示されるURL (`http://localhost:4321/hapislab-org-homepage`) にアクセス

---

## 📝 コンテンツの更新方法

### 一般的な注意

画像は `src/assets/` 以下に配置すること.
ただし, ファイルサイズが大きい画像はGitHubの容量制限に引っかかる可能性があるので, そういう場合はWeb用に圧縮するか外部ストレージに置いてリンクすること.

PDFファイルは研究室の共有Google Driveの`homepage-public`フォルダ以下においてリンクすること.

### 発表論文の追加

`src/data/publications.yml` を編集.
種類によらず先頭から適当に追加して良い.

よくわからない場合は既存のエントリを参考にして, フォーマットを合わせること.

なお, 値にコロン":"が含まれる場合は全体をクオーテーションで囲む必要がある. 例: `title: 'Title: Subtitle'`

追加で, `pages`とか`volume`とかのフィールドを追加しても良い. というか新規の場合は追加しておいてほしい.

> TODO: Bibtex形式からの自動インポート機能を追加

#### 雑誌論文

```yaml
- type: article
  year: 2025
  authors:
    - First Last
    - First Last
  title: Title of the Paper
  journal: Journal Name
  doi: xxx/xxxxxx (optional, https://doi.org/ は入れないこと)
  href: リンク (optional)
  note: 補足情報 (optional)
```

doiがあって, `href`がない場合は自動的にdoiからリンクが生成される.

#### 査読付き国際会議論文

```yaml
- type: inproceedings
  year: 2025
  authors:
    - First Last
    - First Last
  title: Title of the Paper
  booktitle: Conference Name
  doi: xxx/xxxxxx (optional, https://doi.org/ は入れないこと)
  href: リンク (optional)
  note: 補足情報 (optional)
```

#### デモ

```yaml
- type: demos
  year: 2025
  authors:
    - First Last
    - First Last
  title: Title of the Demo
  booktitle: Conference Name
  doi: xxx/xxxxxx (optional, https://doi.org/ は入れないこと)
  href: リンク (optional)
  note: 補足情報 (optional)
```

#### 国内会議論文

```yaml
- type: domestic
  year: 2025
  authors:
    ‐ 姓 名
    ‐ 姓 名
  title: タイトル
  booktitle: 会議名
  doi: xxx/xxxxxx (optional, https://doi.org/ は入れないこと)
  href: リンク (optional)
  note: 補足情報 (optional)
```

日本語しか想定してない

### Newsの更新

`src/content/top/news/` 内に新しい Markdown ファイルを作成.
`.md`だと日本語用, `.en.md`だと英語用のニュースになる.
ファイル名はなんでもいい.

```markdown
---
date: "2026-03-14"         # 掲載日
expireDate: "2026-12-31"   # (任意) 掲載期限. この日を過ぎると非表示になる
---
ここにニュース本文を記述. [リンク](https://example.com) も使える.
```

### 関連プロジェクトの更新

`src/content/top/projects.json` (日本語用) または `projects.en.json` (英語用) を編集.

```json
{
  "title": "プロジェクト名",
  "href": "https://...",
  "description": "説明文",
  "image": "/src/assets/projects/image.jpg"
}
```

### 研究テーマの追加

`src/content/research-topics/` にMarkdownファイルを作成.

```
---
title: 研究テーマのタイトル
summary: 研究テーマの概要
date: '2015-10-01'         # 公開日
updated: '2018-12-28'      # (任意) 更新日
image: /assets/research-topics/xxxx/hero.png # サムネイルとページのトップに表示される画像 (必須)
imageAlt: xxxx # 画像の代替テキスト (必須)
---

本文
```

画像は `src/assets/research-topics/`以下に適当なフォルダを作って配置すること.

### 受賞リストの更新

`src/data/awards.yml` を編集.

```yaml
- year: 2023        # 受賞年
  month: 12         # 受賞月 (optional)
  day: 15           # 受賞日 (optional)
  award: すごい賞   # 受賞名
  org: なんとか団体 # 授与団体 (optaional)
  title: 素晴らしいタイトル # 受賞対象となった研究のタイトル (optional)
  recipients: # 受賞者. 空の場合 recipients: [] とすること
    - 受賞者1
    - 受賞者2
  href: https://example.com/award-link # 受賞に関する詳細情報へのリンク (optional)
```

研究室の学生ではないが, 関連が高い為載せたい場合は
```yaml
  external: true
```
を追加する.

### メンバーの更新

ポスドク以降はスタッフ側で管理している.

#### 学生

`src/data/students.yml` を編集. 

```yaml
- name: 性 名
  nameEn: First Last
  email: sample@hapis.k.u-tokyo.ac.jp
  campus: Hongo # Hongo or Kashiwa (特に使ってない)
  href: http://hapislab.org/sample # 個人ページなどへのリンク (任意)
  degrees:
    B:
      grad: 2024-03-31
      thesis: "卒業論文タイトル"
    M:
      grad: 2024-03-31 
      thesis: "修士論文タイトル" 
    D:
      start: 2024-04-01
      grad: ""
```

`grad`が存在する場合, 卒業生リストに表示される. `grad`が空の場合は在籍中の学生として表示される.

#### スタッフ

`src/data/alumni.yml` を編集.

```yaml
- name: 性 名
  nameEn: First Last
  role: 教授 # 教授, 准教授, 助教, 研究員など
  roleEn: Professor # 英語表記
  startDate: 2000-04-01 # 就任日
  endDate: 2008-03-31 # 退任日. 在籍中の場合は空にする
  email: sample@hapis.k.u-tokyo.ac.jp
  href: http://hapislab.org/sample # 個人ページなどへのリンク (任意)
```

`endDate`が存在する場合, 卒業生リストに表示される. `endDate`が空の場合は在籍中のスタッフとして表示される.

## 🛠GitHubでのプルリクエスト (PR) の送り方

研究室メンバーはリポジトリに直接書き込み権限が与えられているが, **`main` ブランチへ直接 Push することはできない.** 
以下の手順でプルリクエストを送ること.

### GitHub CLIを使った手順 (推奨)

事前に [GitHub CLI](https://cli.github.com/) をインストールしておくこと.

1. **最新の情報を取得**: 自分のPC上の `main` ブランチを最新する
   ```sh
   git switch main
   git pull origin main
   ```
2. **ブランチを作成**: 作業用のブランチを新しく作成. ブランチ名はわかりやすいものにすること.
   ```sh
   git switch -c my-update-name
   ```
3. **ファイルを編集し, 保存**
4. **変更をコミット**:
   ```sh
   git add .
   git commit -m "わかりやすいコメント"
   ```
5. **プルリクエストを作成**:
   ```sh
   gh pr create --web
   ```
   - "Where should we push the '...' branch?"と聞かれたら, "shinolab/hapislab-org-homepage"を選択.
   - `--web` をつけるとブラウザが開く. 内容を確認してボタンを押せば完了.

### 承認と公開

作成された PR を管理者が確認し, 問題なければ `main` ブランチへマージする.
マージされると自動的に公開サイトへ反映される.
