from PySide6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QApplication
from PySide6.QtGui import QPainter, QPainterPath, QColor, QBrush
from PySide6.QtCore import Qt, QSize

class LeftArrowButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(30, 30))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.moveTo(25, 5)
        path.lineTo(5, 15)
        path.lineTo(25, 25)
        path.lineTo(25, 5)

        brush = QBrush(QColor("#000000"))
        painter.fillPath(path, brush)
        painter.drawPath(path)

        painter.end()
