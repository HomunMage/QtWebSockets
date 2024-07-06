# CanvasWidget.py

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QPoint
from Node import Node

class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 200, 200)
        self.node = Node(50, 50, (100, 100), "Start")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.node.pos.x(), self.node.pos.y(), self.node.size[0], self.node.size[1])

        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.node.pos.x() + 25, self.node.pos.y() + 60, self.node.text)

    def get_drawing_command(self):
        return f'draw {self.node.pos.x()} {self.node.pos.y()} {self.node.size[0]} {self.node.text}'

    def handle_mousedown(self, button, x, y):
        if button == 'left':
            if self.node.contains(x, y):
                self.node.dragging = True
                self.node.drag_offset = QPoint(x - self.node.pos.x(), y - self.node.pos.y())
        elif button == 'right':
            # Handle right-click if necessary
            pass

    def handle_mouseup(self, x, y):
        self.node.dragging = False

    def handle_mousemove(self, x, y):
        if self.node.dragging:
            self.node.move(x - self.node.drag_offset.x(), y - self.node.drag_offset.y())
            self.update()  # Update the widget immediately
