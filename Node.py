# Node.py

from PySide6.QtCore import QPoint

class Node:
    def __init__(self, x, y, size, text):
        self.pos = QPoint(x, y)
        self.size = size
        self.text = text
        self.dragging = False
        self.drag_offset = QPoint(0, 0)

    def move(self, x, y):
        self.pos.setX(x)
        self.pos.setY(y)

    def contains(self, x, y):
        return (self.pos.x() <= x <= self.pos.x() + self.size[0] and
                self.pos.y() <= y <= self.pos.y() + self.size[1])

    def get_drawing_command(self):
        return f'draw {self.pos.x()} {self.pos.y()} {self.size[0]} {self.size[1]} {self.text}'
