#!/bin/bash

# このファイルのある場所に移動
cd "$(dirname "$0")"

echo "======================================"
echo "  YouTube 動画ダウンローダー"
echo "  終了するには Ctrl+C を押してください"
echo "======================================"
echo ""

# denoがインストールされているか確認、なければ自動インストール
if ! command -v deno &>/dev/null; then
    echo "⚙️  deno が見つかりません。自動インストールします..."
    echo ""

    if command -v brew &>/dev/null; then
        brew install deno
    else
        curl -fsSL https://deno.land/install.sh | sh
        # インストール先をPATHに追加
        export PATH="$HOME/.deno/bin:$PATH"
    fi

    echo ""
    echo "✅ deno のインストール完了！"
    echo ""
fi

# denoをPATHに通す（インストール済みでも念のため）
export PATH="$HOME/.deno/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

# yt-dlpを最新版にアップデート
echo "⬆️  yt-dlp を最新版に更新中..."
venv/bin/pip install -U yt-dlp -q
echo "✅ 更新完了"
echo ""

# venvのPythonでスクリプトを実行
venv/bin/python3 youtube.py
