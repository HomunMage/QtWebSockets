from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QDockWidget
from PySide6.QtCore import Qt
from CustomGraphicsView import CanvasWidget
from MapView import MapView

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

        self.canvas = CanvasWidget()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.create_dock_widgets()

    def create_dock_widgets(self):
        self.map_view = MapView()
        self.dock_widget = QDockWidget("Map View", self)
        self.dock_widget.setWidget(self.map_view)
        self.dock_widget.setFloating(True)

        # Move the dock widget to the bottom-left corner of the screen
        screen_geometry = self.screen().geometry()
        screen_height = screen_geometry.height()
        self.dock_widget.move(0, screen_height - 200)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_widget)
