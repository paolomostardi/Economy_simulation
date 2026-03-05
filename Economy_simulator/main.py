import sys
import time

from PyQt5.QtWidgets import QApplication

from interface import MainWindow
from society import Society
from tick_manager import TickManager

USE_GUI = False


def run_gui(society: Society):
    app = QApplication(sys.argv)
    window = MainWindow(society)
    window.show()
    sys.exit(app.exec_())


def run_headless(society: Society):
    print("Running headless simulation logs. Press Ctrl+C to stop.")
    try:
        while True:
            society.tick()
            time.sleep(0.8)
    except KeyboardInterrupt:
        print("Simulation stopped.")


if __name__ == "__main__":
    main_society = Society()
    if USE_GUI:
        run_gui(main_society)
    else:
        run_headless(main_society)