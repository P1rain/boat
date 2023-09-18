from PyQt5.QtWidgets import QWidget

from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Lectures(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('../../UI/LectureItem.ui', self)
