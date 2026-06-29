#!/bin/bash

cd "$(dirname "$0")"

export PATH="$HOME/.deno/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

if ! command -v deno &>/dev/null; then
    echo "deno が見つかりません。先に既存のCLI版.commandを一度起動してセットアップしてください。"
    exit 1
fi

if [ ! -x "venv/bin/python3" ]; then
    echo "venv/bin/python3 が見つかりません。"
    exit 1
fi

if [ ! -x "venv/bin/yt-dlp" ]; then
    echo "yt-dlp が見つかりません。インストールします..."
    venv/bin/pip install -U yt-dlp
fi

venv/bin/python3 youtube_gui.py
