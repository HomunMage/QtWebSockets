# app.py
import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Web Browser")

        self.browser = QWebEngineView()
        self.browser.setUrl("http://localhost:8000")

        # Set the window size and position off-screen to hide it
        self.setGeometry(-10000, -10000, 800, 600)
        
        self.setCentralWidget(self.browser)

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    
    # Hide the window
    window.hide()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
