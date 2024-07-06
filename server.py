import sys
from PySide6.QtCore import QObject, QCoreApplication, QTimer, QByteArray
from PySide6.QtWebSockets import QWebSocketServer, QWebSocket
from PySide6.QtNetwork import QHostAddress
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QApplication, QWidget

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(50, 50, 100, 100)
        
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(75, 110, "Start")

    def get_drawing_command(self):
        return "draw square 50 50 100 100 Start"

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
        client.disconnected.connect(lambda: self.on_client_disconnected(client))
        self.clients.append(client)

    def on_client_disconnected(self, client):
        self.clients.remove(client)

    def send_drawing_command(self):
        command = self.widget.get_drawing_command()
        for client in self.clients:
            client.sendTextMessage(command)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CanvasWidget()
    server = WebSocketServer(widget)
    sys.exit(app.exec())
