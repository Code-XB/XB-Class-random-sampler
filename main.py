import sys
from PySide6.QtWidgets import QApplication
from core.ui import MainWindow
from core.config import migrate_legacy


def main():
    migrate_legacy()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()