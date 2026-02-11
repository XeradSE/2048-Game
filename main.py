import sys, mainwindow
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()