import sys, time
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(400, 300)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)

    def draw_square(self, x, y, color):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(10)
        pen.setColor(QtGui.QColor(color[0], color[1], color[2]))
        painter.setPen(pen)
        painter.drawPoint(x, y)
        painter.end()
        print(1)

    def draw_pixels(self, pixels):
        for i in range(len(pixels[0])):
            print([pixels[0][i], pixels[1][i], pixels[2][i]])
            self.draw_square(i * 11, 150, [pixels[0][i], pixels[1][i], pixels[2][i]])

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()

number_of_pixels = 20
pixels = np.tile(1, (3, number_of_pixels))
pixels[0, 0] = 255  # Set 1st pixel red
pixels[1, 1] = 255  # Set 2nd pixel green
pixels[2, 2] = 255  # Set 3rd pixel blue

window.draw_pixels(pixels)

# while 1:
#     pixels = np.roll(pixels, 1, axis=1)
#     time.sleep(1)

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets, uic
# from PyQt5.QtCore import Qt
#
# class Canvas(QtWidgets.QLabel):
#
#     def __init__(self):
#         super().__init__()
#         pixmap = QtGui.QPixmap(600, 300)
#         self.setPixmap(pixmap)
#
#         self.last_x, self.last_y = None, None
#         self.pen_color = QtGui.QColor('#000000')
#
#     def set_pen_color(self, c):
#         self.pen_color = QtGui.QColor(c)
#
#     def mouseMoveEvent(self, e):
#         if self.last_x is None: # First event.
#             self.last_x = e.x()
#             self.last_y = e.y()
#             return # Ignore the first time.
#
#         painter = QtGui.QPainter(self.pixmap())
#         p = painter.pen()
#         p.setWidth(4)
#         p.setColor(self.pen_color)
#         painter.setPen(p)
#         painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
#         painter.end()
#         self.update()
#
#         # Update the origin for next time.
#         self.last_x = e.x()
#         self.last_y = e.y()
#
#     def mouseReleaseEvent(self, e):
#         self.last_x = None
#         self.last_y = None
#
# COLORS = [
# # 17 undertones https://lospec.com/palette-list/17undertones
# '#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
# '#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
# '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
# ]
#
#
# class QPaletteButton(QtWidgets.QPushButton):
#
#     def __init__(self, color):
#         super().__init__()
#         self.setFixedSize(QtCore.QSize(24,24))
#         self.color = color
#         self.setStyleSheet("background-color: %s;" % color)
#
# class MainWindow(QtWidgets.QMainWindow):
#
#     def __init__(self):
#         super().__init__()
#
#         self.canvas = Canvas()
#
#         w = QtWidgets.QWidget()
#         l = QtWidgets.QVBoxLayout()
#         w.setLayout(l)
#         l.addWidget(self.canvas)
#
#         palette = QtWidgets.QHBoxLayout()
#         self.add_palette_buttons(palette)
#         l.addLayout(palette)
#
#         self.setCentralWidget(w)
#
#     def add_palette_buttons(self, layout):
#         for c in COLORS:
#             b = QPaletteButton(c)
#             b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
#             layout.addWidget(b)
#
#
# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow()
# window.show()
# app.exec_()
