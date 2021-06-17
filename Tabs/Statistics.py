from PyQt5.QtChart import QChart, QChartView, QBarCategoryAxis, QValueAxis, QBarSet, QBarSeries
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class Statics(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Statics, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.chart = QChart()
        self.chart.setTitle('Bar Chart Demo')
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.chart_view = QChartView(self.chart)
        self.layout().addWidget(self.chart_view)

    def plotAxis(self, plot: dict):  # todo: Simplify this part, enable tooltip

        if self.chart.series():
            self.chart.removeSeries(*self.chart.series())
            self.chart.removeAxis(self.chart.axisX())
            self.chart.removeAxis(self.chart.axisY())

        series = QBarSeries()

        values = QBarSet('X0')
        values.append(plot.values())

        series.append(values)

        x_axis = plot.keys()

        axisX = QBarCategoryAxis()
        axisX.append(x_axis)

        axisY = QValueAxis()
        axisY.setRange(0, max(plot.values())+5)

        self.chart.addAxis(axisX, Qt.AlignBottom)
        self.chart.addAxis(axisY, Qt.AlignLeft)

        self.chart.addSeries(series)

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)


