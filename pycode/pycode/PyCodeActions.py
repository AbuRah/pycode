from PySide.QtGui import QAction, QActionGroup
from PySide.QtCore import Qt

class PyCodeActions():
	""" Here i've placed all of the Needed actions for the main window
		I feel this will make it easier to debug and modify the program.	

	"""

	def __init__(self, parent=None):
		# super(PyCodeActions, self).__init__(parent)
		
		# for file menu
		self.exitAct = QAction("Exit", parent)
		self.saveAct = QAction("Save", parent)
		self.saveasAct = QAction("Save As ...", parent)
		self.newF = QAction("New File", parent)
		self.newW = QAction("New Window", parent)
		self.closeF = QAction("Close File", parent)
		self.closeW = QAction("Close Window", parent)
		self.openF = QAction("Open", parent)
		self.reopenT = QAction("Re-Open last Tab", parent)

		#for edit menu
		self.pasteAct = QAction("Paste from clipboard", parent)
		self.redoAct = QAction("Redo", parent)
		self.cutAct = QAction("Cut selection", parent)
		self.undoAct = QAction("Undo", parent)
		self.bolden = QAction("Bold", parent)
		self.copyAct = QAction("Copy", parent)
		self.findAct = QAction("Find", parent)
		self.findR = QAction("Find && Replace", parent)

		# for tool menu
		self.tabW2 = QAction("Tab Width: 2", parent)
		self.tabW4 = QAction("Tab Width: 4", parent)
		self.tabW6 = QAction("Tab Width: 6", parent)
		self.tabW8 = QAction("Tab Width: 8", parent)

		# for view menu
		self.plainL = QAction("Single Layout", parent)
		self.splitL = QAction("Two Windows", parent)
		self.gridL = QAction("Four windows", parent)

		# Set menu shortcuts
		self.exitAct.setShortcut("Ctrl+Q")
		self.saveAct.setShortcut("Ctrl+S")
		self.saveasAct.setShortcut("Shift+Ctrl+S")
		self.newF.setShortcut("Ctrl+N")
		self.newW.setShortcut("Ctrl+Shift+N")
		self.openF.setShortcut("Ctrl+O")
		self.closeF.setShortcut("Ctrl+W")
		self.closeW.setShortcut("Ctrl+Shift+W")
		self.bolden.setShortcut("Ctrl+B")
		self.copyAct.setShortcut("Ctrl+C")
		self.findAct.setShortcut("Ctrl+F")
		self.undoAct.setShortcut("Crtl+Z")
		self.reopenT.setShortcut("Ctrl+Shift+T")
		self.findR.setShortcut("Ctrl+F")
		self.redoAct.setShortcut("Ctrl+Shift+Z")
		self.pasteAct.setShortcut("Ctrl+V")
		self.cutAct.setShortcut("Ctrlself.self.self.self.self.self.+X")

		# shorcut Contexts
		self.closeW.setShortcutContext(Qt.WidgetShortcut)



		# status Tips go here

		self.exitAct.setStatusTip("Exit the Application")
		self.saveAct.setStatusTip("Save Current Document")
		self.saveasAct.setStatusTip("Save file as...")
		self.newF.setStatusTip("Create New document")
		self.openF.setStatusTip("Open a file on the file system")
		self.closeF.setStatusTip("Close current file in tab")
		self.bolden.setStatusTip("bold selected text")
		self.copyAct.setStatusTip("copy current Selection")
		self.findAct.setStatusTip("Find indicated text within current document")
		self.cutAct.setStatusTip("Copy text to clipboardthen remove from tab page")
		self.pasteAct.setStatusTip("Paste text in clipboard to paself.self.self.self.self.self.self.ge")


		# set Action Checkable
		self.bolden.setCheckable(True)

		# Action Groups go here
		self.syntaxG = QActionGroup(parent)
		syntaxG = self.syntaxG
		# Action Group Specific Actions
		self.pythonSyn = QAction("Python", syntaxG)
		self.plainSyn = QAction("PlainText", syntaxG)

		# Action Group checkable
		self.pythonSyn.setCheckable(True)
		self.plainSyn.setCheckable(True)
