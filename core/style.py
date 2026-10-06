import os

_ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
_ICON_UP = _ICONS_DIR.replace("\\", "/") + "/up.svg"
_ICON_DOWN = _ICONS_DIR.replace("\\", "/") + "/down.svg"
_ICON_CHECK = _ICONS_DIR.replace("\\", "/") + "/check.svg"

COLORS = {
    "bg": "#1a1a2e",
    "card": "#16213e",
    "accent": "#e94560",
    "gold": "#f5c842",
    "text": "#eeeeee",
    "subtext": "#a8a8b3",
    "success": "#4CAF50",
    "warning": "#FF9800",
    "border": "#2a2a4a",
    "green": "#4ECDC4",
    "blue": "#54A0FF",
}


MAIN_STYLE = f"""
* {{
    font-family: "微软雅黑", "Microsoft YaHei", sans-serif;
}}

QMainWindow {{
    background-color: {COLORS["bg"]};
}}

QWidget#central {{
    background-color: {COLORS["bg"]};
}}

QLabel {{
    color: {COLORS["text"]};
    background: transparent;
}}

QLabel#title_label {{
    font-size: 36px;
    font-weight: bold;
    color: {COLORS["gold"]};
}}

QLabel#config_label {{
    font-size: 16px;
    color: {COLORS["subtext"]};
}}

QLabel#config_label_value {{
    font-size: 18px;
    font-weight: bold;
    color: {COLORS["gold"]};
}}

QLabel#result_label {{
    font-size: 42px;
    font-weight: bold;
    color: {COLORS["accent"]};
    padding: 20px 40px;
}}

QLabel#result_label_multi {{
    font-size: 28px;
    font-weight: bold;
    color: {COLORS["accent"]};
    padding: 20px 40px;
}}

QLabel#status_label {{
    font-size: 14px;
    color: {COLORS["subtext"]};
}}

QLabel#section_label {{
    font-size: 13px;
    color: {COLORS["subtext"]};
}}

QPushButton {{
    background-color: {COLORS["accent"]};
    color: white;
    border: none;
    border-radius: 20px;
    padding: 10px 25px;
    font-size: 14px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #c0392b;
}}

QPushButton:pressed {{
    background-color: #a83350;
}}

QPushButton:disabled {{
    background-color: #3a3a5a;
    color: #666;
}}

QPushButton#accent_btn {{
    background-color: {COLORS["accent"]};
}}

QPushButton#start_btn {{
    background-color: {COLORS["accent"]};
    border-radius: 25px;
    padding: 15px 50px;
    font-size: 18px;
}}

QPushButton#green_btn {{
    background-color: {COLORS["green"]};
}}
QPushButton#green_btn:hover {{
    background-color: #38b2ac;
}}

QPushButton#blue_btn {{
    background-color: {COLORS["blue"]};
}}
QPushButton#blue_btn:hover {{
    background-color: #3b8dd1;
}}

QPushButton#ghost_btn {{
    background-color: transparent;
    color: {COLORS["subtext"]};
    border: 1px solid {COLORS["border"]};
}}
QPushButton#ghost_btn:hover {{
    color: {COLORS["text"]};
    border-color: {COLORS["accent"]};
}}

QPushButton#danger_btn {{
    background-color: transparent;
    color: {COLORS["accent"]};
    border: 1px solid {COLORS["accent"]};
}}
QPushButton#danger_btn:hover {{
    background-color: rgba(233, 69, 96, 0.15);
}}

QPushButton#gold_btn {{
    background-color: transparent;
    color: {COLORS["gold"]};
    border: 1px solid {COLORS["gold"]};
}}
QPushButton#gold_btn:hover {{
    background-color: rgba(245, 200, 66, 0.1);
}}

QSpinBox {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 6px 15px;
    font-size: 14px;
    min-height: 24px;
}}
QSpinBox:focus {{
    border: 1px solid {COLORS["accent"]};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    border: none;
    width: 18px;
    background: transparent;
}}
QSpinBox::up-button:hover {{
    background-color: rgba(233, 69, 96, 0.2);
    border-top-right-radius: 12px;
}}
QSpinBox::down-button:hover {{
    background-color: rgba(233, 69, 96, 0.2);
    border-bottom-right-radius: 12px;
}}
QSpinBox::up-arrow {{
    image: url({_ICON_UP});
    width: 10px;
    height: 10px;
}}
QSpinBox::down-arrow {{
    image: url({_ICON_DOWN});
    width: 10px;
    height: 10px;
}}

QCheckBox {{
    color: {COLORS["text"]};
    font-size: 14px;
    spacing: 10px;
}}
QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 6px;
    border: 2px solid {COLORS["border"]};
    background-color: {COLORS["card"]};
}}
QCheckBox::indicator:hover {{
    border: 2px solid {COLORS["accent"]};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS["accent"]};
    border: 2px solid {COLORS["accent"]};
    image: url({_ICON_CHECK});
}}

QFrame#card_frame {{
    background-color: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 15px;
}}

QFrame#info_frame {{
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}}
"""


DIALOG_STYLE = f"""
QDialog {{
    background-color: {COLORS["bg"]};
}}

QLabel {{
    color: {COLORS["text"]};
    background: transparent;
}}

QLabel#dialog_title {{
    font-size: 22px;
    font-weight: bold;
    color: {COLORS["gold"]};
}}

QLabel#group_label {{
    font-size: 15px;
    font-weight: bold;
    color: {COLORS["gold"]};
}}

QLabel#selected_info {{
    font-size: 14px;
    color: {COLORS["accent"]};
    font-weight: bold;
}}

QLineEdit {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 8px 15px;
    font-size: 14px;
    selection-background-color: {COLORS["accent"]};
}}
QLineEdit:focus {{
    border: 1px solid {COLORS["accent"]};
}}

QListWidget {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 5px;
    font-size: 14px;
}}
QListWidget::item {{
    padding: 6px 10px;
    border-radius: 8px;
    color: {COLORS["text"]};
}}
QListWidget::item:selected {{
    background-color: {COLORS["accent"]};
    color: white;
}}
QListWidget::item:hover {{
    background-color: rgba(233, 69, 96, 0.2);
}}

QPushButton {{
    background-color: {COLORS["accent"]};
    color: white;
    border: none;
    border-radius: 18px;
    padding: 9px 22px;
    font-size: 14px;
    font-weight: bold;
}}
QPushButton:hover {{
    background-color: #c0392b;
}}
QPushButton:disabled {{
    background-color: #3a3a5a;
    color: #666;
}}

QPushButton#green_btn {{
    background-color: {COLORS["green"]};
}}
QPushButton#green_btn:hover {{
    background-color: #38b2ac;
}}

QPushButton#blue_btn {{
    background-color: {COLORS["blue"]};
}}
QPushButton#blue_btn:hover {{
    background-color: #3b8dd1;
}}

QPushButton#ghost_btn {{
    background-color: transparent;
    color: {COLORS["subtext"]};
    border: 1px solid {COLORS["border"]};
}}
QPushButton#ghost_btn:hover {{
    color: {COLORS["text"]};
    border-color: {COLORS["accent"]};
}}

QPushButton#danger_btn {{
    background-color: transparent;
    color: {COLORS["accent"]};
    border: 1px solid {COLORS["accent"]};
}}
QPushButton#danger_btn:hover {{
    background-color: rgba(233, 69, 96, 0.15);
}}

QPushButton#gold_btn {{
    background-color: transparent;
    color: {COLORS["gold"]};
    border: 1px solid {COLORS["gold"]};
}}
QPushButton#gold_btn:hover {{
    background-color: rgba(245, 200, 66, 0.1);
}}

QCheckBox {{
    color: {COLORS["text"]};
    font-size: 14px;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 2px solid {COLORS["border"]};
    background-color: {COLORS["card"]};
}}
QCheckBox::indicator:hover {{
    border: 2px solid {COLORS["accent"]};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS["accent"]};
    border: 2px solid {COLORS["accent"]};
    image: url({_ICON_CHECK});
}}

QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}

QScrollBar:vertical {{
    background-color: {COLORS["card"]};
    width: 12px;
    border-radius: 6px;
    margin: 4px;
}}
QScrollBar::handle:vertical {{
    background-color: {COLORS["border"]};
    border-radius: 6px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {COLORS["accent"]};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QTabWidget::pane {{
    background-color: {COLORS["card"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    top: -1px;
}}

QTabBar::tab {{
    background-color: {COLORS["bg"]};
    color: {COLORS["subtext"]};
    padding: 10px 25px;
    margin-right: 5px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-size: 13px;
    font-weight: bold;
}}
QTabBar::tab:selected {{
    background-color: {COLORS["card"]};
    color: {COLORS["gold"]};
}}
QTabBar::tab:hover {{
    color: {COLORS["text"]};
}}

QComboBox {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 6px 15px;
    font-size: 14px;
    min-height: 22px;
}}
QComboBox:focus {{
    border: 1px solid {COLORS["accent"]};
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    selection-background-color: {COLORS["accent"]};
    selection-color: white;
    outline: 0;
}}

QSpinBox {{
    background-color: {COLORS["card"]};
    color: {COLORS["text"]};
    border: 1px solid {COLORS["border"]};
    border-radius: 12px;
    padding: 6px 15px;
    font-size: 14px;
    min-height: 22px;
}}
QSpinBox:focus {{
    border: 1px solid {COLORS["accent"]};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    border: none;
    width: 16px;
}}

QMessageBox {{
    background-color: {COLORS["bg"]};
}}
QMessageBox QLabel {{
    color: {COLORS["text"]};
}}
QMessageBox QPushButton {{
    min-width: 80px;
}}
"""