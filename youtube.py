import subprocess
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_BIN = os.path.join(SCRIPT_DIR, 'venv', 'bin', 'python3')

def download_youtube_video(url):
    cmd = [
        PYTHON_BIN,
        '-m', 'yt_dlp',
        '--remote-components', 'ejs:github',
        '--cookies-from-browser', 'chrome',
        '--no-playlist',
        '--extractor-args', 'youtube:player_client=tv_embedded,android,web',
        '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        '--merge-output-format', 'mp4',
        '-o', os.path.expanduser('~/Downloads/%(title)s.%(ext)s'),
        url
    ]

    try:
        print("\n--- ダウンロード処理を開始します ---")
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print("\n✅ 完了しました！ダウンロードフォルダを確認してください。")
        else:
            print("\n❌ ダウンロードに失敗しました。")
            print("ヒント: Chromeを完全に終了(Cmd+Q)してから再試行してみてください。")

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    print("====================================")
    print("  YouTube 動画ダウンローダー")
    print("  終了するには Ctrl+C を押してください")
    print("====================================")
    while True:
        try:
            print("")
            url = input("YouTubeのURLを貼り付けてEnter: ").strip()
            if url:
                download_youtube_video(url)
            else:
                print("URLが入力されていません。もう一度入力してください。")
        except KeyboardInterrupt:
            print("\n\n終了します。お疲れ様でした！")
            break
