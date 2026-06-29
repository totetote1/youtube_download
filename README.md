# YouTube動画ダウンローダー

MacでYouTube動画をダウンロードするための小さなGUIアプリです。

URLを貼り付けて保存先を選ぶだけで、`yt-dlp` を使って動画を保存します。既存のコマンドライン版も残しています。

## できること

- YouTube URLから動画をダウンロード
- 保存先フォルダの選択
- ダウンロードログの表示
- 実行中の停止
- ChromeのCookieを使った認証付きダウンロード

## 必要なもの

- macOS
- Python 3.10以上
- Deno
- Google Chrome

`yt-dlp` はプロジェクト内の `venv` にインストールして使います。

## セットアップ

初回だけ以下を実行します。

```bash
cd ~/Desktop/codex/web/youtube_download
python3 -m venv venv
venv/bin/pip install -U yt-dlp
brew install deno
```

すでにこのフォルダで使えている場合は、セットアップ済みです。

## GUI版の起動方法

Finderで以下のファイルをダブルクリックします。

```text
YouTube動画ダウンロード_GUI.command
```

Terminalから起動する場合:

```bash
cd ~/Desktop/codex/web/youtube_download
./YouTube動画ダウンロード_GUI.command
```

起動したら、YouTube URLを入力し、保存先を選んで「ダウンロード開始」を押してください。

## CLI版の起動方法

従来のターミナル版を使う場合は、以下をダブルクリックします。

```text
YouTube動画ダウンロード.command
```

またはTerminalから実行します。

```bash
cd ~/Desktop/codex/web/youtube_download
./YouTube動画ダウンロード.command
```

## Chrome Cookieについて

このアプリは `--cookies-from-browser chrome` を使います。

エラーが出る場合は、Google Chromeを `Cmd+Q` で完全終了してから再試行してください。macOSのキーチェーン確認が出た場合は、許可してください。

## 保存先

GUI版では保存先を選択できます。

CLI版では初期設定で `~/Downloads` に保存します。

## トラブルシューティング

### yt-dlpが見つからない

以下を実行してください。

```bash
cd ~/Desktop/codex/web/youtube_download
venv/bin/pip install -U yt-dlp
```

### denoが見つからない

以下を実行してください。

```bash
brew install deno
```

### ダウンロードに失敗する

以下を試してください。

- Chromeを `Cmd+Q` で完全終了する
- `yt-dlp` を更新する
- URLを貼り直す
- 保存先に書き込み権限があるか確認する

```bash
cd ~/Desktop/codex/web/youtube_download
venv/bin/pip install -U yt-dlp
```

## ファイル構成

```text
youtube_gui.py                         GUI版アプリ本体
YouTube動画ダウンロード_GUI.command     GUI版の起動ファイル
youtube.py                             CLI版アプリ本体
YouTube動画ダウンロード.command         CLI版の起動ファイル
README.md                              この説明書
```

## 注意

ダウンロード対象の動画は、利用規約と著作権を守って扱ってください。
