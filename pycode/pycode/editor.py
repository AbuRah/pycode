import sys, os

from PySide.QtGui import (QAction,QMainWindow,QTabWidget,QPlainTextEdit,
	QFileDialog,QMessageBox,QApplication,QVBoxLayout)

from PySide.QtCore import (QSettings,QFileInfo,QSize,QPoint,QFile,QDir,QIODevice)

# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class PyCodeEditor(QMainWindow):

	def __init__(self):
		super(PyCodeEditor, self).__init__()
		
		self.initUI()
		self.settings = None
		self.read_settings()
		self.setWindowTitle("PyCode The Editor")
		self.show()

	def initUI(self):


		# Here define the various actions the program should take e.g. exit, save, close etc.

		exitAct = QAction("Exit", self)
		exitAct.setShortcut("Ctrl+Q")
		exitAct.setStatusTip("Exit the Application")
		exitAct.triggered.connect(self.exit_event) # replace with self.exit_message()
		# exitAct.triggered.connect(self.exit_message)

		saveAct = QAction("Save", self)
		saveAct.setShortcut("Ctrl+S")
		saveAct.setStatusTip("Save Current Document")
		saveAct.triggered.connect(self.save_event)
		
		saveasAct = QAction("Save As ...", self)
		saveasAct.setShortcut("Shift+Ctrl+S")
		saveasAct.setStatusTip("Save file as...")
		saveasAct.triggered.connect(self.save_file_as)


		newF = QAction("New File", self)
		newF.setShortcut("Ctrl+N")
		newF.setStatusTip("Create New document")
		newF.triggered.connect(self.new_file)

		openF = QAction("Open", self)
		openF.setShortcut("Ctrl+O")
		openF.setStatusTip("Open a file on the file system")
		openF.triggered.connect(self.open_file_dialog)
		# openF.triggered.connect(self.custom_dialog)

		closeF = QAction("Close File", self)
		closeF.setShortcut("Ctrl+W")
		closeF.setStatusTip("Close current file in tab")
		closeF.triggered.connect(self.close_tab)

		bolden = QAction("Bold", self)
		bolden.setCheckable(True)
		bolden.setShortcut("Ctrl+B")
		bolden.setStatusTip("bold selected text")
		
		copyAct = QAction("Copy", self)
		copyAct.setShortcut("Ctrl+C")
		copyAct.setStatusTip("copy current Selection")
		# copyAct.triggered.

		findAct = QAction("Find", self)
		findAct.setShortcut("Ctrl+F")
		findAct.setStatusTip("Find indicated text within current document")
		findAct.triggered.connect(self.find_text)

		cutAct = QAction("Cut selection", self)
		cutAct.setShortcut("Ctrl+X")
		cutAct.setStatusTip("Copy selected text to clipboard, then remove from tab page")
		cutAct.triggered.connect(self.cut_selection)

		pasteAct = QAction("Paste from clipboard", self)
		pasteAct.setShortcut("Ctrl+V")
		pasteAct.setStatusTip("Paste text in clipboard to page")
		pasteAct.triggered.connect(self.paste_selection)

		redoAct = QAction("Redo", self)
		redoAct.setShortcut("Ctrl+Shift+Z")
		redoAct.triggered.connect(self.redo_last)

		undoAct = QAction("Undo", self)
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
		
		editmenu = mainbar.addMenu("Edit")
		editmenu.addAction(findAct)
		editmenu.addSeparator()
		editmenu.addAction(copyAct)
		editmenu.addAction(cutAct)
		editmenu.addAction(pasteAct)
		editmenu.addAction(redoAct)
		editmenu.addAction(undoAct)
		editmenu.addSeparator()
		editmenu.addAction(bolden)


		viewmenu = mainbar.addMenu("View")
		
		toolmenu = mainbar.addMenu("Tools")
		
		preferences = mainbar.addMenu("Preferences")
		
		aboutmenu = mainbar.addMenu("About")

		

		# Here define the statusbar and it's functionality
		status = self.statusBar()
		status.showMessage("Ready", 4000)
		# status.addPermamentWidget() <--- add syntax indicator here using QLabel or other widget


		# testing code goes here:

		# self.setDocumentMode(True)	
		self.setTabShape(QTabWidget.Triangular)
				






		# Here define the final layout of the editor

		self.mainlayout = QVBoxLayout()

		self.workarea = QPlainTextEdit()

		self.tabinterface = QTabWidget(self)
		self.tabinterface.setDocumentMode(True)
		self.tabinterface.setMovable(True)
		self.tabinterface.setTabsClosable(True)
		self.tabinterface.addTab(self.workarea, "Untitled")



		# self.tabinterface.setTabShape(QTabWidget.Triangular)



		self.mainlayout.addWidget(self.tabinterface)
		
		self.setCentralWidget(self.tabinterface)
		self.setLayout(self.mainlayout)



# SLOTS
# ===================================================================================================		

	def open_file_dialog(self):
		"""	opens file in new tab """

		filename,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if filename != '':

			f = open(filename, "r")
			TEholder = QPlainTextEdit()
			
			with f:
				
				data = f.read()
				TEholder.setPlainText(data)

				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.filename()

				self.tabinterface.addTab(TEholder, nameOfFile)
				f.close()
				
		else:
			pass

	def close_tab(self):
		""" Closes focused tab """
		currentTabIndex = self.tabinterface.currentIndex()
		return self.tabinterface.removeTab(currentTabIndex)

	def new_file(self):
		""" Opens a plain rich-text document """
		import re
		
		TEholder = QPlainTextEdit()
		
		return self.tabinterface.addTab(TEholder, "Untitled 1")
		




	def save_event(self):
		""" Saves file with current tab title text, no prompting """
		filename = self.tabinterface.tabText(self.tabinterface.currentIndex())		
		
		
		save_file = QFile(filename)


		save_file_name = QFile.fileName(save_file)

		
		save_file.open(QIODevice.WriteOnly)

		focusedPage = self.tabinterface.currentWidget()
		changes = focusedPage.toPlainText()

		save_file.write(changes)

		save_file.close()



	def save_file_as(self):
		""" Save current file"""
		filename, _ = QFileDialog.getSaveFileName(self,
			"Save File", os.getcwd())


		if filename != '':

			f = open(filename, "w")

			with f:

				focusedPage = self.tabinterface.currentWidget()
				changes = focusedPage.toPlainText()
				
				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.tabinterface.setTabText(self.tabinterface.currentIndex(), nameOfFile)


				updated_data = f.write(changes)
				f.close()
		else:
			pass

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
		""" 
		Working on Custom File Dialog Here 
		
		"""
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setViewMode(QFileDialog.list)
		
		if dialog.exec_():
			filenames = dialog.selectedFiles()

	def undo_last(self):
		""" Steps back in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.undo()



	def redo_last(self):
		""" Steps forward in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.redo()


	def exit_event(self):
		""" Exits without prompting """
		self.write_settings()
		self.close()

	def exit_message(self):
		""" Causes a message box specific to closing """

		ask = QMessageBox.question(self, "WARNING!",
			"Are You Sure You Want To Quit?",
			QMessageBox.Yes | QMessageBox.No, 
			QMessageBox.No)

		if ask == QMessageBox.Yes:
			self.write_settings()
			self.close()
		
		else:
			# event.ignore()
			pass


	def write_settings(self):
		""" Writes the current user settings """
		self.settings = QSettings(QSettings.UserScope, "Autodidactic Engineering", "PyCode The Editor")
		self.settings.beginGroup("Main Window")
		self.settings.setValue("Geometry", self.saveGeometry())
		self.settings.setValue("Window State", self.saveState())
		self.settings.endGroup()


	def read_settings(self):
		""" Loads the saved settings from a previous session """
		self.settings = QSettings("Autodidactic Engineering", "PyCode The Editor")
		self.settings.beginGroup("Main Window")
		self.restoreGeometry(self.settings.value("Geometry"))
		self.restoreState(self.settings.value("Window State"))
		self.settings.endGroup()


#==========================================================================================

def main():
	pycodeapp = QApplication(sys.argv)
	pycodeapp.setStyle("plastique")
	editor = PyCodeEditor()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
