import sys, os
from PySide import QtGui, QtCore
import file_dialogs as FD

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

		exitAct = QtGui.QAction("Exit", self)
		exitAct.setShortcut("Ctrl+Q")
		exitAct.setStatusTip("Exit the Application")
		exitAct.triggered.connect(self.close) # replace with self.close_event

		saveAct = QtGui.QAction("Save", self)
		saveAct.setShortcut("Ctrl+S")
		saveAct.setStatusTip("Save Current Document")
		# saveAct.triggered.connect(self.save)
		
		saveasAct = QtGui.QAction("Save As ...", self)
		saveasAct.setShortcut("Shift+Ctrl+S")
		saveasAct.setStatusTip("Save file as...")


		copyAct = QtGui.QAction("Copy", self)
		copyAct.setShortcut("Ctrl+C")
		copyAct.setStatusTip("copy current Selection")
		# copyAct.triggered.

		newdoc = QtGui.QAction("New File", self)
		newdoc.setShortcut("Ctrl+N")
		newdoc.setStatusTip("Create New document")

		openF = QtGui.QAction("Open", self)
		openF.setShortcut("Ctrl+O")
		openF.setStatusTip("Open a file on the file system")
		openF.triggered.connect(self.testing_open_file_dialog)

		bolden = QtGui.QAction("Bold", self)
		bolden.setCheckable(True)
		bolden.setShortcut("Ctrl+B")
		bolden.setStatusTip("bold selected text")
		

		# Here define the menubar and it's functionality

		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		filemenu.addAction(newdoc)
		filemenu.addSeparator()
		filemenu.addAction(saveasAct)
		filemenu.addAction(exitAct)
		filemenu.addAction(saveAct)
		filemenu.addAction(openF)
		editmenu = mainbar.addMenu("&Edit")
		editmenu.addAction(copyAct)
		editmenu.addAction(bolden)
		viewmenu = mainbar.addMenu("&View")
		toolmenu = mainbar.addMenu("&Tools")
		preferences = mainbar.addMenu("&Preferences")
		aboutmenu = mainbar.addMenu("&About")

		

		# Here define the statusbar and it's functionality
		status = self.statusBar()
		status.showMessage("Ready", 3000)
		# status.addPermamentWidget() <--- add syntax indicator here using QLabel or other widget


		# testing code goes here:

	











		# Here define the final layout of the editor

		mainlayout = QtGui.QVBoxLayout()
		# mainlayout.addStretch(0)

		maintabbar = QtGui.QTabBar()

		# tabstack = QtGui.QStackedWidget()
		# tabstack.addWidget() # this would need to be used for files that are opened. For each file opened, add it to the widget stack
		
		tabinterface = QtGui.QTabWidget()
		self.workarea = QtGui.QTextEdit()

		tabinterface.addTab(self.workarea, "Document")


		mainlayout.addWidget(tabinterface)
		
		self.setCentralWidget(tabinterface)
		self.setLayout(mainlayout)

	def testing_open_file_dialog(self):

		fileName,_ = QtGui.QFileDialog.getOpenFileName(self,
			"Open File",)

		f = open(fileName, "r")

		with f:
			data = f.read()
			self.workarea.setText(data)




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
	# pycodeapp.setStyle("plastique")
	editor = PyCodeEditor()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()