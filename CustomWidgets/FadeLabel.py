import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class FadeLabel(QtWidgets.QLabel):
    
    def __init__(self, *args, **kwargs):
        super(FadeLabel, self).__init__(*args, **kwargs)

        self.setScaledContents(True)
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect(self, opacity=1.0)
        self.setGraphicsEffect(self.opacity_effect)

        self.animation_duration = 20000

    def fadeIn(self):

        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        # self.animation.setEasingCurve(QtCore.QEasingCurve(QtCore.QEasingCurve.InBack))
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start(self.animation.DeleteWhenStopped)

    def fadeOut(self):
        self.animation = QtCore.QPropertyAnimation(self.opacity_effect, b"opacity")
        # self.animation.setEasingCurve(QtCore.QEasingCurve(QtCore.QEasingCurve.OutBack))
        # self.animation.finished.connect(self.animationFinished)
        self.animation.valueChanged.connect(self.animationFinished)
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start(self.animation.DeleteWhenStopped)

    def animationFinished(self, value):
        # self.fadeIn()
        print("FINISHED: ", value)

    def setPixmap(self, a0: QtGui.QPixmap) -> None:
        # self.fadeOut()
        super(FadeLabel, self).setPixmap(a0)
        # self.fadeIn()

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    label = FadeLabel("wfwefwef")
    label.setStyleSheet('background-color: red;')
    label.setFixedSize(300, 100)
    label.show()
    label.setPixmap(QtGui.QPixmap(r"C:\Users\Paul\Desktop\Code Repository\python programs\MusicApp\Resources\Icons\Music.png"))

    label.fadeOut()

    sys.exit(app.exec_())

