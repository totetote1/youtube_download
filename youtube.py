import yt_dlp

def download_youtube_video():
    # URLを入力（ここでは " " で囲む必要はありません！）
    url = input("YouTubeのURLを入力してください: ")

    # コマンド版で成功した「暗号解読設定」をすべて反映
    ydl_opts = {
        # 1. 画質設定：見つかる中でベストな動画を選択
        'format': 'best',
        
        # 2. プレイリスト対策：URLにリストIDが含まれていても1本だけ落とす
        'noplaylist': True,
        
        # 3. 人間証明：Chromeのクッキーを使用（Chromeは終了させておいてください）
        'cookiesfrombrowser': ('chrome',),
        
        # 4. 保存名：動画タイトル.拡張子
        'outtmpl': '%(title)s.%(ext)s',
        
        # 5. 【最重要】コマンド版で成功した「解読スクリプト許可」の設定
        'extractor_args': {
            'youtube': {
                'remote_components': ['ejs:github'],
            }
        },
        
        # 6. エラーが出ても途中で止めず、詳細を報告する
        'ignoreerrors': False,
        'quiet': False,
        'no_warnings': False,
    }

    try:
        print("\n--- ダウンロード処理を開始します ---")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 内部的に deno（インストール済み）を使ってパズルを解き始めます
            ydl.download([url])
        print("\n✅ 完了しました！フォルダ内を確認してください。")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("ヒント: Chromeを完全に終了(Cmd+Q)してから再試行してみてください。")

if __name__ == "__main__":
    download_youtube_video()