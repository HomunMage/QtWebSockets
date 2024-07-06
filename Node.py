# Node.py

from PySide6.QtCore import QPointF

class Node:
    def __init__(self, x, y, size, text):
        self.pos = QPointF(x, y)
        self.size = size
        self.text = text

    def move(self, x, y):
        self.pos = QPointF(x, y)

    def get_drawing_command(self):
        return f"draw square {self.pos.x()} {self.pos.y()} {self.size[0]} {self.size[1]} {self.text}"
