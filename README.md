# 篠田・牧野研究室 ホームページ管理マニュアル

[Astro](https://astro.build/) を使用して構築された研究室ホームページのソースコード.

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
4. ターミナルに表示される `http://localhost:4321/hapislab-org-homepage` にアクセス

---

## 📝 コンテンツの更新方法

### 1. ニュース (News) の更新

`src/content/news/` 内に新しい Markdown (`.md`) ファイルを作成.
ファイル名はなんでもいい.

```markdown
---
date: "2026-03-14"         # 掲載日
expireDate: "2026-12-31"   # (任意) 掲載期限. この日を過ぎると非表示になる
---
ここにニュース本文を記述. [リンク](https://example.com) も使える.
```

### 2. 関連プロジェクト (Related projects) の更新

`src/content/home/projects.json` (日本語用) または `projects.en.json` (英語用) を編集.

```json
{
  "title": "プロジェクト名",
  "href": "https://...",
  "description": "説明文",
  "image": "/src/assets/projects/image.jpg"
}
```

### 3. 研究テーマ (Research Topics) の追加

`src/content/research-topics/` にMarkdownファイルを作成

```
---
title: 研究テーマのタイトル
summary: 研究テーマの概要
date: '2015-10-01'         # 公開日
updated: '2018-12-28'      # (任意) 更新日
image: /assets/research-topics/2d-communication-tile/hero.png # サムネイルとページのトップに表示される画像 (必須)
imageAlt: 二次元通信タイル # 画像の代替テキスト (必須)
---

本文
```

---

## 🛠 GitHub でのプルリクエスト (PR) の送り方

研究室メンバーはリポジトリに直接書き込み権限が与えられているが, **`main` ブランチへ直接 Push することはできない.** 
以下の手順でプルリクエストを送ること.

### GitHub CLI (`gh`) を使った手順 (推奨)

1. **ブランチを作成**: ブランチ名前はわかりやすいものを推奨
   ```sh
   git switch -c my-update-name
   ```
2. **ファイルを編集し, 保存**
3. **変更をコミット**:
   ```sh
   git add .
   git commit -m "わかりやすいコメント"
   ```
4. **プルリクエストを作成**:
   ```sh
   gh pr create --web
   ```
   ※ `--web` をつけるとブラウザが開く. 内容を確認してボタンを押せば完了.

### 承認と公開

作成された PR を管理者が確認し, 問題なければ `main` ブランチへマージする.
マージされると自動的に公開サイトへ反映される.
