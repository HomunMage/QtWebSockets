# CustomGraphicsView.py

from PySide6.QtWidgets import QGraphicsView, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QPointF
from Node import Node

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, widget):
        super().__init__(scene)
        self.setDragMode(QGraphicsView.NoDrag)
        self.widget = widget

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())
        else:
            super().mouseReleaseEvent(event)

    def show_context_menu(self, position):
        self.right_click_position = self.mapToScene(position)
        context_menu = QMenu(self)

        add_node_action = QAction("Add Node", self)
        add_node_action.triggered.connect(lambda: self.add_node(self.right_click_position))
        context_menu.addAction(add_node_action)

        item = self.itemAt(position)
        if item:  # If clicked on an item (node)
            remove_action = QAction("Remove Node", self)
            remove_action.triggered.connect(self.remove_node)
            context_menu.addAction(remove_action)

        context_menu.exec(self.mapToGlobal(position))

    def add_node(self, position):
        new_node = Node(position.x(), position.y(), (100, 100), "New Node")
        self.widget.nodes.append(new_node)
        self.widget.update()  # Update the widget immediately
        self.widget.get_drawing_command()  # Send the updated drawing command immediately

    def remove_node(self):
        if self.widget.nodes:
            self.widget.nodes.pop()  # Remove the last node for simplicity
        self.widget.update()  # Update the widget immediately
        self.widget.get_drawing_command()  # Send the updated drawing command immediately
