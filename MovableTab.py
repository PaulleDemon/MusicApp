from PyQt5 import QtWidgets, QtGui


class MovableTab(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MovableTab, self).__init__(*args, **kwargs)

        self.tabHolder