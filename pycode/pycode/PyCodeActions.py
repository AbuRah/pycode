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
		self.openrecentAct = QAction("Open Recent File", parent)
		self.reopenT = QAction("Re-Open last Tab", parent)
		self.saveallAct = QAction("Save All Files", parent)
		self.closeallAct = QAction("Close All Files", parent)

		#for edit menu
		self.pasteAct = QAction("Paste", parent)
		self.redoAct = QAction("Redo", parent)
		self.cutAct = QAction("Cut", parent)
		self.undoAct = QAction("Undo", parent)
		self.bolden = QAction("Bold", parent)
		self.copyAct = QAction("Copy", parent)
		self.findAct = QAction("Find", parent)
		self.findRegExp = QAction("RegExp Find", parent)
		self.findR = QAction("Find && Replace", parent)
		self.cloneAct = QAction("Clone", parent)

		# for tool menu
		self.snippets = QAction("Code Snippets", parent)
		self.buildAct = QAction("Commence Build", parent)
		self.tabW2 = QAction("Tab Width: 2", parent)
		self.tabW4 = QAction("Tab Width: 4", parent)
		self.tabW6 = QAction("Tab Width: 6", parent)
		self.tabW8 = QAction("Tab Width: 8", parent)

		# for view menu
		self.plainL = QAction("Single Layout", parent)
		self.splitL = QAction("Two Windows", parent)
		self.gridL = QAction("Four windows", parent)

		self.pythonSyn = QAction("Python", parent)
		self.plainSyn = QAction("PlainText", parent)
		self.htmlSyn = QAction("HTML", parent)
		self.status_hideAct = QAction("Hide StatusBar", parent)

		# for perferences Menu
		self.setfontI = QAction("Font Size Increase", parent)
		self.setfontD = QAction("Font Size Decrease", parent)
		self.setfontS = QAction("Serif", parent)
		self.setfontM = QAction("monospace", parent)
		self.setfontSS = QAction("Sans-Serif", parent)
		self.setinverse = QAction("Inverse Theme", parent)

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
		self.undoAct.setShortcut("Ctrl+Z")
		self.reopenT.setShortcut("Ctrl+Shift+T")
		self.findR.setShortcut("Ctrl+F")
		self.redoAct.setShortcut("Ctrl+Shift+Z")
		self.pasteAct.setShortcut("Ctrl+V")
		self.cutAct.setShortcut("Ctrl+X")
		self.setfontI.setShortcut("Ctrl+=")
		self.setfontD.setShortcut("Ctrl+-")


		# shorcut Contexts
		self.closeW.setShortcutContext(Qt.WidgetShortcut)



		# status Tips go here

		self.exitAct.setStatusTip("Exit the Application")
		self.saveAct.setStatusTip("Save Current Document")
		self.saveasAct.setStatusTip("Save file as...")
		self.newF.setStatusTip("Create New document")
		self.openF.setStatusTip("Open a file on the file system")
		self.openrecentAct.setStatusTip("Open Recent File")
		self.closeF.setStatusTip("Close current file in tab")
		self.bolden.setStatusTip("bold selected text")
		self.copyAct.setStatusTip("copy current Selection")
		self.findAct.setStatusTip("Find indicated text within current document")
		self.cutAct.setStatusTip("Remove && Copy text to clipboard")
		self.pasteAct.setStatusTip("Paste text in clipboard to page")
		self.status_hideAct.setStatusTip("Hide the statusbar from view")
		self.saveallAct.setStatusTip("Save all open files")
		self.closeallAct.setStatusTip("Closes all open files")
		self.cloneAct.setStatusTip("Clones Current Document")
		self.setinverse.setStatusTip("Inverses current Theme colors")
		self.buildAct.setStatusTip("Build from specified engine")
		self.snippets.setStatusTip("search code snippets")

		# set Action Checkable
		self.bolden.setCheckable(True)
		self.status_hideAct.setCheckable(True)
		self.tabW2.setCheckable(True)
		self.tabW4.setCheckable(True)
		self.tabW6.setCheckable(True)
		self.tabW8.setCheckable(True)

		#action Groups
		self.layout_group = QActionGroup(parent)
		self.layout_group.addAction(self.plainL)
		self.layout_group.addAction(self.splitL)
		self.layout_group.addAction(self.gridL)

		self.tab_group = QActionGroup(parent)
		self.tab_group.addAction(self.tabW2)
		self.tab_group.addAction(self.tabW4)
		self.tab_group.addAction(self.tabW6)
		self.tab_group.addAction(self.tabW8)