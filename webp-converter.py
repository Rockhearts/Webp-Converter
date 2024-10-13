import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog, QProgressBar, QMessageBox, QSlider, QFrame, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PIL import Image

class ConvertThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, files, quality, lossless, keep_metadata, output_format):
        super().__init__()
        self.files = files
        self.quality = quality
        self.lossless = lossless
        self.keep_metadata = keep_metadata
        self.output_format = output_format

    def run(self):
        total = len(self.files)
        for i, file in enumerate(self.files, 1):
            try:
                if os.path.isdir(file):
                    self.convert_folder(file)
                elif os.path.isfile(file):
                    self.convert_file(file)
                self.progress.emit(int(i / total * 100))
            except Exception as e:
                self.error.emit(f"Error processing {file}: {str(e)}")
        self.finished.emit()

    def convert_file(self, file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                with Image.open(file_path) as img:
                    icc_profile = img.info.get('icc_profile')
                    try:
                        exif = img.info.get('exif', b'')
                        if exif is None:
                            exif = b''
                    except Exception as e:
                        print(f"Warning: Could not read EXIF data from {file_path}: {str(e)}")
                        exif = b''

                    # 出力ファイル名を決定
                    if self.output_format == "append":
                        webp_path = file_path + ".webp"
                    else:  # replace
                        webp_path = os.path.splitext(file_path)[0] + ".webp"

                    img.save(webp_path, 'webp', quality=self.quality, lossless=self.lossless, 
                             icc_profile=icc_profile, exif=exif, 
                             method=6)

                    if self.keep_metadata and not self.lossless and exif:
                        try:
                            with Image.open(webp_path) as webp_img:
                                webp_img.info['exif'] = exif
                                webp_img.save(webp_path, 'webp', quality=self.quality, 
                                              icc_profile=icc_profile, exif=exif)
                        except Exception as e:
                            print(f"Warning: Could not save metadata to {webp_path}: {str(e)}")

                print(f"Converted: {file_path} -> {webp_path}")
            except Exception as e:
                print(f"Error converting {file_path}: {str(e)}")

    def convert_folder(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                self.convert_file(file_path)

class DropArea(QLabel):
    dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                background-color: #f0f0f0;
                min-height: 150px;
            }
        """)
        self.setText("\n\nフォルダまたはファイルを\nここにドラッグ＆ドロップしてください\n\n")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        self.dropped.emit(files)

class WebPConverterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebP Converter")
        self.setGeometry(100, 100, 400, 500)  # ウィンドウの高さをさらに増やしました

        layout = QVBoxLayout()

        self.drop_area = DropArea()
        self.drop_area.dropped.connect(self.handle_dropped_files)
        layout.addWidget(self.drop_area)

        self.select_button = QPushButton("ファイルを選択", self)
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)

        # 出力形式の選択プルダウンを追加
        output_format_layout = QHBoxLayout()
        self.output_format_label = QLabel("出力形式:", self)
        self.output_format_combo = QComboBox(self)
        self.output_format_combo.addItem("元の拡張子 + .webp", "append")
        self.output_format_combo.addItem(".webpのみ", "replace")
        output_format_layout.addWidget(self.output_format_label)
        output_format_layout.addWidget(self.output_format_combo)
        layout.addLayout(output_format_layout)

        quality_layout = QHBoxLayout()
        self.quality_label = QLabel("品質: 95", self)
        self.quality_slider = QSlider(Qt.Horizontal, self)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(95)
        self.quality_slider.valueChanged.connect(self.update_quality_label)
        quality_layout.addWidget(self.quality_label)
        quality_layout.addWidget(self.quality_slider)
        layout.addLayout(quality_layout)

        self.lossless_checkbox = QCheckBox("ロスレス圧縮 (画質維持・ファイルサイズ大)", self)
        self.lossless_checkbox.stateChanged.connect(self.toggle_quality_settings)
        layout.addWidget(self.lossless_checkbox)

        self.metadata_checkbox = QCheckBox("メタデータを保持 (色情報を維持)", self)
        self.metadata_checkbox.setChecked(True)
        layout.addWidget(self.metadata_checkbox)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.files_to_convert = []

    def update_quality_label(self, value):
        self.quality_label.setText(f"品質: {value}")

    def toggle_quality_settings(self, state):
        self.quality_slider.setEnabled(not state)
        self.quality_label.setEnabled(not state)

    def handle_dropped_files(self, files):
        self.files_to_convert.extend(files)
        self.start_conversion()

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "ファイルを選択", "", "Images (*.png *.jpg *.jpeg *.gif)")
        if files:
            self.files_to_convert.extend(files)
            self.start_conversion()

    def start_conversion(self):
        if not self.files_to_convert:
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.drop_area.setText("変換中...")
        self.select_button.setEnabled(False)

        quality = self.quality_slider.value()
        lossless = self.lossless_checkbox.isChecked()
        keep_metadata = self.metadata_checkbox.isChecked()
        output_format = self.output_format_combo.currentData()
        self.convert_thread = ConvertThread(self.files_to_convert, quality, lossless, keep_metadata, output_format)
        self.convert_thread.progress.connect(self.update_progress)
        self.convert_thread.finished.connect(self.conversion_finished)
        self.convert_thread.error.connect(self.show_error)
        self.convert_thread.start()

        self.files_to_convert = []

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.progress_bar.setVisible(False)
        self.drop_area.setText("\n\nフォルダまたはファイルを\nここにドラッグ＆ドロップしてください\n\n")
        self.select_button.setEnabled(True)
        QMessageBox.information(self, "変換完了", "すべてのファイルがWebpに変換されました。")

    def show_error(self, error_message):
        QMessageBox.warning(self, "エラー", error_message)

def main():
    app = QApplication(sys.argv)
    window = WebPConverterWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()