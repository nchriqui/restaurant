from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QPainterPath, QColor, QPen, QBrush
import sys

class HeartCheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)  # Set the desired size of the checkbox
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        
        if self.isChecked():
            brush = QBrush(QColor(255, 0, 0))
        else:
            brush = QBrush(QColor(255, 255, 255))
        
        painter.setBrush(brush)
        
        # Create the heart shape using QPainterPath
        path = QPainterPath()
        path.moveTo(10, 5)
        path.cubicTo(15, 0, 20, 0, 20, 5)
        path.cubicTo(20, 5, 20, 10, 10, 20)
        path.cubicTo(10, 20, 0, 10, 0, 5)
        path.cubicTo(0, 0, 5, 0, 10, 5)
        
        painter.drawPath(path)
    
    def sizeHint(self):
        return QSize(30, 30)
