# CustomGraphicsView.py

from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtCore import QObject, QPointF, QTimer
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWebSockets import QWebSocketServer, QWebSocket
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
        elif parts[0] == 'add':
            x = int(parts[2])
            y = int(parts[3])
            self.widget.square_pos = QPointF(x, y)
            self.widget.update()
            self.send_drawing_command()
        elif parts[0] == 'remove':
            self.widget.square_pos = QPointF(-100, -100)  # Move it out of view for "removal"
            self.widget.update()
            self.send_drawing_command()

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, main_window):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self._dragging = False
        self._last_mouse_pos = QPointF()
        self.main_window = main_window  # Reference to the MainWindow

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self._last_mouse_pos = event.pos()
            item = self.itemAt(event.pos())
            self.show_context_menu(event.pos(), item)
        else:
            super().mousePressEvent(event)

    def show_context_menu(self, position, item):
        context_menu = QMenu(self)
        scene_position = self.mapToScene(position)

        if item:  # If clicked on an item (node)
            remove_action = QAction("Remove Node", self)
            remove_action.triggered.connect(self.remove_node)
            context_menu.addAction(remove_action)
        else:  # If clicked on the canvas
            add_action = QAction("Add Node", self)
            add_action.triggered.connect(lambda: self.add_node(scene_position))
            context_menu.addAction(add_action)

        context_menu.exec(self.mapToGlobal(position))

    def add_node(self, position):
        self.widget.square_pos = position
        self.widget.update()  # Update the widget immediately
        self.server.send_drawing_command()  # Send the updated drawing command immediately

    def remove_node(self):
        self.widget.square_pos = QPointF(-100, -100)  # Move it out of view for "removal"
        self.widget.update()  # Update the widget immediately
        self.server.send_drawing_command()  # Send the updated drawing command immediately

    def update_map_view(self):
        rect = self.scene().sceneRect()
        pixmap = QPixmap(int(rect.width()), int(rect.height()))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()
        self.main_window.map_view.update_map(pixmap)  # Update the map view in the MainWindow
