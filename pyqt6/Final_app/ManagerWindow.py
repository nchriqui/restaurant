import csv
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser
from PyQt6.QtGui import QPainter, QColor, QBrush, QFont, QPainterPath, QPainterPathStroker
from PyQt6.QtCore import Qt, QTimer, QRect, QPointF
from manager_appli import *

def generateColors(num_colors):
    colors = []
    for _ in range(num_colors):
        color = QColor(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
        colors.append(color)
    return colors

class RestaurantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.table_colors = [QColor(Qt.GlobalColor.green)] * 4  # Initialize all tables as green

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Tables
        table_size = 50
        table_margin = 40
        table_spacing = 150

        # Calculate the horizontal offset to center the tables
        total_width = 2 * table_margin + 2 * table_size + table_spacing
        horizontal_offset = (self.width() - total_width) // 2

        # Calculate the vertical offset to center the tables
        total_height = 2 * table_margin + 2 * table_size + table_spacing
        vertical_offset = (self.height() - total_height) // 2

        # First row
        painter.setBrush(QBrush(self.table_colors["1"]))
        painter.drawRect(horizontal_offset + table_margin, vertical_offset + table_margin, table_size, table_size)
        painter.setBrush(QBrush(self.table_colors["2"]))
        painter.drawRect(horizontal_offset + table_margin + table_size + table_spacing, vertical_offset + table_margin, table_size, table_size)

        # Second row
        painter.setBrush(QBrush(self.table_colors["3"]))
        painter.drawRect(horizontal_offset + table_margin, vertical_offset + table_margin + table_size + table_spacing, table_size, table_size)
        painter.setBrush(QBrush(self.table_colors["4"]))
        painter.drawRect(horizontal_offset + table_margin + table_size + table_spacing, vertical_offset + table_margin + table_size + table_spacing, table_size, table_size)

        # Labels
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(horizontal_offset + table_margin, vertical_offset + table_margin - 10, "Table 1")
        painter.drawText(horizontal_offset + table_margin + table_size + table_spacing, vertical_offset + table_margin - 10, "Table 2")
        painter.drawText(horizontal_offset + table_margin, vertical_offset + table_margin + table_size + table_spacing - 10, "Table 3")
        painter.drawText(horizontal_offset + table_margin + table_size + table_spacing, vertical_offset + table_margin + table_size + table_spacing - 10, "Table 4")

    def updateTableColors(self, table_colors):
        self.table_colors = table_colors
        self.update()  # Trigger a repaint

class PieChartWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.colors = generateColors(len(data))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Pie chart properties
        radius = min(self.width(), self.height()) / 2 - 20
        center = QPointF(self.rect().center())
        center.setX(center.x() + 50)
        total = sum(self.data.values())
        start_angle = 0

        # Draw each pie slice
        color_index = 0
        for label, value in self.data.items():
            angle = 360 * value / total

            # Create pie slice path
            path = QPainterPath()
            path.moveTo(center)
            path.arcTo(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius, start_angle, angle)
            path.lineTo(center)

            # Set pie slice color
            color = self.colors[color_index % len(self.colors)]
            painter.setBrush(QBrush(color))

            # Draw pie slice
            painter.drawPath(path)

            # Draw legend rectangle
            legend_rect = self.rect().adjusted(10, 10, -10, -10)
            rect_width = 15
            rect_height = 12
            rect_margin = 5

            legend_x = legend_rect.left()
            legend_y = legend_rect.top() + rect_height * list(self.data.keys()).index(label) 

            rect = QRect(legend_x, legend_y, rect_width, rect_height)
            painter.drawRect(rect)

            text_x = int(legend_x + rect_width + rect_margin)
            text_y = int(legend_y + rect_height / 2)

            # Alignement vertical du texte avec le carré de légende
            font_metrics = painter.fontMetrics()
            text_rect = font_metrics.boundingRect(label)
            text_height = text_rect.height()
            text_y += int((rect_height - text_height) / 2) + 6

            painter.drawText(text_x, text_y, label)

            start_angle += angle
            color_index += 1

class StatsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Example statistics
        self.labels = []
        self.text_browsers = []

        label_client = QLabel(f"Nombre de clients en salle")
        text_browser_client = QTextBrowser()
        text_browser_client.setMaximumHeight(25)

        layout.addWidget(label_client)
        layout.addWidget(text_browser_client)

        self.labels.append(label_client)
        self.text_browsers.append(text_browser_client)

        label_recipe = QLabel(f"Recette préférée des clients")
        favorite_recipe, favorite_count = get_most_favorite_recipe()
        text_browser_recipe = QTextBrowser()

        if favorite_recipe:
            text_browser_recipe.setText(f"{favorite_recipe} (Favoris: {favorite_count})")
        else:
            text_browser_recipe.setText("Aucune recette trouvée")
        
        text_browser_recipe.setMaximumHeight(25)

        layout.addWidget(label_recipe)
        layout.addWidget(text_browser_recipe)

        self.labels.append(label_recipe)
        self.text_browsers.append(text_browser_recipe)

        # Add pie chart for ingredients statistics
        type_data = get_ingredient_proportions()
        recipe_chart = PieChartWidget(type_data)
        recipe_chart.setMinimumSize(275, 150)  # Set the minimum size for the pie chart widget
        layout.addWidget(recipe_chart, alignment=Qt.AlignmentFlag.AlignHCenter)  # Add the pie chart widget to the layout

        # Add title label
        title_label = QLabel("Répartition des ingrédients des recettes")
        title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label)


        # Add pie chart forvcuisine statistics
        origine_data = get_cuisine_proportions()
        origine_chart = PieChartWidget(origine_data)
        origine_chart.setMinimumSize(275, 150)  # Set the minimum size for the pie chart widget
        layout.addWidget(origine_chart, alignment=Qt.AlignmentFlag.AlignHCenter)  # Add the pie chart widget to the layout

        # Add title label
        title_label_origine = QLabel("Répartition des origines des recettes")
        title_label_origine.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(title_label_origine)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(850, 400)
        self.setWindowTitle("Restaurant")

        main_widget = QWidget()
        layout = QHBoxLayout()

        self.restaurant_widget = RestaurantWidget()
        stats_widget = StatsWidget()

        layout.addWidget(self.restaurant_widget, 3)  # 3/4 width
        layout.addWidget(stats_widget, 1)  # 1/4 width

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Start the timer for table color updates
        file_path = "pyqt6/Final_app/table_colors.csv"  # Update with your CSV file path
        file_path_client = "pyqt6/Final_app/nb_clients.txt"  # Update with the actual file path
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.updateTableColors(readCSVFile(file_path)))
        self.timer.timeout.connect(lambda: self.updateClientCount(file_path_client))
        # self.timer.timeout.connect(lambda: self.updateFavoriteRecipe())
        self.timer.timeout.emit()
        self.timer.start(1000)  # Update every second

        self.favorite_recipe_timer = QTimer()
        self.favorite_recipe_timer.timeout.connect(lambda: self.updateFavoriteRecipe())
        self.favorite_recipe_timer.timeout.emit()
        self.favorite_recipe_timer.start(2000)  # Update every 2 seconds

    def updateTableColors(self, table_colors):
        self.restaurant_widget.updateTableColors(table_colors)
        print("update")

    def updateClientCount(self, file_path):
        with open(file_path, 'r') as file:
            client_count = int(file.read().strip())
        
        stats_widget = self.centralWidget().layout().itemAt(1).widget()
        stats_widget.text_browsers[0].setText(str(client_count))

    def updateFavoriteRecipe(self):
        favorite_recipe, favorite_count = get_most_favorite_recipe()
        stats_widget = self.centralWidget().layout().itemAt(1).widget()

        if favorite_recipe:
            stats_widget.text_browsers[1].setText(f"{favorite_recipe} (Favoris: {favorite_count})")
        else:
            stats_widget.text_browsers[1].setText("Aucune recette trouvée")


def readCSVFile(file_path):
    table_colors = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                table_name = row[0]
                table_state = row[1]
                color = QColor(Qt.GlobalColor.red) if table_state == '0' else QColor(Qt.GlobalColor.green)
                table_colors[table_name] = color
    return table_colors
