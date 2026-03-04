import sys
import time
import numpy as np

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)

import pyqtgraph as pg

from society import Society


class SimulationWorker(QThread):
    data_signal = pyqtSignal()

    def __init__(self, society: Society, parent=None):
        super().__init__(parent)
        self.society = society
        self._running = True

    def run(self):
        while self._running:
            self.society.tick()
            self.data_signal.emit()
            time.sleep(0.8)

    def stop(self):
        self._running = False
        self.wait(1000)


class PyQtGraphWindow(QMainWindow):
    def __init__(self, society: Society):
        super().__init__()
        self.setWindowTitle("Economy Simulation - PyQtGraph Dashboard")
        self.society = society

        pg.setConfigOptions(antialias=True, background="#0f1116", foreground="w")

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.price_plot = pg.PlotWidget(title="Market Prices")
        self.price_plot.showGrid(x=True, y=True, alpha=0.3)
        self.price_plot.setLabel("left", "Cost")
        self.price_plot.setLabel("bottom", "Resource")
        layout.addWidget(self.price_plot)

        self.consumption_plot = pg.PlotWidget(title="Market Consumption History")
        self.consumption_plot.showGrid(x=True, y=True, alpha=0.3)
        self.consumption_plot.addLegend(offset=(10, 10))
        self.consumption_plot.setLabel("left", "Units Consumed")
        self.consumption_plot.setLabel("bottom", "Tick")
        layout.addWidget(self.consumption_plot)

        self.population_plot = pg.PlotWidget(title="Population & Needs")
        self.population_plot.showGrid(x=True, y=True, alpha=0.3)
        self.population_plot.addLegend(offset=(10, 10))
        self.population_plot.setLabel("left", "People")
        self.population_plot.setLabel("bottom", "Tick")
        layout.addWidget(self.population_plot)

        self.toggle_button = QPushButton("Start Simulation")
        self.toggle_button.clicked.connect(self.toggle_simulation)
        layout.addWidget(self.toggle_button)

        self.worker: SimulationWorker | None = None
        self.update_plots()

    def toggle_simulation(self):
        if self.worker is None:
            self.worker = SimulationWorker(self.society)
            self.worker.data_signal.connect(self.update_plots)
            self.worker.start()
            self.toggle_button.setText("Stop Simulation")
        else:
            self.worker.stop()
            self.worker = None
            self.toggle_button.setText("Start Simulation")

    def closeEvent(self, event):
        if self.worker is not None:
            self.worker.stop()
            self.worker = None
        super().closeEvent(event)

    def update_plots(self):
        self._update_price_plot()
        self._update_consumption_plot()
        self._update_population_plot()

    def _update_price_plot(self):
        market = self.society.market
        labels = ["Medicine", "Food", "Plumbing"]
        prices = [market.medicine_cost, market.food_cost, market.plumbing_cost]
        x = np.arange(len(labels))

        self.price_plot.clear()
        for idx, value in enumerate(prices):
            bar = pg.BarGraphItem(
                x=[x[idx]],
                height=[value],
                width=0.6,
                brush=pg.mkBrush(["#d9534f", "#5cb85c", "#5bc0de"][idx]),
            )
            self.price_plot.addItem(bar)

        self.price_plot.getAxis("bottom").setTicks([list(enumerate(labels))])

    def _update_consumption_plot(self):
        market = self.society.market
        ticks = np.arange(len(market.food_history))

        self.consumption_plot.clear()
        self.consumption_plot.plot(
            ticks,
            market.food_history,
            pen=pg.mkPen("#5cb85c", width=2),
            name="Food",
        )
        self.consumption_plot.plot(
            ticks,
            market.medicine_history,
            pen=pg.mkPen("#d9534f", width=2),
            name="Medicine",
        )
        self.consumption_plot.plot(
            ticks,
            market.plumbing_history,
            pen=pg.mkPen("#5bc0de", width=2),
            name="Plumbing",
        )

    def _update_population_plot(self):
        ticks = np.arange(len(self.society.population_history))
        self.population_plot.clear()
        self.population_plot.plot(
            ticks,
            self.society.population_history,
            pen=pg.mkPen("#f0ad4e", width=2),
            name="Population",
        )
        self.population_plot.plot(
            ticks,
            self.society.hunger_history,
            pen=pg.mkPen("#5cb85c", width=2, style=pg.QtCore.Qt.DashLine),
            name="Hunger",
        )
        self.population_plot.plot(
            ticks,
            self.society.thirst_history,
            pen=pg.mkPen("#5bc0de", width=2, style=pg.QtCore.Qt.DotLine),
            name="Thirst",
        )
        self.population_plot.plot(
            ticks,
            self.society.sickness_history,
            pen=pg.mkPen("#d9534f", width=2, style=pg.QtCore.Qt.DashDotLine),
            name="Sickness",
        )


def main():
    app = QApplication(sys.argv)
    window = PyQtGraphWindow(Society())
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
