# app.py

import sys
import signal
from PySide6.QtCore import QCoreApplication, QTimer, QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView

class BrowserWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("PySide6 Web Browser")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))

        # Set the window size and position off-screen to hide it
        self.setGeometry(-10000, -10000, 800, 600)
        
        self.setCentralWidget(self.browser)
        
        # Store the URL
        self.url = url

def signal_handler(signum, frame):
    QCoreApplication.quit()

def main():
    app = QApplication(sys.argv)
    
    # Set up signal handling
    signal.signal(signal.SIGINT, signal_handler)
    
    url = "http://localhost:8000"
    window = BrowserWindow(url)
    window.show()
    
    # Hide the window
    window.hide()
    
    # Print the URL to hint the user
    print(f"Browser is running at: {window.url}")
    
    # Create a timer to process Python events
    timer = QTimer()
    timer.start(100)  # Fire every 100ms
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 100ms
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
