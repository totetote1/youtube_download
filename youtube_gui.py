import os
import queue
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_BIN = os.path.join(SCRIPT_DIR, "venv", "bin", "python3")
DEFAULT_DOWNLOAD_DIR = os.path.expanduser("~/Downloads")


class YouTubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube 動画ダウンローダー")
        self.geometry("760x520")
        self.minsize(680, 440)

        self.output_queue = queue.Queue()
        self.process = None
        self.worker = None

        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value=DEFAULT_DOWNLOAD_DIR)
        self.status_var = tk.StringVar(value="待機中")

        self._build_ui()
        self.after(100, self._drain_output_queue)

    def _build_ui(self):
        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(4, weight=1)

        ttk.Label(root, text="YouTube URL").grid(row=0, column=0, sticky="w")
        url_row = ttk.Frame(root)
        url_row.grid(row=1, column=0, sticky="ew", pady=(6, 14))
        url_row.columnconfigure(0, weight=1)

        url_entry = ttk.Entry(url_row, textvariable=self.url_var)
        url_entry.grid(row=0, column=0, sticky="ew")
        url_entry.focus_set()

        ttk.Button(url_row, text="貼り付け", command=self._paste_url).grid(
            row=0, column=1, padx=(8, 0)
        )

        ttk.Label(root, text="保存先").grid(row=2, column=0, sticky="w")
        output_row = ttk.Frame(root)
        output_row.grid(row=3, column=0, sticky="ew", pady=(6, 14))
        output_row.columnconfigure(0, weight=1)

        ttk.Entry(output_row, textvariable=self.output_dir_var).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Button(output_row, text="選択", command=self._select_output_dir).grid(
            row=0, column=1, padx=(8, 0)
        )

        log_frame = ttk.LabelFrame(root, text="ログ")
        log_frame.grid(row=4, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, height=14, wrap="word", state="disabled")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(root)
        bottom.grid(row=5, column=0, sticky="ew", pady=(14, 0))
        bottom.columnconfigure(1, weight=1)

        self.download_button = ttk.Button(
            bottom, text="ダウンロード開始", command=self._start_download
        )
        self.download_button.grid(row=0, column=0)

        self.stop_button = ttk.Button(
            bottom, text="停止", command=self._stop_download, state="disabled"
        )
        self.stop_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

        ttk.Label(bottom, textvariable=self.status_var).grid(row=0, column=2, sticky="e")

    def _paste_url(self):
        try:
            self.url_var.set(self.clipboard_get().strip())
        except tk.TclError:
            messagebox.showinfo("貼り付け", "クリップボードにテキストがありません。")

    def _select_output_dir(self):
        selected = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if selected:
            self.output_dir_var.set(selected)

    def _start_download(self):
        url = self.url_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        if not url:
            messagebox.showwarning("URL未入力", "YouTubeのURLを入力してください。")
            return

        if not os.path.isdir(output_dir):
            messagebox.showwarning("保存先エラー", "保存先フォルダが存在しません。")
            return

        if not os.path.exists(PYTHON_BIN):
            messagebox.showerror(
                "Python環境が見つかりません",
                "venv/bin/python3 が見つかりません。先にセットアップしてください。",
            )
            return

        self._set_running(True)
        self._append_log("\n--- ダウンロード処理を開始します ---\n")

        self.worker = threading.Thread(
            target=self._download_worker, args=(url, output_dir), daemon=True
        )
        self.worker.start()

    def _download_worker(self, url, output_dir):
        output_template = os.path.join(output_dir, "%(title)s.%(ext)s")
        cmd = [
            PYTHON_BIN,
            "-m",
            "yt_dlp",
            "--remote-components",
            "ejs:github",
            "--cookies-from-browser",
            "chrome",
            "--no-playlist",
            "--extractor-args",
            "youtube:player_client=tv_embedded,android,web",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "--merge-output-format",
            "mp4",
            "-o",
            output_template,
            url,
        ]

        try:
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )

            assert self.process.stdout is not None
            for line in self.process.stdout:
                self.output_queue.put(("log", line))

            return_code = self.process.wait()
            if return_code == 0:
                self.output_queue.put(("done", "完了しました。保存先を確認してください。"))
            elif return_code < 0:
                self.output_queue.put(("error", "停止しました。"))
            else:
                self.output_queue.put(
                    (
                        "error",
                        "ダウンロードに失敗しました。ChromeをCmd+Qで完全終了してから再試行してください。",
                    )
                )
        except Exception as exc:
            self.output_queue.put(("error", f"エラーが発生しました: {exc}"))
        finally:
            self.process = None

    def _stop_download(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self._append_log("\n--- 停止要求を送信しました ---\n")

    def _drain_output_queue(self):
        try:
            while True:
                kind, message = self.output_queue.get_nowait()
                if kind == "log":
                    self._append_log(message)
                elif kind == "done":
                    self._append_log(f"\n{message}\n")
                    self.status_var.set("完了")
                    self._set_running(False)
                    messagebox.showinfo("完了", message)
                elif kind == "error":
                    self._append_log(f"\n{message}\n")
                    self.status_var.set("エラー")
                    self._set_running(False)
                    messagebox.showerror("エラー", message)
        except queue.Empty:
            pass

        self.after(100, self._drain_output_queue)

    def _append_log(self, text):
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _set_running(self, running):
        self.download_button.configure(state="disabled" if running else "normal")
        self.stop_button.configure(state="normal" if running else "disabled")
        self.status_var.set("実行中" if running else "待機中")


if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
