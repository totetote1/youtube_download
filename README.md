
```markdown
# YouTube Downloader (yt-dlp wrapper)

Mac環境でYouTube動画を安全かつ確実にダウンロードするためのPythonスクリプトです。
YouTubeの最新のボット対策（JavaScriptパズル）を回避するために、`yt-dlp` と `Deno` を組み合わせて動作します。

## 🛠 必須要件

実行には以下のツールが必要です。

- **Python 3.10+**
- **Homebrew** (Mac用パッケージマネージャ)
- **Deno** (YouTubeの暗号解読エンジンとして使用)
- **Google Chrome** (認証クッキーの取得用)

## 🚀 セットアップ手順

### 1. 外部依存ツールのインストール
YouTubeの暗号（Signature/n-challenge）を解くために `deno` をインストールします。

```bash
brew install deno

```

### 2. プロジェクトの準備

リポジトリをクローンまたはフォルダに移動した後、仮想環境を作成しライブラリをインストールします。

```bash
# フォルダへ移動
cd youtube_download

# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate

# yt-dlpのインストール
pip install -U yt-dlp

```

## 📂 構成ファイル

* `youtube.py`: メインの実行スクリプト
* `venv/`: Python仮想環境（`.gitignore` で除外推奨）
* `README.md`: このファイル

## 📝 使い方

1. **Google Chromeを完全に終了**させます（クッキー読み取りエラー防止）。
2. ターミナルで仮想環境を有効化します。
```bash
source venv/bin/activate

```


3. スクリプトを実行します。
```bash
python youtube.py

```


4. プロンプトが表示されたら、YouTubeの動画URLを貼り付けて `Enter` を押してください。

## 💡 トラブルシューティング

### 「Requested format is not available」が出る場合

YouTubeの制限が更新されています。以下のコマンドでライブラリを最新に更新してください。

```bash
pip install -U yt-dlp

```

### Macのキーチェーンアクセスを求められる場合

スクリプトがChromeのクッキーを読み取る際、Macのシステムパスワードを求められることがあります。「常に許可」を選択してください。

### プレイリストのURLを貼った場合

本スクリプトは `'noplaylist': True` 設定になっているため、プレイリストのURLを貼り付けても、その中の1動画のみをダウンロードします。


