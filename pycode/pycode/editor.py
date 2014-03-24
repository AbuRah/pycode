import sys, os
from PySide import QtGui, QtCore
# import file_dialogs as FD

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class PyCodeEditor(QtGui.QMainWindow):

	def __init__(self):
		super(PyCodeEditor, self).__init__()
		
		self.initUI()
		self.setGeometry(150, 150, 800, 600)
		self.setWindowTitle("PyCode The Editor")
		self.show()

	def initUI(self):


		# Here define the various actions the program should take e.g. exit, save, close etc.

		exitAct = QtGui.QAction("Exit", self)
		exitAct.setShortcut("Ctrl+Q")
		exitAct.setStatusTip("Exit the Application")
		exitAct.triggered.connect(self.close) # replace with self.exit_message()

		saveAct = QtGui.QAction("Save", self)
		saveAct.setShortcut("Ctrl+S")
		saveAct.setStatusTip("Save Current Document")
		saveAct.triggered.connect(self.save_file)
		
		saveasAct = QtGui.QAction("Save As ...", self)
		saveasAct.setShortcut("Shift+Ctrl+S")
		saveasAct.setStatusTip("Save file as...")


		newF = QtGui.QAction("New File", self)
		newF.setShortcut("Ctrl+N")
		newF.setStatusTip("Create New document")
		newF.triggered.connect(self.new_file)

		openF = QtGui.QAction("Open", self)
		openF.setShortcut("Ctrl+O")
		openF.setStatusTip("Open a file on the file system")
		openF.triggered.connect(self.open_file_dialog)
		# openF.triggered.connect(self.custom_dialog)

		closeF = QtGui.QAction("Close File", self)
		closeF.setShortcut("Ctrl+W")
		closeF.setStatusTip("Close current file in tab")
		closeF.triggered.connect(self.close_tab)

		bolden = QtGui.QAction("Bold", self)
		bolden.setCheckable(True)
		bolden.setShortcut("Ctrl+B")
		bolden.setStatusTip("bold selected text")
		
		copyAct = QtGui.QAction("Copy", self)
		copyAct.setShortcut("Ctrl+C")
		copyAct.setStatusTip("copy current Selection")
		# copyAct.triggered.

		findAct = QtGui.QAction("Find", self)
		findAct.setShortcut("Ctrl+F")
		findAct.setStatusTip("Find indicated text within current document")
		findAct.triggered.connect(self.find_text)

		cutAct = QtGui.QAction("Cut selection", self)
		cutAct.setShortcut("Ctrl+X")
		cutAct.setStatusTip("Copy selected text to clipboard, then remove from tab page")
		cutAct.triggered.connect(self.cut_selection)

		pasteAct = QtGui.QAction("Paste from clipboard", self)
		pasteAct.setShortcut("Ctrl+V")
		pasteAct.setStatusTip("Paste text in clipboard to page")
		pasteAct.triggered.connect(self.paste_selection)

		redoAct = QtGui.QAction("Redo", self)
		redoAct.setShortcut("Ctrl+Shift+Z")
		redoAct.triggered.connect(self.redo_last)

		undoAct = QtGui.QAction("Undo", self)
		undoAct.setShortcut("Crtl+Z")
		undoAct.triggered.connect(self.undo_last)

		# Here define the menubar and it's functionality

		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		filemenu.addAction(newF)
		filemenu.addSeparator()
		filemenu.addAction(openF)
		filemenu.addAction(saveAct)
		filemenu.addAction(saveasAct)
		filemenu.addSeparator()
		filemenu.addAction(closeF)
		filemenu.addAction(exitAct)
		
		editmenu = mainbar.addMenu("&Edit")
		editmenu.addAction(findAct)
		editmenu.addSeparator()
		editmenu.addAction(copyAct)
		editmenu.addAction(cutAct)
		editmenu.addAction(pasteAct)
		editmenu.addAction(redoAct)
		editmenu.addAction(undoAct)
		editmenu.addSeparator()
		editmenu.addAction(bolden)


		viewmenu = mainbar.addMenu("&View")
		
		toolmenu = mainbar.addMenu("&Tools")
		
		preferences = mainbar.addMenu("&Preferences")
		
		aboutmenu = mainbar.addMenu("&About")

		

		# Here define the statusbar and it's functionality
		status = self.statusBar()
		status.showMessage("Ready", 4000)
		# status.addPermamentWidget() <--- add syntax indicator here using QLabel or other widget


		# testing code goes here:

	











		# Here define the final layout of the editor

		mainlayout = QtGui.QVBoxLayout()
		# mainlayout.addStretch(0)

		maintabbar = QtGui.QTabBar()
		self.workarea = QtGui.QTextEdit()

		self.tabinterface = QtGui.QTabWidget(self)
		self.tabinterface.setMovable(True)
		self.tabinterface.setTabsClosable(True)
		self.tabinterface.addTab(self.workarea, "Document")


		mainlayout.addWidget(self.tabinterface)
		
		self.setCentralWidget(self.tabinterface)
		self.setLayout(mainlayout)

	def open_file_dialog(self):
		"""	opens file in new tab """

		fileName,_ = QtGui.QFileDialog.getOpenFileName(self,
			"Open File",)

		if fileName != '':

			f = open(fileName, "r")
			TEholder = QtGui.QTextEdit()
			
			with f:
				
				data = f.read()
				TEholder.setText(data)
				
				self.tabinterface.addTab(TEholder, "file2")
				f.close()
				
		else:
			pass

	def close_tab(self):
		""" Closes focused tab """
		currentTabIndex = self.tabinterface.currentIndex()
		self.tabinterface.removeTab(currentTabIndex)

	def new_file(self):
		""" Opens a plain rich-text document """
		
		TEholder = QtGui.QTextEdit()
		self.tabinterface.addTab(TEholder, "Untitled")


	def save_file(self):
		""" Save current file"""
		fileName, _ = QtGui.QFileDialog.getSaveFileName(self,
			"Save File")


	def cut_selection(self):
		""" copy/cut selected text """
		currentPage = self.tabinterface.currentWidget()
		currentPage.cut()

	def find_text(self):
		""" Find the indicated text within the current tab page"""
		# currentTabIndex = self.tabinterface.currentIndex()
		### need to add a dialog window OR a pop-up bar.
		currentTab = self.tabinterface.currentWidget()
		currentTab.find()# text goes here

	def paste_selection(self):
		""" paste text from clipboard to tab page """
		currentTab = self.tabinterface.currentWidget()
		currentTab.paste()

	def custom_dialog(self):
		""" Working on Custom File Dialog Here """
		dialog = QtGui.QFileDialog(self)
		dialog.setFileMode(QtGui.QFileDialog.AnyFile)
		dialog.setViewMode(QtGui.QFileDialog.Detail)
		
		if dialog.exec_():
			fileNames = dialog.selectedFiles()

	def undo_last(self):
		""" Steps back in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.undo()



	def redo_last(self):
		""" Steps forward in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.redo()



	def exit_message(self):
		""" Causes a message box specific to closing """

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
