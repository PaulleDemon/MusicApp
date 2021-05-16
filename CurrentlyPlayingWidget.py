from PyQt5 import QtWidgets, QtGui, QtCore


class CurrentlyPlaying(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CurrentlyPlaying, self).__init__(*args, **kwargs)

        grid_layout = QtWidgets.QGridLayout(self)

        self.thumb_nail = QtWidgets.QLabel()
        self.setThumbNail(r"Resources/Music.png")
        self.thumb_nail.setStyleSheet("border: 2px solid black")
        self.thumb_nail.setScaledContents(True)

        self.play_pause = QtWidgets.QPushButton(objectName="PlayPause")
        self.next = QtWidgets.QPushButton(objectName="Next")
        self.previous = QtWidgets.QPushButton(objectName="Previous")

        self.progress = QtWidgets.QProgressBar()

        grid_layout.addWidget(self.thumb_nail, 0, 0, 1, 3)
        grid_layout.addWidget(self.previous, 1, 0, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.play_pause, 1, 1, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.next, 1, 2, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress, 2, 0, 1, 3, alignment=QtCore.Qt.AlignTop)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(CurrentlyPlaying, self).resizeEvent(event)
        self.thumb_nail.setFixedHeight(self.thumb_nail.width())

    def setThumbNail(self, path: str):
        pixmap = QtGui.QPixmap(path)
        pixmap = pixmap.scaled(self.thumb_nail.width()-2, self.thumb_nail.height()-2)
        self.thumb_nail.setPixmap(pixmap)


