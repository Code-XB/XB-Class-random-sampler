import random
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QCheckBox, QMessageBox, QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from .style import MAIN_STYLE
from .config import (
    ensure_default_config, load_config, save_cfg,
    append_history, reset_round_extracted, get_all_students_from_config
)
from .student_dialog import StudentDialog
from .history_dialog import HistoryDialog
from .settings_dialog import SettingsDialog
from .utils import get_random_color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("随机抽取器")
        self.resize(820, 620)
        self.setStyleSheet(MAIN_STYLE)

        self.current_config_name = ensure_default_config()
        self.config = load_config(self.current_config_name)
        self.is_animating = False
        self._setup_ui()
        self._refresh_config_display()

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(30, 20, 30, 20)
        root.setSpacing(15)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        config_label = QLabel("当前配置：")
        config_label.setObjectName("config_label")
        top_row.addWidget(config_label)

        self.config_label_value = QLabel("")
        self.config_label_value.setObjectName("config_label_value")
        top_row.addWidget(self.config_label_value)

        top_row.addStretch()

        count_label = QLabel("抽取数量：")
        count_label.setObjectName("config_label")
        top_row.addWidget(count_label)

        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 42)
        self.count_spin.setValue(1)
        self.count_spin.valueChanged.connect(self._on_count_changed)
        top_row.addWidget(self.count_spin)

        dedup_label = QLabel("去重抽取")
        dedup_label.setObjectName("config_label")
        top_row.addWidget(dedup_label)

        self.dedup_check = QCheckBox()
        self.dedup_check.setChecked(True)
        self.dedup_check.stateChanged.connect(self._on_dedup_changed)
        top_row.addWidget(self.dedup_check)

        root.addLayout(top_row)

        title = QLabel("随机抽取同学")
        title.setObjectName("title_label")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        result_card = QFrame()
        result_card.setObjectName("card_frame")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(20, 15, 20, 15)
        result_layout.setSpacing(5)

        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_scroll.setStyleSheet(
            "QScrollArea { border: none; background: transparent; }"
            "QScrollBar:vertical { background: #16213e; width: 10px; border-radius: 5px; margin: 2px; }"
            "QScrollBar::handle:vertical { background: #2a2a4a; border-radius: 5px; min-height: 20px; }"
            "QScrollBar::handle:vertical:hover { background: #e94560; }"
            "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }"
        )

        result_container = QWidget()
        result_inner = QVBoxLayout(result_container)
        result_inner.setContentsMargins(10, 10, 10, 10)

        self.result_label = QLabel("点击开始抽取")
        self.result_label.setObjectName("result_label")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.NoTextInteraction)
        result_inner.addWidget(self.result_label)
        result_inner.addStretch()

        result_scroll.setWidget(result_container)
        result_layout.addWidget(result_scroll, 1)

        self.status_label = QLabel("准备就绪")
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setContentsMargins(0, 5, 0, 10)
        result_layout.addWidget(self.status_label)

        root.addWidget(result_card, 1)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        select_btn = QPushButton("选择学生")
        select_btn.setObjectName("green_btn")
        select_btn.clicked.connect(self._open_select_students)
        action_row.addWidget(select_btn)

        history_btn = QPushButton("历史记录")
        history_btn.setObjectName("blue_btn")
        history_btn.clicked.connect(self._open_history)
        action_row.addWidget(history_btn)

        settings_btn = QPushButton("设置")
        settings_btn.setObjectName("ghost_btn")
        settings_btn.clicked.connect(self._open_settings)
        action_row.addWidget(settings_btn)

        action_row.addStretch()

        clear_btn = QPushButton("清空")
        clear_btn.setObjectName("ghost_btn")
        clear_btn.clicked.connect(self._clear_round)
        action_row.addWidget(clear_btn)

        start_btn = QPushButton("开始抽取")
        start_btn.setObjectName("start_btn")
        start_btn.clicked.connect(self._start_draw)
        action_row.addWidget(start_btn)

        root.addLayout(action_row)

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()
        copyright_text = self._load_copyright()
        version = QLabel(copyright_text)
        version.setStyleSheet("color: #666; font-size: 11px;")
        bottom_row.addWidget(version)
        root.addLayout(bottom_row)

        self._init_spin_range()

    def _load_copyright(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "copyright.txt")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text:
                        return text
        except Exception:
            pass
        return "v3.1.1  |  © 2026 CodeXB"

    def _refresh_config_display(self):
        self.config_label_value.setText(self.current_config_name)
        self._init_spin_range()
        self._update_status()
        cfg = self.config["cfg"]
        self.count_spin.blockSignals(True)
        self.count_spin.setValue(cfg.get("extract_count", 1))
        self.count_spin.blockSignals(False)
        self.dedup_check.blockSignals(True)
        self.dedup_check.setChecked(cfg.get("dedup", True))
        self.dedup_check.blockSignals(False)

    def _init_spin_range(self):
        total = len(get_all_students_from_config(self.config))
        if total <= 0:
            total = 1
        self.count_spin.setRange(1, total)

    def _on_count_changed(self, val):
        self.config["cfg"]["extract_count"] = val
        save_cfg(self.current_config_name, self.config["cfg"])
        self._update_status()

    def _on_dedup_changed(self, state):
        self.config["cfg"]["dedup"] = bool(state)
        save_cfg(self.current_config_name, self.config["cfg"])

    def _update_status(self):
        cfg = self.config["cfg"]
        selected = cfg.get("selected_students", "all")
        dedup = cfg.get("dedup", True)
        count = self.count_spin.value()
        extracted_count = len(cfg.get("extracted_this_round", []))

        if selected == "all":
            scope_text = "全班"
        else:
            scope_text = f"已选 {len(selected)} 人"

        dedup_text = f"（去重：已抽 {extracted_count} 人）" if dedup and extracted_count > 0 else ""
        self.status_label.setText(
            f"抽取范围：{scope_text}  |  数量：{count}  |  {'去重' if dedup else '可重复'}{dedup_text}"
        )

    def _get_draw_pool(self):
        cfg = self.config["cfg"]
        selected = cfg.get("selected_students", "all")
        dedup = cfg.get("dedup", True)
        extracted = set(cfg.get("extracted_this_round", []))

        if selected == "all":
            pool = get_all_students_from_config(self.config)
        else:
            all_names = set(get_all_students_from_config(self.config))
            pool = [s for s in selected if s in all_names]

        if dedup and extracted:
            pool = [s for s in pool if s not in extracted]

        return pool

    def _start_draw(self):
        if self.is_animating:
            return

        pool = self._get_draw_pool()
        if not pool:
            QMessageBox.warning(
                self, "无法抽取",
                "没有可抽取的同学！\n"
                "如果是去重模式，可能本轮已抽完全部。\n"
                "请点击「清空」重开一轮。"
            )
            return

        count = self.count_spin.value()
        if count > len(pool):
            count = len(pool)

        self.is_animating = True
        self.result_label.setStyleSheet(f"color: {get_random_color()};")
        self.result_label.setFont(QFont("微软雅黑", 24))

        self._animation_rounds = random.randint(15, 25)
        self._animation_pool = pool
        self._animation_index = 0
        self._animation_count = count
        self._anim_timer = QTimer()
        self._anim_timer.timeout.connect(self._animation_tick)
        self._anim_timer.start(70)

    def _animation_tick(self):
        if self._animation_index < self._animation_rounds:
            temp = random.choice(self._animation_pool)
            self.result_label.setText(temp)
            self.result_label.setStyleSheet(f"color: {get_random_color()};")
            self._animation_index += 1
        else:
            self._anim_timer.stop()
            self._show_result()

    def _show_result(self):
        pool = self._animation_pool
        count = self._animation_count

        if self.config["cfg"].get("dedup", True):
            result = random.sample(pool, count)
        else:
            result = [random.choice(pool) for _ in range(count)]

        self.config["cfg"].setdefault("extracted_this_round", [])
        self.config["cfg"]["extracted_this_round"].extend(result)
        save_cfg(self.current_config_name, self.config["cfg"])
        append_history(self.current_config_name, result)

        self.config = load_config(self.current_config_name)

        if count == 1:
            name = result[0]
            self.result_label.setText(f"恭喜 {name} 同学！")
            self.result_label.setObjectName("result_label")
            self.result_label.setStyleSheet("color: #FF0000; font-weight: bold;")
            self.result_label.setFont(QFont("微软雅黑", 22, QFont.Bold))
        else:
            names_text = "、".join(result)
            self.result_label.setObjectName("result_label_multi")
            self.result_label.setStyleSheet("color: #FF0000; font-weight: bold;")
            self.result_label.setFont(QFont("微软雅黑", 18, QFont.Bold))
            self.result_label.setText(names_text)

        self.is_animating = False
        self._update_status()

    def _open_select_students(self):
        if self.is_animating:
            return
        dlg = StudentDialog(self.config, self)
        if dlg.exec() == dlg.Accepted:
            self.config = load_config(self.current_config_name)
            self._init_spin_range()
            self._update_status()

    def _open_history(self):
        HistoryDialog(self.config, self).exec()

    def _open_settings(self):
        if self.is_animating:
            return
        dlg = SettingsDialog(self.current_config_name, self)
        dlg.config_changed.connect(self._on_config_changed)
        dlg.exec()

    def _on_config_changed(self, new_name):
        self.current_config_name = new_name
        self.config = load_config(new_name)
        self._refresh_config_display()

    def _clear_round(self):
        if self.is_animating:
            return
        reset_round_extracted(self.config)
        self.config = load_config(self.current_config_name)
        self.result_label.setText("点击开始抽取")
        self.result_label.setObjectName("result_label")
        self.result_label.setStyleSheet("")
        self.result_label.setFont(QFont("微软雅黑", 22))
        self._update_status()