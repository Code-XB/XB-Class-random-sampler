from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from .style import DIALOG_STYLE


class HistoryDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("历史记录")
        self.setStyleSheet(DIALOG_STYLE)
        self.resize(600, 600)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.config = config
        self._build_ui()
        self._load_history()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        title = QLabel("抽取历史记录")
        title.setObjectName("dialog_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: 1px solid #2a2a4a; border-radius: 12px; background-color: #16213e; }")
        self.scroll_content = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(15, 15, 15, 15)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()
        scroll.setWidget(self.scroll_content)
        layout.addWidget(scroll, 1)

        btn_row = QHBoxLayout()
        clear_btn = QPushButton("清空全部记录")
        clear_btn.setObjectName("danger_btn")
        clear_btn.clicked.connect(self._clear_all)
        btn_row.addWidget(clear_btn)
        btn_row.addStretch()

        close_btn = QPushButton("关闭")
        close_btn.setObjectName("ghost_btn")
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _load_history(self):
        history = self.config.get("history", [])
        if not history:
            empty = QLabel("暂无抽取记录")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #a8a8b3; font-size: 14px; padding: 40px;")
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, empty)
            return

        for day_entry in reversed(history):
            date_frame = QFrame()
            date_frame.setStyleSheet(
                "QFrame { background-color: rgba(255,255,255,0.03); border-radius: 10px; padding: 10px; }"
            )
            date_layout = QVBoxLayout(date_frame)
            date_layout.setContentsMargins(15, 10, 15, 10)
            date_layout.setSpacing(6)

            date_label = QLabel(f"{day_entry.get('date', '')}")
            date_label.setStyleSheet("color: #f5c842; font-weight: bold; font-size: 15px;")
            date_layout.addWidget(date_label)

            for record in reversed(day_entry.get("records", [])):
                time_str = record.get("time", "")
                names = record.get("names", [])
                names_text = "、".join(names)
                record_label = QLabel(f"  {time_str}  |  {names_text}")
                record_label.setStyleSheet("color: #eeeeee; font-size: 14px; padding: 4px 0;")
                record_label.setWordWrap(True)
                date_layout.addWidget(record_label)

            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, date_frame)

    def _clear_all(self):
        ret = QMessageBox.warning(
            self, "确认",
            "即将清空全部历史记录！\n此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        from .config import save_history
        save_history(self.config["name"], [])
        self.config["history"] = []
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._load_history()