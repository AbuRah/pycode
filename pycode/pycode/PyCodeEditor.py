import sys, os, time
from exceptions import IOError, AttributeError

from PySide.QtCore import *
from PySide.QtGui import *

from SyntaxClasses import *
from PyCodeActions import *
from PyCodeShortcuts import *
from functools import partial
import re


class PyCodeEditor(QMainWindow):
	
	_CLOSED_TAB_LIST = []
	_SYNTAX_DICT = {}
	# _EXTENSIONS = {".py": "PythonSyntax"}

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
		self.initUI()
		self.settings = None
		self.setStyleSheet("""QStatusBar::item{border: none;}""")
		self.setWindowTitle("PyCode Text Editor")

	def initUI(self):


		self.ALL_ACTIONS = PyCodeActions(self)
		self.EXT = Extensions()
		self.EXTENSIONS_LIST = self.EXT.EXT_LIST
		self.TAB_INTERFACE = QTabWidget(self)
		self.TAB_INTERFACE.setDocumentMode(True)
		self.TAB_INTERFACE.setMovable(True)
		self.TAB_INTERFACE.setTabsClosable(True)
		self.TAB_INTERFACE.setElideMode(Qt.ElideRight)
		self.TAB_INTERFACE.setFocusPolicy(Qt.NoFocus)
		self.TAB_INTERFACE.addTab(QPlainTextEdit(self.TAB_INTERFACE), "Untitled")
		self.TAB_INTERFACE.currentWidget().setFocus()
	
		self.CURRENT_TEXT_EDIT = self.TAB_INTERFACE.currentWidget()
		self.CURRENT_TEXT_DOC = self.CURRENT_TEXT_EDIT.document()
		self.CURRENT_TEXT_CURSOR = self.CURRENT_TEXT_EDIT.textCursor()
		self.CURRENT_INDEX = self.TAB_INTERFACE.currentIndex()


		self.setCentralWidget(self.TAB_INTERFACE)

# QAction Signals and connections===============================================
		ALL_ACTIONS = self.ALL_ACTIONS
		ALL_ACTIONS.exitAct.triggered.connect(self.exit_event)
		ALL_ACTIONS.saveAct.triggered.connect(self.save_event)
		ALL_ACTIONS.saveasAct.triggered.connect(self.save_file_as)
		ALL_ACTIONS.newF.triggered.connect(self.new_file)
		ALL_ACTIONS.newW.triggered.connect(self.new_window)
		ALL_ACTIONS.openF.triggered.connect(self.open_file_dialog)
		ALL_ACTIONS.cutAct.triggered.connect(self.cut_selection)
		ALL_ACTIONS.pasteAct.triggered.connect(self.paste_selection)
		ALL_ACTIONS.redoAct.triggered.connect(self.redo_last)
		ALL_ACTIONS.undoAct.triggered.connect(self.undo_last)
		ALL_ACTIONS.tabW2.triggered.connect(partial(self.set_tab_width, 20))
		ALL_ACTIONS.tabW4.triggered.connect(partial(self.set_tab_width, 40))
		ALL_ACTIONS.tabW6.triggered.connect(partial(self.set_tab_width, 60))
		ALL_ACTIONS.tabW8.triggered.connect(partial(self.set_tab_width, 80))
		ALL_ACTIONS.reopenT.triggered.connect(self.reopen_last_tab)
		ALL_ACTIONS.closeF.triggered.connect(self.close_tab)
		ALL_ACTIONS.closeW.triggered.connect(self.close_window)
		ALL_ACTIONS.findAct.triggered.connect(self.find_text)

		ALL_ACTIONS.pythonSyn.triggered.connect(self.python_syntax)
		ALL_ACTIONS.plainSyn.triggered.connect(self.plain_text)
		ALL_ACTIONS.htmlSyn.triggered.connect(self.html_syntax)

		
		
		self.TAB_INTERFACE.tabCloseRequested.connect(self.close_tab)
		self.CURRENT_TEXT_EDIT.cursorPositionChanged.connect(self.column_line_update)
		self.TAB_INTERFACE.currentChanged.connect(self.set_file_and_status_bar)



# MENUBAR Specific ==================================================
		# CREATE MENUS HERE
		self.mainbar = self.menuBar()
		filemenu = self.mainbar.addMenu("&File")
		editmenu = self.mainbar.addMenu("Edit")
		viewmenu = self.mainbar.addMenu("View")
		toolmenu = self.mainbar.addMenu("Tools")
		preferences = self.mainbar.addMenu("Preferences")
		
		# FILE MENU
		filemenu.addAction(ALL_ACTIONS.newF)
		filemenu.addAction(ALL_ACTIONS.newW)
		filemenu.addAction(ALL_ACTIONS.reopenT)
		filemenu.addSeparator()
		filemenu.addAction(ALL_ACTIONS.openF)
		filemenu.addAction(ALL_ACTIONS.saveAct)
		filemenu.addAction(ALL_ACTIONS.saveasAct)
		filemenu.addSeparator()
		filemenu.addAction(ALL_ACTIONS.closeW)
		filemenu.addAction(ALL_ACTIONS.closeF)
		filemenu.addAction(ALL_ACTIONS.exitAct)
		
		#EDIT MENU
		editmenu.addAction(ALL_ACTIONS.findAct)
		editmenu.addSeparator()
		editmenu.addAction(ALL_ACTIONS.copyAct)
		editmenu.addAction(ALL_ACTIONS.cutAct)
		editmenu.addAction(ALL_ACTIONS.pasteAct)
		editmenu.addAction(ALL_ACTIONS.redoAct)
		editmenu.addAction(ALL_ACTIONS.undoAct)
		editmenu.addSeparator()
		editmenu.addAction(ALL_ACTIONS.bolden)

		# VIEW MENU
		layoutmenu = viewmenu.addMenu("Layouts")
		syntaxmenu = viewmenu.addMenu("syntax")

		layoutmenu.addAction(ALL_ACTIONS.plainL)
		layoutmenu.addAction(ALL_ACTIONS.splitL)
		layoutmenu.addAction(ALL_ACTIONS.gridL)
		viewmenu.addSeparator()
		syntaxmenu.addAction(ALL_ACTIONS.pythonSyn)
		syntaxmenu.addAction(ALL_ACTIONS.plainSyn)
		syntaxmenu.addAction(ALL_ACTIONS.htmlSyn)

		# TOOL MENU
		tabwidth = toolmenu.addMenu("Tab Width")
		
		tabwidth.addAction(ALL_ACTIONS.tabW2)
		tabwidth.addAction(ALL_ACTIONS.tabW4)
		tabwidth.addAction(ALL_ACTIONS.tabW6)
		tabwidth.addAction(ALL_ACTIONS.tabW8)
		
# STATUSBAR =====================================================
		self.status = self.statusBar()
		self.status.showMessage("Ready?", 4000)
		
		self.line_count = QLabel("Line: 1, Column: 1")
		self.current_syntax = QLabel("")
		self.status.addPermanentWidget(self.line_count)
		self.status.addPermanentWidget(self.current_syntax)

# DockWidget Area ==============================================================

		# this is broken at the moment		
		self.main_dock_widget = QDockWidget(self)
		self.main_dock_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
		self.main_dock_widget.setFloating(False)
		self.main_dock_widget.setObjectName('Main Dock')
		self.addDockWidget(Qt.BottomDockWidgetArea, self.main_dock_widget)
		self.user_input = QLineEdit(self)
		self.main_dock_widget.hide()
		self.main_dock_widget.setWidget(self.user_input)

		self.user_input.returnPressed.connect(self.select_current_text)
		self.user_input.textChanged.connect(self.find_text)

# SHORTCUT ==================================================================
		ALL_SHORTCUTS = PyCodeShortcuts(self.TAB_INTERFACE)
		ALL_SHORTCUTS.move_right_between_tabs.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.move_left_between_tabs.activated.connect(self.tab_seek_left)
		ALL_SHORTCUTS.move_right_between_tabs2.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.close_active_window.activated.connect(self.close_window)
		ALL_SHORTCUTS.close_dock.activated.connect(self.main_dock_widget.hide)
		
# SLOTS ========================================================================
	
	def set_file_and_status_bar(self):
		"""Make all menu and statubs bar options reflect current document"""
		ALL_ACTIONS = self.ALL_ACTIONS
		self.CURRENT_INDEX = self.TAB_INTERFACE.currentIndex()
		self.CURRENT_TEXT_EDIT = self.TAB_INTERFACE.currentWidget()

		try:
			self.CURRENT_TEXT_CURSOR = self.CURRENT_TEXT_EDIT.textCursor()
			self.CURRENT_TEXT_DOC = self.CURRENT_TEXT_EDIT.document()
			self.CURRENT_TEXT_DOC.contentsChanged.connect(self.modified_since_save)
			self.CURRENT_TEXT_EDIT.cursorPositionChanged.connect(self.column_line_update)
		except AttributeError:
			print "no tab_page available"

		# to be removed after testings
		self.get_extension()
		try:
			self.current_syntax.setText(self._SYNTAX_DICT.get(self.CURRENT_INDEX))
			
		except ValueError, KeyError:
			print "Key or Value missing from Syntax Dict"

#INTERNAL SLOTS=================================================================
	def tab_seek_right(self):
		"""Moves focus one tab to the right, back to start if at the end"""

		total_tabs = self.TAB_INTERFACE.count()

		if self.CURRENT_INDEX == total_tabs - 1:
			self.CURRENT_INDEX = 0

		else:
			self.CURRENT_INDEX += 1

		widget_at_index = self.TAB_INTERFACE.widget(self.CURRENT_INDEX)
		return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)

	def tab_seek_left(self):
		"""Moves focus one tab to the left, moves to end if at the start"""

		total_tabs = self.TAB_INTERFACE.count()

		if self.CURRENT_INDEX == 0:
			self.CURRENT_INDEX = total_tabs - 1

		else:
			self.CURRENT_INDEX -= 1


		widget_at_index = self.TAB_INTERFACE.widget(self.CURRENT_INDEX)
		return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)

	def modified_since_save(self):
		"""Causes tab text to change if modified since last save"""
		current_index = self.TAB_INTERFACE.currentIndex()
		return self.TAB_INTERFACE.tabBar().setTabTextColor(current_index,
												 QColor("#fff5ee"))

	def column_line_update(self):
		"""updates current cursor position in document"""
		CURRENT_TEXT_CURSOR = self.TAB_INTERFACE.currentWidget().textCursor()
		return self.line_count.setText("Line: %d, Column: %d" % (
			CURRENT_TEXT_CURSOR.blockNumber()+1, CURRENT_TEXT_CURSOR.columnNumber()+1))

	def select_current_text(self):
		"""Selects text in find bar when enter is pressed"""
		self.user_input.setSelection(0, len(self.user_input.text()))

	def get_extension(self):
		"""Looks for the file file extension and sets appropriate syntax"""
		file_name = self.TAB_INTERFACE.tabBar().tabText(self.CURRENT_INDEX)
		if "." in file_name:
			point = file_name.index(".")
			extension = file_name[point:]

			if self.EXTENSIONS_LIST.get(extension):
				self.EXTENSIONS_LIST.get(extension)(self.CURRENT_TEXT_DOC)
			else:
				pass
		else:
			self.plain_text()

# FILEMENU SLOTS===============================================================
	def open_file_dialog(self):
		"""opens file in new tab"""

		filename,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if filename != '':

			with open(filename, "r") as f:
				
				data = f.read()
				new_page = QPlainTextEdit(self.TAB_INTERFACE)
				new_page.setPlainText(data)

				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.TAB_INTERFACE.addTab(new_page, nameOfFile)
				f.close()
				
		else:
			pass
	
	def close_tab(self):
		"""Closes focused tab"""
		current_index = self.TAB_INTERFACE.currentIndex()
		self._CLOSED_TAB_LIST.append(self.TAB_INTERFACE.tabText(current_index))
		
		self.TAB_INTERFACE.removeTab(current_index)

		try:
			return self.TAB_INTERFACE.currentWidget().setFocus()
		
		except AttributeError:
			pass
	
	def new_file(self):
		"""Opens a plain rich-text document"""

		new_page = QPlainTextEdit(self.TAB_INTERFACE)
		PlainText(new_page.document())
		self.TAB_INTERFACE.addTab(new_page, "Untitled")
		self.set_file_and_status_bar
		self.CURRENT_TEXT_EDIT.setFocus()


	def new_window(self):
		"""opens a completely new window."""
		self.new_window_instance = PyCodeEditor()
		return self.new_window_instance.show()


	def close_window(self):
		"""Close active window"""
		return self.close()
	
	def reopen_last_tab(self):
		"""Opens the last tab closed"""

		if len(self._CLOSED_TAB_LIST) > 0:

			new_page = QPlainTextEdit(self.TAB_INTERFACE)
			last_file = self._CLOSED_TAB_LIST.pop()

			try:

				with open(last_file, "r") as f:
					data = f.read()
					new_page.setPlainText(data)
		
					self.TAB_INTERFACE.addTab(new_page, last_file)
					self.CURRENT_TEXT_EDIT.setFocus()
		
			except IOError:
				pass

		else:
			pass

	def save_event(self):
		"""Saves file with current tab title text, no prompting"""

		filename = self.TAB_INTERFACE.tabText(self.TAB_INTERFACE.currentIndex())		
		save_file = QFile(filename)
		save_file_name = QFile.fileName(save_file)

		if save_file_name != "Untitled":
			f = open(save_file_name, "w")

			with f:
				# focusedPage = self.TAB_INTERFACE.currentWidget()
				changes = self.CURRENT_TEXT_EDIT.toPlainText()
				f.write(changes)
				f.close()
				current_index = self.CURRENT_INDEX
				return self.TAB_INTERFACE.tabBar().setTabTextColor(current_index,
												 QColor("#848482"))

		else:
			return self.save_file_as()

	def save_file_as(self):
		"""Save current file as"""

		filename, _ = QFileDialog.getSaveFileName(self,
			"Save File", os.getcwd())


		if filename != '':

			f = open(filename, "w")

			with f:

				focusedPage = self.TAB_INTERFACE.currentWidget()
				changes = focusedPage.toPlainText()
				
				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.TAB_INTERFACE.setTabText(self.TAB_INTERFACE.currentIndex(),
											 nameOfFile)


				updated_data = f.write(changes)
				f.close()
		
		else:
			pass
	def exit_event(self):
		"""Exits without prompting"""
		self.write_settings()
		sys.exit()

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

# EDIT MENU SLOTS =============================================================
	def cut_selection(self):
		"""copy/cut selected text"""
		return self.CURRENT_TEXT_EDIT.cut()

	def find_text(self):
		"""Find the indicated text within the current tab page"""
		### need to add auto-complete, find & replace
		self.main_dock_widget.show()
		self.user_input.setFocus()

		_TESTING = QTextCursor(self.CURRENT_TEXT_CURSOR)
		
		if self.CURRENT_TEXT_CURSOR.position() != 0:
			update = self.CURRENT_TEXT_DOC.find(self.user_input.text())
			self.CURRENT_TEXT_EDIT.setTextCursor(update)
			self.CURRENT_TEXT_CURSOR.select(QTextCursor.WordUnderCursor)

		

	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		return self.CURRENT_TEXT_EDIT.paste()

	def undo_last(self):
		"""Steps back in operation history"""
		return self.CURRENT_TEXT_EDIT.undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		return self.CURRENT_TEXT_EDIT.redo()

# VIEW MENU SLOTS ==============================================================
	def set_tab_width(self, num):
		return self.CURRENT_TEXT_EDIT.setTabStopWidth(num)

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.CURRENT_TEXT_DOC)
		self._SYNTAX_DICT[self.CURRENT_INDEX] = "Python"
		self.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.CURRENT_TEXT_DOC)
		self._SYNTAX_DICT[self.CURRENT_INDEX] = "PlainText"
		self.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.CURRENT_TEXT_DOC)
		self._SYNTAX_DICT[self.CURRENT_INDEX] = "HTML"
		self.current_syntax.setText("HTML") 

# SETTINGS/STATE SLOTS ========================================================

	def write_settings(self):
		"""Writes the current user settings"""
		self.settings = QSettings(QSettings.UserScope, 
						"Auto-didactic Engineering", "PyCode The Editor")

		files = [self.TAB_INTERFACE.tabText(i) for i in xrange(self.TAB_INTERFACE.count())]
		
		self.settings.beginGroup("Main Window")
		self.settings.beginWriteArray("files")
		for i in xrange(len(files)):
			self.settings.setArrayIndex(i)
			self.settings.setValue("filename", files[i] )
		self.settings.endArray()
		self.settings.setValue("Position", self.pos())
		self.settings.setValue("Size", self.size())
		# self.settings.setValue("")
		# self.settings.setValue("Window State", self.saveState())
		self.settings.endGroup()


	def read_settings(self):
		"""Loads the saved settings from a previous session"""
		self.settings = QSettings("Auto-didactic Engineering", 
									"PyCode The Editor")

		self.settings.beginGroup("Main Window")
		
		size = self.settings.beginReadArray("files")
		
		for i in xrange(size):
			self.settings.setArrayIndex(i)
			tabname = self.settings.value("filename")
			try:
				with open(tabname, "r") as f:
					data = f.read()
					new_page = QPlainTextEdit(self.TAB_INTERFACE)
					new_page.setPlainText(data)
					self.TAB_INTERFACE.addTab(new_page, tabname)
					f.close()
			except IOError:
				pass

		self.settings.endArray()
		self.move(self.settings.value("Position"))
		self.resize(self.settings.value("Size"))
		# self.restoreState(self.settings.value("Window State"))
		self.settings.endGroup()

#MAIN =========================================================================
def main():
	pycodeapp = QApplication(sys.argv)

	try:
		with open("PyCodeThemes/PyCodeCrimson.qss") as f:
			stylesheet = f.read()
			pycodeapp.setStyleSheet(stylesheet)
	
	except IOError:
		print "Cannot find Stylesheet; falling back to native style"

	editor = PyCodeEditor()
	# need to put a try/except statement here
	editor.read_settings()
	editor.show()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
