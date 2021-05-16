from PyQt5 import QtWidgets, QtGui, QtCore


class Tile(QtWidgets.QLabel):

    def __init__(self, image_path: str = "", size: tuple = (100, 100),*args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)

        self.setScaledContents(True)
        pixMap = QtGui.QPixmap(image_path)
        self.setPixmap(pixMap)

        self.setLayout(QtWidgets.QHBoxLayout())

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setToolTip("Play")

        self.favourite = QtWidgets.QPushButton(objectName="favourite")
        self.favourite.setToolTip("Mark Favourite")

        self.collection = QtWidgets.QPushButton(objectName="Collection")
        self.collection.setToolTip("Add to Collection")

        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.collection, alignment=QtCore.Qt.AlignBottom)

        self.btns.hide()
        self.layout().addWidget(self.btns)

        self._original_size = QtCore.QSize(*size)
        self.setMinimumSize(self._original_size)
        # self.setMaximumSize(self._original_size.width()+25, self._original_size.height()+25)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:

        event.accept()

        if event.size().width() > event.size().height():
            self.resize(event.size().height(), event.size().height())

        else:
            self.resize(event.size().width(), event.size().width())

    def enterEvent(self, a0: QtCore.QEvent):

        self.btns.show()
        # self.setFixedSize(self._original_size.width()+25, self._original_size.height()+25)

        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setStartValue(QtCore.QRect(self.geometry()))
        self.animation.setEndValue(QtCore.QRect(self.geometry().adjusted(-25, -25, 25, 25)))
        self.animation.setDuration(150)
        self.animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)


    def leaveEvent(self, a0: QtCore.QEvent):
        print(self.geometry(), self.geometry().right(), self.geometry().bottom())
        self.btns.hide()
        # self.setFixedSize(self._original_size.width(), self._original_size.height())
        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setStartValue(QtCore.QRect(self.geometry()))
        self.animation.setEndValue(QtCore.QRect(self.geometry().adjusted(25, 25, -25, -25)))
        self.animation.setDuration(150)
        self.animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)

