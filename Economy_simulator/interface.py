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
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x + 1 * 0.1)  # Update the sine wave based on input_value
            self.data_signal.emit() # Emit the new data
            time.sleep(0.5)

class MainWindow(QMainWindow):
    def __init__(self, society : Society) -> None:
        super().__init__()
        self.setWindowTitle("Simulation")
        self.society = society

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.fig = Figure(figsize=(50, 40), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

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
        print('plotting ')
        ax = self.fig.add_subplot(2,1,1)
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        ax.bar(['Medicine Price', 'Food Price'] , [self.society.market.medicine_cost, self.society.market.food_cost] )
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.set_title('Simple Sine Wave')
        self.canvas.draw()

    def on_button_click(self):
        self.plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(Society())
    window.show()
    sys.exit(app.exec_())
