import sys
import os
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                            QFileDialog, QVBoxLayout, QHBoxLayout, QProgressBar,
                            QComboBox, QTextEdit, QSpinBox)
from PyQt5.QtCore import Qt
import yt_dlp


class SmartClipDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Clip Downloader (YouTube)")
        self.setGeometry(100, 100, 700, 500)

        # Layouts
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Video URL
        self.url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()
        main_layout.addWidget(self.url_label)
        main_layout.addWidget(self.url_input)

        # Start and End Time
        time_layout = QHBoxLayout()
        self.start_label = QLabel("Start (HH:MM:SS):")
        self.start_input = QLineEdit()
        self.end_label = QLabel("End (HH:MM:SS):")
        self.end_input = QLineEdit()
        time_layout.addWidget(self.start_label)
        time_layout.addWidget(self.start_input)
        time_layout.addWidget(self.end_label)
        time_layout.addWidget(self.end_input)
        main_layout.addLayout(time_layout)

        # Quality Options
        self.quality_label = QLabel("Select Quality:")
        self.quality_box = QComboBox()
        self.quality_box.addItems([
            "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p",
            "audio-64k", "audio-128k", "audio-320k"
        ])
        main_layout.addWidget(self.quality_label)
        main_layout.addWidget(self.quality_box)

        # Folder Selection
        self.folder_label = QLabel("Save to:")
        self.folder_path = QLineEdit()
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(self.browse_btn)
        main_layout.addWidget(self.folder_label)
        main_layout.addLayout(folder_layout)

        # Parallel Download Limit
        self.parallel_label = QLabel("Parallel Downloads:")
        self.parallel_spin = QSpinBox()
        self.parallel_spin.setMinimum(1)
        self.parallel_spin.setMaximum(10)
        self.parallel_spin.setValue(2)
        main_layout.addWidget(self.parallel_label)
        main_layout.addWidget(self.parallel_spin)

        # Download Button
        self.download_btn = QPushButton("Start Download")
        self.download_btn.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_btn)

        # Progress
        self.progress = QProgressBar()
        main_layout.addWidget(self.progress)

        # Log/History
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder")
        if folder:
            self.folder_path.setText(folder)

    def start_download(self):
        url = self.url_input.text()
        start = self.start_input.text()
        end = self.end_input.text()
        quality = self.quality_box.currentText()
        folder = self.folder_path.text()
        parallel = self.parallel_spin.value()

        if not all([url, start, end, folder]):
            self.log.append("⚠️ Please fill in all fields.")
            return

        self.progress.setValue(0)
        self.log.append("🔽 Starting download...")

        thread = threading.Thread(target=self.download_clip,
                                args=(url, start, end, quality, folder, parallel))
        thread.start()

    def download_clip(self, url, start, end, quality, folder, parallel):
        try:
            out_file = os.path.join(folder, "%(title)s.%(ext)s")

            if "audio" in quality:
                format_selector = "bestaudio"
                postprocessors = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality.split("-")[-1][:-1],
                }]
            else:
                format_selector = f"bestvideo[height={quality[:-1]}]+bestaudio/best"

                postprocessors = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]

            ydl_opts = {
                'format': format_selector,
                'outtmpl': out_file,
                'postprocessors': postprocessors,
                'download_sections': [{
                    'start_time': start,
                    'end_time': end,
                }],
                'concurrent_fragment_downloads': parallel,
                'progress_hooks': [self.ydl_progress_hook],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log.append("✅ Download complete.")
            self.progress.setValue(100)

        except Exception as e:
            self.log.append(f"❌ Error: {e}")

    def ydl_progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').strip().replace('%', '')
            try:
                percent = float(percent)
                self.progress.setValue(int(percent))
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SmartClipDownloader()
    win.show()
    sys.exit(app.exec_())
