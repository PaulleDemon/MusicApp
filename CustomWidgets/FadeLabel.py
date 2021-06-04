import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class FadeLabel(QtWidgets.QLabel):

    finished = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(FadeLabel, self).__init__(*args, **kwargs)

        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation_duration = 5000

    def fadeIn(self):

        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        # self.animation.setEasingCurve(QtCore.QEasingCurve(QtCore.QEasingCurve.InBack))
        self.animation.finished.connect(self.finished.emit)
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start(self.animation.DeleteWhenStopped)

    def fadeOut(self):
        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        # self.animation.setEasingCurve(QtCore.QEasingCurve(QtCore.QEasingCurve.OutBack))
        # self.animation.finished.connect(self.animationFinished)
        self.animation.finished.connect(self.finished.emit)
        self.animation.valueChanged.connect(self.animationFinished)
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start(self.animation.DeleteWhenStopped)

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        super(FadeLabel, self).setPixmap(a0)
