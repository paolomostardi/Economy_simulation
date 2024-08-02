import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from society import Society


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


        self.fig2 = Figure(figsize=(20, 20), dpi=100)
        self.canvas2 = FigureCanvas(self.fig2)
        layout.addWidget(self.canvas2)


        button_plot = QPushButton("Start Worker")
        button_plot.clicked.connect(self.start_game)
        layout.addWidget(button_plot)

        self.running = True
        self.plot()

    def start_game(self):
        self.worker = Worker(self.society)
        self.worker.data_signal.connect(self.plot)
        self.worker.start()  # Start the background task

    def plot(self):
        self.fig.clear()
        self.fig2.clear()
        print('plotting ')
        ax = self.fig.add_subplot(241)

        ax.bar(['Medicine ', 'Food ', 'Plumbing '] , [self.society.market.medicine_cost, 
                                                      self.society.market.food_cost, self.society.market.plumbing_cost], color = (0.2,0.7,0.2) )
        ax.set_title('Market Prices')

        ax = self.fig.add_subplot(442)

        ax.set_title('Market Consumption') 

        ax.plot(range(len(self.society.market.medicine_history)) ,self.society.market.medicine_history, color = 'red')
        ax.plot(range(len(self.society.market.plumbing_history)) , self.society.market.plumbing_history, color = 'blue')

        ax = self.fig.add_subplot(446)
        ax.plot(range(len(self.society.market.food_history)) , self.society.market.food_history, color = 'green')


        ax = self.fig.add_subplot(223)
        ax.bar(self.society.count_professions().keys(),  self.society.count_professions().values())  
        

        ax = self.fig.add_subplot(422)
        ax.plot(range(len(self.society.population_history)) ,self.society.sickness_history, color = 'red')
        ax.plot(range(len(self.society.population_history)) , self.society.hunger_history, color = 'green')
        ax.plot(range(len(self.society.population_history)) , self.society.thirst_history, color = 'blue')
        ax.set_title('Population history ' + str(len(self.society.population)))

        ax = self.fig.add_subplot(424)

        ax.plot(range(len(self.society.population_history)) ,self.society.population_history )

        print('total population')
        print(len(self.society.population))


        ax = self.fig.add_subplot(247)

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

        self.canvas.draw()

    def on_button_click(self):
        self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(Society())
    window.show()
    sys.exit(app.exec_())
