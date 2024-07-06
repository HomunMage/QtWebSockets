from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtCore import QObject, QPointF, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress
import sys

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
