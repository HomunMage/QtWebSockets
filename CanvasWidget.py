# CanvasWidget.py

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPoint
from Node import Node

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)
        self.nodes = [
            Node(50, 50, (100, 100), "Start"),
            Node(100, 150, (100, 100), "End")
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        for node in self.nodes:
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(node.pos.x(), node.pos.y(), node.size[0], node.size[1])

            painter.setPen(QColor(255, 255, 255))
            painter.drawText(node.pos.x() + 25, node.pos.y() + 60, node.text)

    def get_drawing_command(self):
        commands = []
        for node in self.nodes:
            commands.append(f'draw {node.pos.x()} {node.pos.y()} {node.size[0]} {node.size[1]} {node.text}')
        return ' | '.join(commands)

    def handle_mousedown(self, button, x, y):
        if button == 'left':
            for node in self.nodes:
                if node.contains(x, y):
                    node.dragging = True
                    node.drag_offset = QPoint(x - node.pos.x(), y - node.pos.y())
                    break
        elif button == 'right':
            pass

    def handle_mouseup(self, x, y):
        for node in self.nodes:
            node.dragging = False

    def handle_mousemove(self, x, y):
        for node in self.nodes:
            if node.dragging:
                node.move(x - node.drag_offset.x(), y - node.drag_offset.y())
                self.update()  # Update the widget immediately
