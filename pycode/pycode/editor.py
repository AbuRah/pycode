import sys, os
from PySide import QtGui, QtCore

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class PyCodeEditor(QtGui.QMainWindow):

	def __init__(self):
		super(PyCodeEditor, self).__init__()
		
		self.initUI()
		self.setGeometry(150, 150, 600, 600)
		self.setWindowTitle("PyCode The Editor")
		self.show()

	def initUI(self):


		# Here define the various actions the program should take e.g. exit, save, close etc.

		exitAct = QtGui.QAction(QtGui.QIcon("../images_tmp/exit_icon.png"), "&Exit", self)
		exitAct.setShortcut("Ctrl+Q")
		exitAct.setStatusTip("Exit the Application")
		exitAct.triggered.connect(self.close) # replace with self.close_event

		saveAct = QtGui.QAction("&Save", self)
		saveAct.setShortcut("Ctrl+S")
		saveAct.setStatusTip("Save Current Document")
		# saveAct.triggered.connect(self.save)
		
		copyAct = QtGui.QAction("&Copy", self)
		copyAct.setShortcut("Ctrl+C")
		copyAct.setStatusTip("copy current Selection")
		

		# Here define the menubar and it's functionality

		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		filemenu.addAction(exitAct)
		filemenu.addAction(saveAct)
		editmenu = mainbar.addMenu("&Edit")
		editmenu.addAction(copyAct)
		viewmenu = mainbar.addMenu("&View")
		toolmenu = mainbar.addMenu("&Tools")
		preferences = mainbar.addMenu("&Preferences")
		aboutmenu = mainbar.addMenu("&About")

		









		# Here define the final layout of the editor
		
		mainlayout = QtGui.QVBoxLayout()
		mainlayout.addStretch(1)

		# QtCore.QIODevice.write
		maintabbar = QtGui.QTabBar()

		tabstack = QtGui.QStackedWidget()
		# tabstack.addWidget() # this would need to be used for files that are opened. For each file opened, add it to the widget stack
		
		tabinterface = QtGui.QTabWidget()
		workarea =QtGui.QTextEdit()

		tabinterface.addTab(workarea, "Current Document")


		mainlayout.addWidget(tabinterface)
		
		self.setCentralWidget(tabinterface)
		self.setLayout(mainlayout)







		



	def close_event(self):

		ask = QtGui.QMessageBox.question(self, "WARNING!",
			"Are You Sure You Want To Quit?",
			QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, 
			QtGui.QMessageBox.No)

		if ask == QtGui.QMessageBox.Yes:
			self.close()
		else:
			event.ignore()

def main():
	pycodeapp = QtGui.QApplication(sys.argv)
	editor = PyCodeEditor()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
