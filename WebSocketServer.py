# WebSocketServer.py

from PySide6.QtCore import QObject, QTimer
from PySide6.QtWebSockets import QWebSocketServer
from PySide6.QtNetwork import QHostAddress
import sys

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
        command = parts[0]
        if command == 'mousedown':
            button = parts[1]
            x = int(parts[2])
            y = int(parts[3])
            self.widget.handle_mousedown(button, x, y)
        elif command == 'mouseup':
            x = int(parts[1])
            y = int(parts[2])
            self.widget.handle_mouseup(x, y)
        elif command == 'mousemove':
            x = int(parts[1])
            y = int(parts[2])
            self.widget.handle_mousemove(x, y)
        self.send_drawing_command()
