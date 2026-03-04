import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from society import Society

# graphic interface of the game 
class Worker(QThread):
    data_signal = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, society : Society, parent=None):
        super().__init__(parent)
        self.society = society

    def run(self):
        while True:
            print('runnig ticks')
            self.society.tick()
            self.data_signal.emit() # Emit the new data
            time.sleep(0.8)


class SecondaryWindow(QMainWindow):
    def __init__(self, society: Society, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.society = society
        self.setWindowTitle("Market Overview")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        info_label = QLabel("Market prices and consumption")
        layout.addWidget(info_label)

        self.fig_market = Figure(figsize=(8, 10), dpi=100)
        self.canvas_market = FigureCanvas(self.fig_market)
        layout.addWidget(self.canvas_market)

        back_button = QPushButton("Return to Main Window")
        back_button.clicked.connect(self.return_to_main)
        layout.addWidget(back_button)

        self.plot_market()

    def return_to_main(self):
        if self.main_window is not None:
            self.hide()
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def plot_market(self):
        self.fig_market.clear()

        ax = self.fig_market.add_subplot(311)
        ax.bar(['Medicine', 'Food', 'Plumbing'], [
            self.society.market.medicine_cost,
            self.society.market.food_cost,
            self.society.market.plumbing_cost
        ], color=(0.2, 0.7, 0.2))
        ax.set_title('Market Prices')

        ax = self.fig_market.add_subplot(312)
        ax.set_title('Market Consumption (Medicine / Plumbing)')
        ax.plot(range(len(self.society.market.medicine_history)), self.society.market.medicine_history, color='red', label='Medicine')
        ax.plot(range(len(self.society.market.plumbing_history)), self.society.market.plumbing_history, color='blue', label='Plumbing')
        ax.legend(loc='upper right')

        ax = self.fig_market.add_subplot(313)
        ax.set_title('Market Consumption (Food)')
        ax.plot(range(len(self.society.market.food_history)), self.society.market.food_history, color='green')

        self.fig_market.tight_layout(pad=2.0, h_pad=2.0, w_pad=1.0)
        self.canvas_market.draw()

class MainWindow(QMainWindow):
    def __init__(self, society : Society) -> None:
        super().__init__()
        self.setWindowTitle("Simulation")
        self.society = society

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.fig = Figure(figsize=(70, 40), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)


        button_plot = QPushButton("Start Worker")
        button_plot.clicked.connect(self.toggle_worker)
        self.button_plot = button_plot
        layout.addWidget(button_plot)

        switch_button = QPushButton("Open Secondary Window")
        switch_button.clicked.connect(self.open_secondary_window)
        layout.addWidget(switch_button)

        self.worker = None
        self.secondary_window = SecondaryWindow(self.society, self)
        self.running = True
        self.plot()

    def toggle_worker(self):
        if self.worker is None or not self.worker.isRunning():
            # Start the worker
            self.worker = Worker(self.society)
            self.worker.data_signal.connect(self.plot)
            self.worker.start()
            self.button_plot.setText("Stop Worker")
        else:
            # Stop the worker
            self.worker.terminate()
            self.worker.wait()
            self.worker = None
            self.button_plot.setText("Start Worker")

    def open_secondary_window(self):
        if self.secondary_window is None:
            self.secondary_window = SecondaryWindow(self)

        self.hide()
        self.secondary_window.show()
        self.secondary_window.raise_()
        self.secondary_window.activateWindow()

    def plot(self):
        self.fig.clear()
        print('plotting ')

        ax = self.fig.add_subplot(231)
        ax.bar(self.society.count_professions().keys(),  self.society.count_professions().values())  
        

        ax = self.fig.add_subplot(232)
        ax.plot(range(len(self.society.population_history)) ,self.society.sickness_history, color = 'red')
        ax.plot(range(len(self.society.population_history)) , self.society.hunger_history, color = 'green')
        ax.plot(range(len(self.society.population_history)) , self.society.thirst_history, color = 'blue')
        ax.set_title('Population history ' + str(len(self.society.population)))

        ax = self.fig.add_subplot(233)

        ax.plot(range(len(self.society.population_history)) ,self.society.population_history )

        print('total population')
        print(len(self.society.population))


        ax = self.fig.add_subplot(234)

        money_stats = self.society.profession_money_stats()

        labels = [
            'Farmers',
            'Pharmacists',
            'Plumbers',
            'Students'
        ]
        values = [
            money_stats['farmer_money'],
            money_stats['pharmacist_money'],
            money_stats['plumber_money'],
            money_stats['student_money']
        ]
        
        # Plotting the pie chart
        ax.pie(values, labels=labels, startangle=90)        
        ax.set_title('money distribution')

        ax = self.fig.add_subplot(235)
        ax.plot(range(len(self.society.population_history)), self.society.hunger_history, label='Hunger', color='green')
        ax.plot(range(len(self.society.population_history)), self.society.thirst_history, label='Thirst', color='blue')
        ax.plot(range(len(self.society.population_history)), self.society.sickness_history, label='Sickness', color='red')
        ax.set_title('Needs Over Time')
        ax.legend(loc='upper right')

        ax = self.fig.add_subplot(236)
        ax.plot(range(len(self.society.population_history)) ,self.society.population_history )
        ax.set_title('Population Trend')

        # ensure subplot titles/labels don't overlap
        self.fig.tight_layout(pad=2.0, h_pad=2.0, w_pad=1.5)
        self.canvas.draw()

        if self.secondary_window is not None:
            self.secondary_window.plot_market()

    def on_button_click(self):
        self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(Society())
    window.show()
    sys.exit(app.exec_())
