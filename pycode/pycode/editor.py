import sys, os
from PySide import QtGui, QtCore

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class PyCodeEditor(QtGui.QMainWindow):

	def __init__(self):
		super(PyCodeEditor, self).__init__()
		
		self.initUI()

	def initUI(self):

		exitAct = QtGui.QAction(QtGui.QIcon("../images_tmp/exit_icon.png"), "&Exit", self)
		exitAct.setShortcut("Ctrl+Q")
		exitAct.setStatusTip("Exit the Application")
		exitAct.triggered.connect(self.close)

		# self.statusBar()

		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		filemenu.addAction(exitAct)

		self.setGeometry(300, 300, 600, 800)
		self.setWindowTitle("PyCode The Editor")
		self.show()


	def close_event(self):

		ask = QtGui.QMessageBox.question(self, "Alert!",
			"Are You Sure You Want To Quit?",
			QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
			QtGui.QMessageBox.No)

		if ask == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

def main():
	pycodeapp = QtGui.QApplication(sys.argv)
	editor = PyCodeEditor()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
