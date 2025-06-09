from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QProgressBar, QComboBox, QListWidget)
from PyQt5.QtCore import Qt
import yt_dlp_wrapper
import history
import threading


class YouTubeClipDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Clip Downloader - PyQt Edition 🚀")
        self.setGeometry(300, 300, 600, 600)

        # Widgets
        self.url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()

        self.segments_label = QLabel("Segments (one per line, hh:mm:ss-hh:mm:ss):")
        self.segments_input = QTextEdit()

        self.format_label = QLabel("Select Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItem("Click 'List Formats' first")

        self.list_formats_button = QPushButton("List Formats")
        self.list_formats_button.clicked.connect(self.list_formats)

        self.locate_button = QPushButton("Locate Output Folder")
        self.locate_button.clicked.connect(self.locate_folder)
        self.output_folder = ""

        self.download_button = QPushButton("Download Clip")
        self.download_button.clicked.connect(self.download_clip)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.status_label = QLabel("Status: Waiting...")

        self.history_label = QLabel("Download History:")
        self.history_list = QListWidget()
        self.load_history()

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        layout.addWidget(self.segments_label)
        layout.addWidget(self.segments_input)

        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)
        layout.addWidget(self.list_formats_button)

        layout.addWidget(self.locate_button)
        layout.addWidget(self.download_button)

        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

        layout.addWidget(self.history_label)
        layout.addWidget(self.history_list)

        self.setLayout(layout)

    def locate_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.status_label.setText(f"Output folder set to: {folder}")

    def list_formats(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a URL first.")
            return
        self.status_label.setText("Fetching formats...")

        # Run in background thread:
        threading.Thread(target=self._list_formats_worker, args=(url,)).start()

    def _list_formats_worker(self, url):
        formats = yt_dlp_wrapper.list_formats(url)
        
        # Now update UI back on main thread:
        self.format_combo.clear()
        for fmt in formats:
            self.format_combo.addItem(fmt)

        self.status_label.setText("Formats loaded.")


    def download_clip(self):
        url = self.url_input.text().strip()
        # Clean URL to remove playlist params (optional but recommended):
        url_clean = url.split('&')[0]
        
        segments = self.segments_input.toPlainText().strip().splitlines()
        selected_format = self.format_combo.currentText().split(" ")[0]
        output_folder = self.output_folder

        if not url or not segments or not output_folder:
            self.status_label.setText("Please fill all fields.")
            return


        # Check if user selected format properly:
        if selected_format == "Click":
            self.status_label.setText("Please list and select a format first.")
            return
        
        self.status_label.setText("Starting download...")

        def progress_hook(progress):
            if progress.get("_percent_str"):
                percent = float(progress["_percent_str"].replace("%", "").strip())
                self.progress_bar.setValue(int(percent))
            if progress.get("eta"):
                self.status_label.setText(f"Downloading... ETA: {progress['eta']} sec")

        yt_dlp_wrapper.download_clip(url_clean,segments, selected_format, output_folder, progress_hook)

        # After download:
        history.add_to_history(url_clean, segments, selected_format)
        self.load_history()
        self.status_label.setText("Download finished!")
        self.progress_bar.setValue(100)

    def load_history(self):
        self.history_list.clear()
        past = history.load_history()
        for entry in past:
            self.history_list.addItem(entry)
