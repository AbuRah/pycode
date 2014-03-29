import sys, os

from PySide.QtGui import (QAction, QMainWindow, QTabWidget, QPlainTextEdit, 
	QFileDialog, QMessageBox, QApplication, QHBoxLayout, QSyntaxHighlighter, 
	QFont, QTextCharFormat, QBrush, QColor, QTextEdit, QShortcut, QListView, 
	QSplitter, QKeySequence, QLineEdit, QDockWidget, QPainter, QDialog, QPalette,
	QPen)

from PySide.QtCore import (QSettings, QFileInfo, QSize, QPoint, QFile, 
	QDir, QIODevice, QRegExp)

from PySide.QtCore import Qt
# from PySide import QtGui

# import Work_Bench

class PyCodeEditor(QMainWindow):

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
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
		exitAct.setShortcutContext(Qt.ApplicationShortcut)
		exitAct.triggered.connect(self.exit_event)

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

		newW = QAction("New Window", self)
		newW.setShortcut("Ctrl+Shift+N")
		newW.triggered.connect(self.new_window)

		openF = QAction("Open", self)
		openF.setShortcut("Ctrl+O")
		openF.setStatusTip("Open a file on the file system")
		openF.triggered.connect(self.open_file_dialog)
		# openF.triggered.connect(self.custom_dialog)

		closeF = QAction("Close File", self)
		closeF.setShortcut("Ctrl+W")
		closeF.setStatusTip("Close current file in tab")
		closeF.triggered.connect(self.close_tab)

		closeW = QAction("Close Window", self)
		closeW.setShortcut("Ctrl+Shift+W")
		closeW.setShortcutContext(Qt.WidgetWithChildrenShortcut)
		closeW.triggered.connect(self.close_window)

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
		cutAct.setStatusTip("Copy text to clipboard, then remove from tab page")
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

		tabW2 = QAction("Tab Width: 2", self)
		tabW2.triggered.connect(self.tab_width2)
		
		tabW4 = QAction("Tab Width: 4", self)
		tabW4.triggered.connect(self.tab_width4)
		
		tabW6 = QAction("Tab Width: 6", self)
		tabW6.triggered.connect(self.tab_width6)
		
		tabW8 = QAction("Tab Width: 8", self)
		tabW8.triggered.connect(self.tab_width8)

		reopenT = QAction("Re-Open last Tab", self)
		reopenT.triggered.connect(self.reopen_last_tab)

		# MENUBAR Specific ==================================================

		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		filemenu.addAction(newF)
		filemenu.addAction(newW)
		filemenu.addAction(reopenT)
		filemenu.addSeparator()
		filemenu.addAction(openF)
		filemenu.addAction(saveAct)
		filemenu.addAction(saveasAct)
		filemenu.addSeparator()
		filemenu.addAction(closeW)
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
		tabwidth = toolmenu.addMenu("Tab Width")
		tabwidth.addAction(tabW2)
		tabwidth.addAction(tabW4)
		tabwidth.addAction(tabW6)
		tabwidth.addAction(tabW8)
		
		preferences = mainbar.addMenu("Preferences")
		
		aboutmenu = mainbar.addMenu("About")

		

		# STATUSBAR =====================================================
		status = self.statusBar()
		status.showMessage("Ready", 4000)
		# status.addPermamentWidget() <--- add syntax indicator here using
		# QLabel or other widget


		# TESTING Area ============================================

		




		# LAYOUT AND FINAL INITIAL SETUP======================================
		self.mainlayout = QHBoxLayout()


		self.tabinterface = QTabWidget(self)
		self.tabinterface.setDocumentMode(True)
		self.tabinterface.setMovable(True)
		self.tabinterface.setTabsClosable(True)
		self.tabinterface.addTab(QPlainTextEdit(self.tabinterface), "Untitled")
		# self.workarea = CustomPlainTextEdit(self.tabinterface)
		# self.tabinterface.addTab(self.workarea, "Untitled")
		self.tabinterface.setElideMode(Qt.ElideRight)

		self.setCentralWidget(self.tabinterface)
		self.tabinterface.currentWidget().setFocus()


		# self.mainlayout.addWidget(self.tabinterface)
		# self.setLayout(self.mainlayout)

		current_workarea = self.tabinterface.currentWidget()
		python_syntax(current_workarea.document())

		# SHORTCUT ====================================================
		# may be able to move by setting parent to mainwindow.This way, i can place it
		# as an ATTR of the main class.

		move_right_between_tabs = QShortcut("Ctrl+pgup", self.tabinterface, 
									self.tab_seek_right)
		move_right_between_tabs.setAutoRepeat(True)


		move_left_between_tabs = QShortcut("Ctrl+pgdn", self.tabinterface, 
									self.tab_seek_left)
		move_left_between_tabs.setAutoRepeat(True)

		move_right_between_tabs = QShortcut("Ctrl+Tab", self.tabinterface, 
									self.tab_seek_right)
		move_right_between_tabs.setAutoRepeat(True)


		move_left_between_tabs = QShortcut("Ctrl+Shift+Tab", self.tabinterface, 
									self.tab_seek_left)
		move_left_between_tabs.setAutoRepeat(True)
		
		close_active_window = QShortcut("Ctrl+Shift+W", self.tabinterface,
									self.close_window, Qt.WidgetShortcut)

	# TESTING Area for methods ================================================








# SLOTS
# ===================================================================================================		

	def open_file_dialog(self):
		"""opens file in new tab"""

		filename,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if filename != '':

			f = open(filename, "r")
			new_workarea = QPlainTextEdit(self.tabinterface)
			python_syntax(new_workarea.document())

			
			with f:
				
				data = f.read()
				new_workarea.setPlainText(data)

				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.tabinterface.addTab(new_workarea, nameOfFile)
				f.close()
				
		else:
			pass
	
	def close_tab(self):
		"""Closes focused tab"""
		currentTabIndex = self.tabinterface.currentIndex()
		return self.tabinterface.removeTab(currentTabIndex)
	
	def new_file(self):
		"""Opens a plain rich-text document"""
		# replace the hard-coded python_syntax with a variable that will 
		# change depending upon user preference

		new_workarea = QPlainTextEdit(self.tabinterface)
		python_syntax(new_workarea.document())
		new_workarea.setFocus()
		return self.tabinterface.addTab(new_workarea, "Untitled")

	def save_event(self):
		"""Saves file with current tab title text, no prompting"""

		filename = self.tabinterface.tabText(self.tabinterface.currentIndex())		
		

		save_file = QFile(filename)


		save_file_name = QFile.fileName(save_file)


		if save_file_name != "Untitled":
			f = open(save_file_name, "w")

			with f:


				focusedPage = self.tabinterface.currentWidget()
				changes = focusedPage.toPlainText()
				f.write(changes)
				f.close()
		
		else:
			return self.save_file_as()


	def save_file_as(self):
		"""Save current file as"""

		filename, _ = QFileDialog.getSaveFileName(self,
			"Save File", os.getcwd())


		if filename != '':

			f = open(filename, "w")

			with f:

				focusedPage = self.tabinterface.currentWidget()
				changes = focusedPage.toPlainText()
				
				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.tabinterface.setTabText(self.tabinterface.currentIndex(),
											 nameOfFile)


				updated_data = f.write(changes)
				f.close()
		
		else:
			pass

	def cut_selection(self):
		"""copy/cut selected text"""
		currentPage = self.tabinterface.currentWidget()
	
		currentPage.cut()
	
	def find_text(self):
		"""Find the indicated text within the current tab page"""
		### need to add a dialog window OR a pop-up bar for user input

		user_input = QLineEdit(self)
		user_input.setFrame(False)
		main_dock_widget = QDockWidget(self)
		main_dock_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
		main_dock_widget.setWidget(user_input)
		self.addDockWidget(Qt.BottomDockWidgetArea, main_dock_widget)
		user_input.setFocus()

		# user_input.textChanged(): # <- signal emitted when text field changes
		current_tab = self.tabinterface.currentWidget()
		# current_tab_doc = current_tab.document()
		current_tab.find(user_input.text())

	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.paste()

	def custom_dialog(self):
		"""Working on Custom File Dialog Here"""
		dialog = QFileDialog(self)
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setViewMode(QFileDialog.list)
		
		if dialog.exec_():
			filenames = dialog.selectedFiles()

	def undo_last(self):
		"""Steps back in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		currentTab = self.tabinterface.currentWidget()
		currentTab.redo()

	def exit_event(self):
		"""Exits without prompting"""
		self.write_settings()
		self.close()

	def exit_message(self):
		"""Causes a message box specific to closing"""

		ask = QMessageBox.question(self, "WARNING!",
			"Are You Sure You Want To Quit?",
			QMessageBox.Yes | QMessageBox.No, 
			QMessageBox.No)

		if ask == QMessageBox.Yes:
			self.write_settings()
			self.close()
		
		else:
			pass

	def tab_seek_right(self):
		"""Moves focus one tab to the right, back to start if at the end"""

		total_open_tabs = self.tabinterface.count()

		focused_tab_index = self.tabinterface.currentIndex()

		if focused_tab_index == total_open_tabs - 1:
			focused_tab_index = 0

		else:
			focused_tab_index += 1

		widget_at_index = self.tabinterface.widget(focused_tab_index)
		return self.tabinterface.setCurrentWidget(widget_at_index)

	def tab_seek_left(self):
		"""Moves focus one tab to the left, moves to end if at the start"""

		total_open_tabs = self.tabinterface.count()

		focused_tab_index = self.tabinterface.currentIndex()

		if focused_tab_index == 0:
			focused_tab_index = total_open_tabs - 1

		else:
			focused_tab_index -= 1


		widget_at_index = self.tabinterface.widget(focused_tab_index)
		return self.tabinterface.setCurrentWidget(widget_at_index)


	def new_window(self):
		"""creates a complete new window."""
		self.new_window_instance = NewWindow(self)
		self.new_window_instance.setWindowTitle("PyCode Text EditorX")

	def close_window(self):
		"""Close active window"""
		return self.close()

	def tab_width2(self):
		return self.tabinterface.currentWidget().setTabStopWidth(20)
	
	def tab_width4(self):
		return self.tabinterface.currentWidget().setTabStopWidth(40)
	
	def tab_width6(self):
		return self.tabinterface.currentWidget().setTabStopWidth(60)
	
	def tab_width8(self):
		return self.tabinterface.currentWidget().setTabStopWidth(80)

	def reopen_last_tab(self):
		pass


# SETTINGS/STATE SLOTS ========================================================

	def write_settings(self):
		"""Writes the current user settings"""
		self.settings = QSettings(QSettings.UserScope, 
						"Auto-didactic Engineering", "PyCode The Editor")

		self.settings.beginGroup("Main Window")
		self.settings.setValue("Geometry", self.saveGeometry())
		self.settings.setValue("Window State", self.saveState())
		self.settings.endGroup()


	def read_settings(self):
		"""Loads the saved settings from a previous session"""
		self.settings = QSettings("Auto-didactic Engineering", 
									"PyCode The Editor")

		self.settings.beginGroup("Main Window")
		self.restoreGeometry(self.settings.value("Geometry"))
		self.restoreState(self.settings.value("Window State"))
		self.settings.endGroup()

# QDialog Classes ===============================================

class NewWindow(PyCodeEditor):

	def __init__(self, parent=None):
		super(NewWindow, self).__init__(parent)
		self.initUI()
		self.setGeometry(100, 100, 800, 500)
		self.show()

class CustomPlainTextEdit(QPlainTextEdit):
	def __init__(self, parent=None):
		super(CustomPlainTextEdit, self).__init__(parent)

		# palette = QPalette(self.palette())
		# palette.setColor(palette.Background, Qt.transparent)

		# self.setPalette(palette)
	
	# # qp.begin(self)
	# qp.setRenderHint(QPainter.Antialiasing)
	# qp.setPen(QPen(Qt.NoPen))
	# qp.end()
	def update_test(self):
		qp = QPainter(self)
		self.update(qp.fillRect(self.rect(), QBrush(Qt.transparent)))
	

	# def paintEvent(self, e):
	# 	qp = QPainter(self)
	# 	qp.begin(self)
	# 	qp.setRenderHint(QPainter.Antialiasing)
	# 	qp.fillRect(self.rect(), QBrush(Qt.transparent))
	# 	qp.setPen(QPen(Qt.NoPen))
	# 	qp.end()

# Syntax Highlighting CLASSES ================================================================

class python_syntax(QSyntaxHighlighter):
	""" Highlights regular python syntax"""
	
	#!!! going to need to create a custom search for class, def, etc. keywords.
	bergundy_color = QColor("#800020")
	amber_color = QColor("#ffbf00")

	python_basic_keywords = ["for", "in", "while", "print"]

	# This will hold all well builtin function keywords

	python_builtin_function_keywords = ["abs",	"divmod", "input", "open"]
						# "staticmethod",	"all", "enumerate", "int", "ord", 
						# "str", "any", "eval", "isinstance", "pow", "sum", 
						# "basestring", "execfile", "issubclass", "print", 
						# "super", "bin", "file", "iter", "property", 
						# "tuple", "bool", "filter", "len", "range", "type", 
						# "bytearray", "float", "list", "raw_input", "unichr",
						# "callable", "format", "locals", "reduce", "unicode",
						# "chr", "frozenset", "long", "reload", "vars",
						# "classmethod", "getattr", "map", "repr", "xrange",
						# "cmp", "globals", "max", "reversed", "zip",
						# "compile", "hasattr", "memoryview", "round", 
						# "__import__", "complex", "hash", "min", "set", 
						# "apply", "delattr", "help", "next", "setattr", 
						# "buffer", "dict", "hex", "object", "slice", "coerce",
						# "dir", "id", "oct", "sorted", "intern"]

	def highlightBlock(self, text):
	
		python_basic_format = QTextCharFormat()
		python_basic_format.setFontWeight(QFont.Bold)
		python_basic_format.setForeground(self.amber_color)
		
		for i in self.python_basic_keywords:
			expression = QRegExp("\\b" + i +"\\b")
			index = expression.indexIn(text)
		
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, python_basic_format)
				index = expression.indexIn(text, index + length)


		# !!!! Same as Below with Comment code; this will Freeze the program
		# need to fix.

		# python_builtin_format = QTextCharFormat()
		# python_builtin_format.setFontWeight(QFont.Bold)
		# python_builtin_format.setForeground(self.amber_color)

		# for i in self.python_builtin_function_keywords:
		# 	expression = QRegExp("\\b" + i + "()\\b")
		# 	index = expression.indexIn(text)

		# 	while index >= 0:
		# 		length = expression.matchedLength()
		# 		self.setFormat(index, length, python_builtin_format)
		# 		index = expression.indexIn(text)

		# python long comment form;! CURRENTLY CAUSES AN INFINITE LOOP; Buggy


		# python_commentL_format = QTextCharFormat()
		# python_commentL_format.setFontWeight(QFont.Bold)
		# python_commentL_format.setBackground(self.amber_color)
		# start_pattern = QRegExp("\"\"\"")
		# end_pattern = QRegExp("\"\"\"")
		# commentLength = 0
		
		# self.setCurrentBlockState(0)

		# startIndex= 0
		# if self.previousBlockState() != 1:
		# 	startIndex = start_pattern.indexIn(text)

		# while startIndex >= 0:
		# 	endIndex = end_pattern.indexIn(text, startIndex)
		# 	if endIndex == -1:
		# 		self.setCurrentBlockState(1)
		# 		commentLength = text.length() - startIndex
		# 	else:
		# 		commentLength = (endIndex - startIndex
		# 			+ end_pattern.matchedLength())

		# self.setFormat(startIndex, commentLength, python_commentL_format)
		# startIndex = start_pattern.indexIn(text,
		# 	startIndex + commentLength)












#===========================================================================================
def main():
	pycodeapp = QApplication(sys.argv)
	# pycodeapp.setStyle("plastique")
	editor = PyCodeEditor()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
