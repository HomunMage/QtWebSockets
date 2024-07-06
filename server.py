import sys
import signal
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PySide6.QtCore import QObject, QTimer, QThread, QPointF
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QComboBox, QVBoxLayout
from PySide6.QtWebSockets import QWebSocketServer, QWebSocket
from PySide6.QtNetwork import QHostAddress

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)
        self.square_pos = QPointF(50, 50)
        self.square_size = (100, 100)
        self.text = "Start"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.square_pos.x(), self.square_pos.y(), self.square_size[0], self.square_size[1])

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.square_pos.x() + 25, self.square_pos.y() + 60, self.text)

    def get_drawing_command(self):
        return f"draw square {self.square_pos.x()} {self.square_pos.y()} {self.square_size[0]} {self.square_size[1]} {self.text}"

class WebSocketServer(QObject):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.server = QWebSocketServer("Qt WebSocket Server", QWebSocketServer.NonSecureMode, self)
        if not self.server.listen(QHostAddress.Any, 8000):
            print("Error: Unable to start the server.")
            sys.exit(-1)
        self.server.newConnection.connect(self.on_new_connection)
        self.clients = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_drawing_command)
        self.timer.start(1000)  # Send commands every 1000 ms

    def on_new_connection(self):
        client = self.server.nextPendingConnection()
        client.textMessageReceived.connect(lambda msg: self.process_message(client, msg))
        client.disconnected.connect(lambda: self.on_client_disconnected(client))
        self.clients.append(client)

    def on_client_disconnected(self, client):
        self.clients.remove(client)

    def send_drawing_command(self):
        command = self.widget.get_drawing_command()
        for client in self.clients:
            client.sendTextMessage(command)

    def process_message(self, client, message):
        parts = message.split(' ')
        if parts[0] == 'move':
            x = int(parts[1])
            y = int(parts[2])
            self.widget.square_pos = QPointF(x, y)
            self.widget.update()  # Update the widget immediately
            self.send_drawing_command()  # Send the updated drawing command immediately

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 300)

        self.layout = QVBoxLayout()

        self.type_layout = QHBoxLayout()
        self.type_label = QLabel("Node:")
        self.type_combo = QComboBox()
        self.type_combo.addItem("Square")
        self.type_layout.addWidget(self.type_label)
        self.type_layout.addWidget(self.type_combo)

        self.layout.addLayout(self.type_layout)

        self.canvas = CanvasWidget()
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)

class HTTPServerThread(QThread):
    def run(self):
        handler = SimpleHTTPRequestHandler
        httpd = HTTPServer(('localhost', 8000), handler)
        httpd.serve_forever()

def signal_handler(sig, frame):
    print("Interrupt received, shutting down...")
    QApplication.quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.hide()  # Hide the main window
    server = WebSocketServer(main_window.canvas)

    timer = QTimer()
    timer.start(100)  # Fire every 100ms
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 100ms

    sys.exit(app.exec())
