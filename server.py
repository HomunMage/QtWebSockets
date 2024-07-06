# server.py

import sys
import signal
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from MainWindow import MainWindow
from WebSocketServer import WebSocketServer

def signal_handler(sig, frame):
    print("Interrupt received, shutting down...")
    QApplication.quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.hide()  # Hide the main window
    server = WebSocketServer(main_window.canvas_widget)

    timer = QTimer()
    timer.start(100)  # Fire every 100ms
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 100ms

    sys.exit(app.exec())

