from society import Society
from interface import MainWindow
from PyQt5.QtWidgets import QApplication
import sys
from tick_manager import TickManager

main = Society()
app = QApplication(sys.argv)
window = MainWindow(main)
window.show()




sys.exit(app.exec_())