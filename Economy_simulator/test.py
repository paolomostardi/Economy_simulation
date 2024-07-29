import sys
import time
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from society import Society

class Worker(QThread):
    data_signal = pyqtSignal(np.ndarray, np.ndarray)
    progress = pyqtSignal(int)

    def __init__(self, input_value, parent=None):
        super().__init__(parent)
        print()
        self.input_value = input_value

    def run(self):
        for i in range(1, 11):
            time.sleep(1)  # Simulate a long-running task
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x + self.input_value * i * 0.1)  # Update the sine wave based on input_value
            self.data_signal.emit(x, y) # Emit the new data
            self.progress.emit(i * 10) # Emit the progress
            self.data_signal.emit(x, y) # Emit the new data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matplotlib with PyQt5")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.fig = Figure(figsize=(10, 8))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.ax = self.fig.add_subplot(111)
        
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter a value")
        layout.addWidget(self.input_field)

        button_plot = QPushButton("Start Worker")
        button_plot.clicked.connect(self.start_worker)
        layout.addWidget(button_plot)

        button_clear = QPushButton("Clear Plot")
        button_clear.clicked.connect(self.clear_plot)
        layout.addWidget(button_clear)

        self.progress_label = QLabel("Progress: 0%")
        layout.addWidget(self.progress_label)

    def start_worker(self):
        input_value = float(self.input_field.text())  # Get the input value from the line edit
        self.worker = Worker(input_value)
        self.worker.data_signal.connect(self.update_plot)
        self.worker.progress.connect(self.update_progress)
        self.worker.start()  # Start the background task

    def update_plot(self, x, y):
        self.ax.clear()  # Clear the previous plot
        self.ax.plot(x, y)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('sin(x)')
        self.ax.set_title('Dynamic Sine Wave')
        self.canvas.draw()

    def clear_plot(self):
        self.fig.clear()  # Clear the figure to remove all plots
        self.ax = self.fig.add_subplot(111)  # Re-add the single subplot
        self.canvas.draw()  # Redraw the canvas to reflect the changes

    def update_progress(self, value):
        self.progress_label.setText(f"Progress: {value}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
