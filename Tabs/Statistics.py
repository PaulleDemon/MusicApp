import pyqtgraph as pg
from PyQt5 import QtWidgets


class Statics(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Statics, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        plot = pg.plot()

        bargraph = pg.BarGraphItem(x=x, height=y1, width=0.6, brush='g')
        plot.addItem(bargraph)

        self.layout().addWidget(plot)