from PyQt5 import QtWidgets, QtCore


class Tile(QtWidgets.QWidget):  # This is the base class for collection, music tiles etc

    def __init__(self, size: tuple = (100, 100),*args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)

        self.setObjectName("Tile")

        self._original_size = QtCore.QSize(*size)
        self.setMinimumSize(self._original_size)
        self.setMaximumSize(self._original_size.width()+50, self._original_size.height()+50)

        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)

    def play(self):
        raise NotImplementedError("Must implement play")

    def pause(self):
        raise NotImplementedError("Must implement pause")

    def animate(self, expand):
        if expand:
            self.animation.setDirection(self.animation.Forward)
        else:
            self.animation.setDirection(self.animation.Backward)
        self.animation.start()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        super(Tile, self).enterEvent(a0)
        self.animate(True)

        try:
            self.btns.show()

        except:
            raise NotImplementedError(f"btns and blur_effect must be an instance"
                                      f" variable in child class: {self.__class__}")

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        super(Tile, self).leaveEvent(a0)
        self.animate(False)
        self.btns.hide()

    def updateAnimation(self):
        if not self.animation.state():
            center = self.geometry().center()
            start = QtCore.QRect(QtCore.QPoint(), self.minimumSize())
            start.moveCenter(center)
            self.animation.setStartValue(start)
            end = QtCore.QRect(QtCore.QPoint(), self.maximumSize())
            end.moveCenter(center)
            self.animation.setEndValue(end)

    def moveEvent(self, event):
        self.updateAnimation()

    def resizeEvent(self, event):
        self.updateAnimation()
        if not self.animation.state():
            rect = QtCore.QRect(QtCore.QPoint(),
                                self.maximumSize() if self.underMouse() else self.minimumSize())
            rect.moveCenter(self.geometry().center())
            self.setGeometry(rect)
