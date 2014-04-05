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
	_RECENTLY_OPENED = []
	_SYNTAX_DICT = {}

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
		self.initUI()
		self.setStyleSheet("""QStatusBar::item{border: none;}""")
		self.setWindowTitle("PyCode Text Editor")

	def initUI(self):

		# self.settings = QSettings(QSettings.UserScope, 
		# 				"AD Engineering", "PyCode Text Editor")

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

		# test_layout2 = QHBoxLayout(self)
		# test_layout2.addWidget(self.TAB_INTERFACE)
		self.setCentralWidget(self.TAB_INTERFACE)

# QAction Signals and connections===============================================
		ALL_ACTIONS = self.ALL_ACTIONS
		ALL_ACTIONS.exitAct.triggered.connect(self.exit_event)
		ALL_ACTIONS.saveAct.triggered.connect(self.save_event)
		ALL_ACTIONS.saveasAct.triggered.connect(self.save_file_as)
		ALL_ACTIONS.newF.triggered.connect(self.new_file)
		ALL_ACTIONS.newW.triggered.connect(self.new_window)
		ALL_ACTIONS.openF.triggered.connect(self.open_file_dialog)
		ALL_ACTIONS.saveallAct.triggered.connect(self.save_all)
		ALL_ACTIONS.closeallAct.triggered.connect(self.close_all)
		ALL_ACTIONS.reopenT.triggered.connect(self.reopen_last_tab)
		ALL_ACTIONS.closeF.triggered.connect(self.close_tab)
		ALL_ACTIONS.closeW.triggered.connect(self.close_window)

		ALL_ACTIONS.findAct.triggered.connect(self.find_text)
		# ALL_ACTIONS.findRegExp.triggered.connect(self.find_regexp)
		ALL_ACTIONS.redoAct.triggered.connect(self.redo_last)
		ALL_ACTIONS.undoAct.triggered.connect(self.undo_last)
		ALL_ACTIONS.cutAct.triggered.connect(self.cut_selection)
		ALL_ACTIONS.pasteAct.triggered.connect(self.paste_selection)
		ALL_ACTIONS.cloneAct.triggered.connect(self.clone_doc)
		
		ALL_ACTIONS.tabW2.triggered.connect(partial(self.set_tab_width, 20))
		ALL_ACTIONS.tabW4.triggered.connect(partial(self.set_tab_width, 40))
		ALL_ACTIONS.tabW6.triggered.connect(partial(self.set_tab_width, 60))
		ALL_ACTIONS.tabW8.triggered.connect(partial(self.set_tab_width, 80))

		ALL_ACTIONS.status_hideAct.triggered.connect(self.hide_statusbar)
		ALL_ACTIONS.pythonSyn.triggered.connect(self.python_syntax)
		ALL_ACTIONS.plainSyn.triggered.connect(self.plain_text)
		ALL_ACTIONS.htmlSyn.triggered.connect(self.html_syntax)
		ALL_ACTIONS.plainL.triggered.connect(self.plain_layout)
		ALL_ACTIONS.splitL.triggered.connect(self.split_screen_layout)
		ALL_ACTIONS.gridL.triggered.connect(self.grid_layout)

		ALL_ACTIONS.setfontI.triggered.connect(self.increase_font_size)
		ALL_ACTIONS.setfontD.triggered.connect(self.decrease_font_size)
		ALL_ACTIONS.setfontS.triggered.connect(self.set_serif)
		ALL_ACTIONS.setfontM.triggered.connect(self.set_monospace)
		ALL_ACTIONS.setfontSS.triggered.connect(self.set_sansserif)

		self.TAB_INTERFACE.tabCloseRequested.connect(self.close_tab)
		
		self.TAB_INTERFACE.currentChanged.connect(self.set_file_and_status_bar)

		self.GET_TEXT_EDIT().cursorPositionChanged.connect(self.column_line_update)
		self.GET_TEXT_EDIT().textChanged.connect(self.modified_since_save)



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
		filemenu.addAction(ALL_ACTIONS.saveallAct)
		self.recent_files_menu = filemenu.addMenu("Open Recent")
		recent_files_menu = self.recent_files_menu

		recent_files_menu.addAction(ALL_ACTIONS.openrecentAct)
		recent_files_menu.addSeparator()
		recent_files_menu.setDisabled(True)
		# need to be able to open indicated file whenever triggered
		# recent_files_menu.triggered.connect(self.open_file)

		filemenu.addSeparator()
		filemenu.addAction(ALL_ACTIONS.closeW)
		filemenu.addAction(ALL_ACTIONS.closeF)
		filemenu.addAction(ALL_ACTIONS.closeallAct)
		filemenu.addAction(ALL_ACTIONS.exitAct)
		
		#EDIT MENU
		editmenu.addAction(ALL_ACTIONS.findAct)
		editmenu.addAction(ALL_ACTIONS.findRegExp)
		editmenu.addSeparator()
		editmenu.addAction(ALL_ACTIONS.undoAct)
		editmenu.addAction(ALL_ACTIONS.redoAct)
		editmenu.addSeparator()
		editmenu.addAction(ALL_ACTIONS.cloneAct)
		editmenu.addAction(ALL_ACTIONS.copyAct)
		editmenu.addAction(ALL_ACTIONS.cutAct)
		editmenu.addAction(ALL_ACTIONS.pasteAct)
		editmenu.addSeparator()
		editmenu.addAction(ALL_ACTIONS.bolden)

		# VIEW MENU
		viewmenu.addAction(ALL_ACTIONS.status_hideAct)
		viewmenu.addSeparator()
		layoutmenu = viewmenu.addMenu("Layouts")
		layoutmenu.addAction(ALL_ACTIONS.plainL)
		layoutmenu.addAction(ALL_ACTIONS.splitL)
		layoutmenu.addAction(ALL_ACTIONS.gridL)
		viewmenu.addSeparator()
		syntaxmenu = viewmenu.addMenu("syntax")
		syntaxmenu.addAction(ALL_ACTIONS.pythonSyn)
		syntaxmenu.addAction(ALL_ACTIONS.plainSyn)
		syntaxmenu.addAction(ALL_ACTIONS.htmlSyn)

		# TOOL MENU
		tabwidth = toolmenu.addMenu("Tab Width")
		
		tabwidth.addAction(ALL_ACTIONS.tabW2)
		tabwidth.addAction(ALL_ACTIONS.tabW4)
		tabwidth.addAction(ALL_ACTIONS.tabW6)
		tabwidth.addAction(ALL_ACTIONS.tabW8)

		#Preferences Menu
		usermenu = preferences.addMenu("User Settings")
		preferences.addSeparator()
		fontmenu = preferences.addMenu("Font Size")
		fontmenu.addAction(ALL_ACTIONS.setfontI)
		fontmenu.addAction(ALL_ACTIONS.setfontD)
		fontstylemenu = preferences.addMenu("Font Style")
		fontstylemenu.addAction(ALL_ACTIONS.setfontS)
		fontstylemenu.addAction(ALL_ACTIONS.setfontM)
		fontstylemenu.addAction(ALL_ACTIONS.setfontSS)
		preferences.addSeparator()
		themesmenu = preferences.addMenu("PyCodeThemes")
		
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

# SHORTCUTS ==================================================================
		ALL_SHORTCUTS = PyCodeShortcuts(self.TAB_INTERFACE)
		ALL_SHORTCUTS.move_right_between_tabs.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.move_left_between_tabs.activated.connect(self.tab_seek_left)
		ALL_SHORTCUTS.move_right_between_tabs2.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.close_active_window.activated.connect(self.close_window)
		ALL_SHORTCUTS.close_dock.activated.connect(self.main_dock_widget.hide)
		
# SLOTS ========================================================================
	
	def set_file_and_status_bar(self):
		"""Make all menu and statubs bar options reflect current/active page"""
		
		try:
			self.GET_TEXT_EDIT().cursorPositionChanged.connect(self.column_line_update)
		
		except AttributeError:
			print "no tab_page available"

		try:
			self.current_syntax.setText(self._SYNTAX_DICT.get(self.GET_TEXT_INDEX()))
		
		except ValueError, KeyError:
			print "Key or Value missing from Syntax Dict"

	def GET_TEXT_CURSOR(self):
		"""return current text cursor"""
		return self.TAB_INTERFACE.currentWidget().textCursor()
	
	def GET_TEXT_EDIT(self):
		"""return current text editor"""
		return self.TAB_INTERFACE.currentWidget()
	
	def GET_TEXT_DOC(self):
		"""return current text doc"""
		return self.TAB_INTERFACE.currentWidget().document()

	def GET_TEXT_INDEX(self):
		"""return current text index"""
		return self.TAB_INTERFACE.currentIndex()


# INTERNAL SLOTS=================================================================
	def tab_seek_right(self):
		"""Moves focus one tab to the right, back to start if at the end"""

		total_tabs = self.TAB_INTERFACE.count()

		if self.GET_TEXT_INDEX() == total_tabs - 1:
			return self.TAB_INTERFACE.setCurrentWidget(self.TAB_INTERFACE.widget(0))

		else:
			widget_at_index = self.TAB_INTERFACE.widget(self.GET_TEXT_INDEX() + 1)
			return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)

	def tab_seek_left(self):
		"""Moves focus one tab to the left, moves to end if at the start"""

		total_tabs = self.TAB_INTERFACE.count()

		if self.GET_TEXT_INDEX() == 0:
			return self.TAB_INTERFACE.setCurrentWidget(self.TAB_INTERFACE.widget(total_tabs - 1))

		else:
			widget_at_index = self.TAB_INTERFACE.widget(self.GET_TEXT_INDEX() - 1)
			return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)



	# NOTE: make color changes Theme dependent. i.e. theme page should specify
	# these colors. This isn't working correctly as of yet.
	# should compare contents to orignal and indicate file has changed if !=
	def modified_since_save(self):
		"""Causes tab text to change if modified since last save"""
		return self.TAB_INTERFACE.tabBar().setTabTextColor(
									self.GET_TEXT_INDEX(), QColor("#fff5ee"))

	def column_line_update(self):
		"""updates current cursor position in document"""
		return self.line_count.setText("Line: %d, Column: %d" % (
			self.GET_TEXT_CURSOR().blockNumber()+1, self.GET_TEXT_CURSOR().columnNumber()+1))

	def select_current_text(self):
		"""Selects text in find bar when enter is pressed"""
		self.user_input.setSelection(0, len(self.user_input.text()))


# FILEMENU SLOTS===============================================================
	def open_file_dialog(self):
		"""opens file in new tab"""

		file_name,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if file_name != '':

			with open(file_name, "r") as f:
				
				data = f.read()
				new_page = QPlainTextEdit(self.TAB_INTERFACE)
				new_page.setPlainText(data)
				f.close()
				
				# codense the following two lines of code
				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()


				self.TAB_INTERFACE.addTab(new_page, nameOfFile)
				
		else:
			pass
	# needs work. Testing stages
	def open_file(self, file_name=None):
		"""Opens file without prompting user"""

		if file_name:
			with open(file_name, "r") as f:
				data = f.read()
				new_page = QPlainTextEdit(self.TAB_INTERFACE)
				new_page.setPlainText(data)
				f.close()
				self.TAB_INTERFACE.addTab(new_page, file_name)
		else:
			print "no filename supplied"

	def close_tab(self):
		"""Closes focused tab"""
		
		file_name = self.TAB_INTERFACE.tabText(self.GET_TEXT_INDEX())
		self._CLOSED_TAB_LIST.append(file_name)
		if file_name not in self._RECENTLY_OPENED and file_name != "":
			self._RECENTLY_OPENED.append(file_name)
		self.TAB_INTERFACE.removeTab(self.GET_TEXT_INDEX())

		try:
			return self.GET_TEXT_EDIT().setFocus()
		
		except AttributeError:
			pass
	
	def close_all(self):
		"""Closes all open files"""
		for i in xrange(self.TAB_INTERFACE.count()):
			self.close_tab()

	def new_file(self):
		"""Opens a plain text document"""

		new_page = QPlainTextEdit(self.TAB_INTERFACE)
		PlainText(new_page.document())
		self.TAB_INTERFACE.addTab(new_page, "Untitled")
		self.set_file_and_status_bar
		self.GET_TEXT_EDIT().setFocus()

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
					self.GET_TEXT_EDIT().setFocus()
		
			except IOError:
				pass

		else:
			pass

	def save_event(self):
		"""Saves file with current tab title text, no prompting. Does Not
		save ANY file with default "Untitled" file_name without prompting first. 
		"""
			
		file_name = self.TAB_INTERFACE.tabText(self.GET_TEXT_INDEX())		
		save_file = QFile(file_name)

		if file_name != "Untitled":
			f = open(file_name, "w")

			with f:
				data = self.GET_TEXT_EDIT().toPlainText()
				f.write(data)
				f.close()
				self.status.showMessage("Saved %s" % file_name, 4000)
				return self.modified_since_save()

		else:
			return self.save_file_as()
	
	def save_all(self):
		"""Save all opened files, prompt if "Untitled" page exists"""
		for i in xrange(self.TAB_INTERFACE.count()):
			
			file_name = self.TAB_INTERFACE.tabText(i)
			if file_name != "Untitled":
			
				save_file = QFile(file_name)

				with open(file_name, "w") as f:
					data = self.TAB_INTERFACE.widget(i).toPlainText()
					f.write(data)
					f.close()
					self.modified_since_save()
			else:
				self.save_file_as()

		return self.status.showMessage("Saved All Opened Files", 4000)

	def save_file_as(self):
		"""Save current file as"""

		file_name, _ = QFileDialog.getSaveFileName(self,
			"Save File", os.getcwd())

		# could use RegExp search to catch more complicated errors here
		if file_name != '':

			f = open(file_name, "w")

			with f:

				data = self.GET_TEXT_EDIT().toPlainText()
				
				f.write(data)
				f.close()
				# condense the following code				
				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()

				self.TAB_INTERFACE.setTabText(self.GET_TEXT_INDEX(), nameOfFile)
		
		else:
			pass

	def exit_event(self):
		"""Exits without prompting"""
		self.write_settings()
		# remove this line after testing
		# self.settings.clear()
		sys.exit()

# EDIT MENU SLOTS =============================================================
	def cut_selection(self):
		"""copy/cut selected text"""
		return self.GET_TEXT_EDIT().cut()

	def find_text(self):
		"""Find the indicated text within the current tab page"""
		### need to add auto-complete, find & replace
		self.main_dock_widget.show()
		self.user_input.setFocus()

		_TESTING = QTextCursor(self.GET_TEXT_CURSOR())
		
		if self.GET_TEXT_CURSOR().position() != 0:
			update = self.GET_TEXT_DOC().find(self.user_input.text())
			self.GET_TEXT_EDIT().setTextCursor(update)
			self.GET_TEXT_CURSOR().select(QTextCursor.WordUnderCursor)

		

	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		return self.GET_TEXT_EDIT().paste()

	def undo_last(self):
		"""Steps back in operation history"""
		return self.GET_TEXT_EDIT().undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		return self.GET_TEXT_EDIT().redo()

	def clone_doc(self):
		"""clones current document in focus"""
		cloned_doc = self.GET_TEXT_DOC().clone(self.TAB_INTERFACE)
		# this seems redundent. there's probaly a better way to do this
		cloned_doc.setDocumentLayout(QPlainTextDocumentLayout(cloned_doc))
		new_page = QPlainTextEdit(self.TAB_INTERFACE)
		new_page.setDocument(cloned_doc)
		return self.TAB_INTERFACE.addTab(new_page, "Untitled")

	def find_regexp(self):
		"""finds text in doc using regexp"""
		pass

# VIEW MENU SLOTS ==============================================================
	def set_tab_width(self, num):
		return self.GET_TEXT_EDIT().setTabStopWidth(num)

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.GET_TEXT_DOC())
		self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "Python"
		self.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.GET_TEXT_DOC())
		self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "PlainText"
		self.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.GET_TEXT_DOC())
		self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "HTML"
		self.current_syntax.setText("HTML") 

	def hide_statusbar(self):
		if self.ALL_ACTIONS.status_hideAct.isChecked():
			self.status.hide()
		else:
			self.status.show()
	# the following three functions are broken. Remove after testing.
	def plain_layout(self):
		"""Changes the Layout of current Window to a single page"""
		return self.setLayout(None)
	
	def split_screen_layout(self):
		test_layout = QHBoxLayout(self)
		test_layout.addWidget(self.TAB_INTERFACE)
		test_layout.addWidget(self.TAB_INTERFACE)
		self.setLayout(test_layout)
	
	def grid_layout(self):
		pass

# Perfrences Menu Slots =======================================================
	def increase_font_size(self):
		"""Incrementally increases font point size"""
		self.GET_TEXT_EDIT().selectAll()
		currentF = self.GET_TEXT_EDIT().currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()+ 5)
		self.GET_TEXT_EDIT().setCurrentCharFormat(currentF)

	def decrease_font_size(self):
		"""Incrementally decreases font point size"""
		self.GET_TEXT_EDIT().selectAll()
		currentF = self.GET_TEXT_EDIT().currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()- 5)
		if currentF.fontPointSize() > 0:
			return self.GET_TEXT_EDIT().setCurrentCharFormat(currentF)
		else:
			pass

	def set_serif(self):
		"""Set all text to serif font family"""
		self.GET_TEXT_EDIT().selectAll()
		currentF = self.GET_TEXT_EDIT().currentCharFormat()
		currentF.setFontFamily("serif")
		self.GET_TEXT_EDIT().setCurrentCharFormat(currentF)

	def set_monospace(self):
		"""Set all text to monospace font family"""
		self.GET_TEXT_EDIT().selectAll()
		currentF = self.GET_TEXT_EDIT().currentCharFormat()
		currentF.setFontFamily("monospace")
		self.GET_TEXT_EDIT().setCurrentCharFormat(currentF)

	def set_sansserif(self):
		"""Set all text to sans-serif font family"""
		self.GET_TEXT_EDIT().selectAll()
		currentF = self.GET_TEXT_EDIT().currentCharFormat()
		currentF.setFontFamily("sans-serif")
		self.GET_TEXT_EDIT().setCurrentCharFormat(currentF)

# SETTINGS/STATE SLOTS ========================================================

	def write_settings(self):
		"""Writes the current user settings"""
		# self.settings = QSettings(QSettings.UserScope, 
		# 				"AD Engineering", "PyCode Text Editor")

		files = [self.TAB_INTERFACE.tabText(i) for i in xrange(self.TAB_INTERFACE.count())]
		
		self.settings.beginGroup("Main Window")
		# save opened tabs
		self.settings.beginWriteArray("files")
		for i in xrange(len(files)):
			self.settings.setArrayIndex(i)
			self.settings.setValue("filename", files[i] )
		self.settings.endArray()

		# save recently opened tabs
		self.settings.beginWriteArray("Recently Opened")
		for i in xrange(len(self._RECENTLY_OPENED)):
			self.settings.setArrayIndex(i)
			self.settings.setValue("ROFile", self._RECENTLY_OPENED[i])
		self.settings.endArray()
		self.settings.setValue("Position", self.pos())
		self.settings.setValue("Size", self.size())
		self.settings.endGroup()


	def read_settings(self):
		"""Loads the saved settings from a previous session"""
		self.settings = QSettings("AD Engineering", 
									"PyCode Text Editor")

		self.settings.beginGroup("Main Window")
		
		# get and set files from last session
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

		# get and set recently opened files. I think there is a better way to do this
		size = self.settings.beginReadArray("Recently Opened")
		for i in xrange(size):
			self.settings.setArrayIndex(i)
			recent_file = self.settings.value("ROFile")
			self._RECENTLY_OPENED.append(recent_file)
		self.settings.endArray()
		# here we add all recently opened files to open recent menu
		for i in self._RECENTLY_OPENED:
			i_action = QAction(i, self)
			self.recent_files_menu.addAction(i_action)
		self.move(self.settings.value("Position"))
		self.resize(self.settings.value("Size"))
		self.settings.endGroup()

#MAIN =========================================================================
def main():
	pycodeapp = QApplication(sys.argv)
	editor = PyCodeEditor()

	try:
		with open("PyCodeThemes/PyCodeCrimson.qss") as f:
			stylesheet = f.read()
			pycodeapp.setStyleSheet(stylesheet)
	except IOError:
		print "Cannot find Stylesheet; falling back to native style"

	try:
		editor.read_settings()
	except TypeError:
		pass

	editor.show()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
