# MainWindow.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDockWidget, QGraphicsScene
from PySide6.QtCore import Qt
from CustomGraphicsView import CustomGraphicsView
from CanvasWidget import CanvasWidget

class MainWindow(QMainWindow):
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

        self.canvas_widget = CanvasWidget()
        self.scene = QGraphicsScene()
        self.graphics_view = CustomGraphicsView(self.scene, self)
        self.layout.addWidget(self.graphics_view)
        self.setLayout(self.layout)