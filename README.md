# 篠田・牧野研究室 ホームページ管理マニュアル

このリポジトリは, [篠田・牧野研究室](https://hapislab.org/) の公式ウェブサイトのソースコードを管理しています.

👉 [**コンテンツ更新ガイド (docs/edit-guide.md)**](./docs/edit-guide.md)

---

## 🚀 クイックスタート (ローカルでのプレビュー)

変更内容を自分のPCで確認する手順です.

1. **事前準備**: [Node.js](https://nodejs.org/) (v22以上推奨) をインストール.
2. **クローンとセットアップ**:
    ```sh
    git clone https://github.com/shinolab/hapislab-org-homepage.git
    cd hapislab-org-homepage
    npm install
    ```
3. **開発サーバーの起動**:
   ```sh
   npm run dev
   ```
4. ブラウザで `http://localhost:4321` を開きます.

---

## 🛠 プルリクエスト (PR) の送り方

変更をサイトに反映させるには, プルリクエストを作成してください. **`main` ブランチへの直接 Push はできません.**

### 推奨: GitHub CLI (`gh`) を使う

事前に [GitHub CLI](https://cli.github.com/) をインストールしておいてください.

1. 最新の `main` を取得: `git switch main && git pull origin main`
2. 作業用ブランチ作成: `git switch -c <your-branch-name>`
    - ブランチ名は内容に応じて適宜変更してください.
3. 編集: 具体的な更新手順については, 以下のガイドを参照してください.
    - 👉 [**コンテンツ更新ガイド (docs/edit-guide.md)**](./docs/edit-guide.md)
4. コミット: `git add . && git commit -m "<your commit message>"`
    - コミットメッセージは変更内容がわかるように書いてください.
    - `git add .` は変更したファイルをすべてステージングします. 不要なファイル/機密ファイルなどが含まれないように注意してください. gitに慣れていない場合はGUIクライアントの使用を推奨します.
5. PR作成: `gh pr create --web`
    - ブラウザが開くので, タイトルと説明を入力して PR を作成してください.
    - `--web`を付けない場合は CLI 上で完結できます.

### GitHub Web UI を使う

1. [リポジトリページ](https://github.com/shinolab/hapislab-org-homepage)でファイルを直接編集.
2. "Commit changes..." から "Create a new branch..." を選択して PR を作成.

---

## ⚠️ 注意事項

- **公開情報**: このリポジトリに追加したデータはすべてパブリックに公開されます.
- **画像**: 大きな画像は圧縮するか, 外部ストレージを活用してください.
- **承認**: PR が管理者にマージされると, 自動的にサイトへ反映されます.
