# IMPORTANT! This is under active development. The code is being restructured to OOP
import sys, os, time
import re

from PySide.QtCore import *
from PySide.QtGui import *

from SyntaxClasses import *
from PyCodeActions import *
from PyCodeShortcuts import *
from functools import partial


class PyCodeEditor(QMainWindow):
	"""Main Program win. Creates new instance of pycode editor"""	

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
		self.initUI()
		self.setStyleSheet("""QStatusBar::item{border: none;}""")
		self.setWindowTitle("PyCode Text Editor")

	def initUI(self):

		TAB_INTERFACE = TabInterface(self)
		menu_bar = PyCodeMenuBar(TAB_INTERFACE)
		filemenu = menu_bar.addMenu(FileMenuActions(menu_bar))
		editmenu = menu_bar.addMenu(EditMenuActions(menu_bar))
		viewmenu = menu_bar.addMenu(ViewMenuActions(menu_bar))
		toolmenu = menu_bar.addMenu(ToolMenuActions(menu_bar))
		menu_bar.addMenu()
		TAB_INTERFACE.new_file()
		
		self.setStatusBar(TAB_INTERFACE.currentWidget().tab_status_bar)
		self.setMenuBar(menu_bar)
		
		# should check here for any previously opened tabs

		self.setCentralWidget(TAB_INTERFACE)

		# test_layout2 = QHBoxLayout(self)
		# test_layout2.addWidget(self.TAB_INTERFACE)

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

		
		# self.TAB_INTERFACE.currentChanged.connect(self.set_file_and_status_bar)

		# self.GET_TEXT_EDIT().cursorPositionChanged.connect(self.column_line_update)
		# self.GET_TEXT_EDIT().textChanged.connect(self.modified_since_save)



# MENUBAR Specific ==================================================
		# CREATE MENUS HERE
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
		
		# try:
		# 	self.GET_TEXT_EDIT().cursorPositionChanged.connect(self.column_line_update)
		
		# except AttributeError:
		# 	print "no tab_page available"

		try:
			self.current_syntax.setText(self._SYNTAX_DICT.get(self.GET_TEXT_INDEX()))
		
		except ValueError, KeyError:
			print "Key or Value missing from Syntax Dict"


# INTERNAL SLOTS=================================================================
	# these should go in tabinterface class
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
	# def modified_since_save(self):
	# 	"""Causes tab text to change if modified since last save"""
	# 	return self.TAB_INTERFACE.tabBar().setTabTextColor(
	# 								self.GET_TEXT_INDEX(), QColor("#fff5ee"))

	# def column_line_update(self):
	# 	"""updates current cursor position in document"""
	# 	return self.line_count.setText("Line: %d, Column: %d" % (
	# 		self.GET_TEXT_CURSOR().blockNumber()+1, self.GET_TEXT_CURSOR().columnNumber()+1))

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
	# def set_tab_width(self, num):
	# 	return self.GET_TEXT_EDIT().setTabStopWidth(num)

	# def python_syntax(self):
	# 	"""sets python syntax highlighting for textdocument in focus"""
	# 	PythonSyntax(self.GET_TEXT_DOC())
	# 	self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "Python"
	# 	self.current_syntax.setText("Python")

	# def plain_text(self):
	# 	"""Sets plain text syntax highlighting for textdocument in focus"""
	# 	PlainText(self.GET_TEXT_DOC())
	# 	self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "PlainText"
	# 	self.current_syntax.setText("PlainText")

	# def html_syntax(self):
	# 	"""sets syntax highlighting to HTML"""
	# 	HtmlSyntax(self.GET_TEXT_DOC())
	# 	self._SYNTAX_DICT[self.GET_TEXT_INDEX()] = "HTML"
	# 	self.current_syntax.setText("HTML") 

	# def hide_statusbar(self):
	# 	if self.ALL_ACTIONS.status_hideAct.isChecked():
	# 		self.status.hide()
	# 	else:
	# 		self.status.show()
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

# OOP Restructuring============================================================
class PyCodeMenuBar(QMenuBar):
	"""Responsible for holding all menus"""
	def __init__(self, parent=None):
		super(PyCodeMenuBar, self).__init__(parent)


class TabInterface(QTabWidget):
	"""Responsible for all QTabWidget/QTabBar related signals and slots.
	Holds all file-related slots(method-functions) and signals IF not in TabPage

	"""

	def __init__(self, parent=None):
		super(TabInterface, self).__init__(parent)

		self._CLOSED_TAB_LIST = []
		self.setDocumentMode(True)
		self.setMovable(True)
		self.setTabsClosable(True)
		self.setElideMode(Qt.ElideRight)
		self.setFocusPolicy(Qt.NoFocus)

	# signals go here for now
	self.tabCloseRequested.connect(self.close_tab)

	def open_file_dialog(self):
		"""opens file in new tab"""

		file_name,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if file_name != '':

			with open(file_name, "r") as f:
				
				data = f.read()
				new_page = TabPage(self)
				new_page.setPlainText(data)
				f.close()
				
				# codense the following two lines of code
				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()

				self.addTab(new_page, nameOfFile)

				
		else:
			pass

	def reopen_last_tab(self):
		"""Opens the last tab closed"""

		if len(self._CLOSED_TAB_LIST) > 0:

			new_page = TabPage(self)
			last_file = self._CLOSED_TAB_LIST.pop()

			try:

				with open(last_file, "r") as f:
					data = f.read()
					new_page.setPlainText(data)
		
					self.addTab(new_page, last_file)
					self.setFocus()
		
			except IOError:
				pass

		else:
			pass

	def new_file(self):
		"""Opens a plain text document"""

		new_page = TabPage(self)
		PlainText(new_page.document())
		
		self.addTab(new_page, "Untitled")
		self.currentWidget().setFocus()

	def close_tab(self):
		"""Closes focused tab"""
		
		file_name = self.tabText(self.currentIndex())

		self._CLOSED_TAB_LIST.append(file_name)
		self.removeTab(self.currentIndex())


		try:
			return self.setFocus()
		
		except AttributeError:
			pass

	def close_all(self):
		"""Closes all open files"""
		for i in xrange(self.count()):
			self.close_tab()

	# needs work. Testing stages
	def open_file(self, file_name=None):
		"""Opens file without prompting user"""

		if file_name:
			with open(file_name, "r") as f:
				data = f.read()
				new_page = TabPage(self)
				new_page.setPlainText(data)
				f.close()
				self.addTab(new_page, file_name)
		else:
			print "no filename supplied"

	def save_event(self):
		"""Saves current file tab text, except if "Untitled"; it will prompt."""
			
		file_name = self.tabText(self.currentIndex())		
		save_file = QFile(file_name)

		if file_name != "Untitled":
			f = open(file_name, "w")

			with f:
				data = self.currentWidget().toPlainText()
				f.write(data)
				f.close()
				self.status.showMessage("Saved %s" % file_name, 4000)

		else:
			return self.save_file_as()
	
	def save_all(self):
		"""Save all opened files, prompt if "Untitled" page exists"""
		for i in xrange(self.count()):
			
			file_name = self.tabText(i)
			if file_name != "Untitled":
			
				save_file = QFile(file_name)

				with open(file_name, "w") as f:
					data = self.widget(i).toPlainText()
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

				data = self.currentWidget().toPlainText()
				
				f.write(data)
				f.close()
				# condense the following code				
				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()

				self.setTabText(self.currentIndex(), nameOfFile)
		
		else:
			pass


class TabPage(QPlainTextEdit):
	"""Responsible for all signals and method-functions related ONLY to QPlainTextEdit.
	Use the TabPage.Doc in order to access the current QTextDocument


	"""
	def __init__(self, parent=None):
		super(TabPage, self).__init__(parent)
		self._SYNTAX_DICT = {}
		self.DOC = self.document()
		self.tab_status_bar = PyCodeStatusBar(self)

	# slots and signals 
	self.textChanged.connect(self.modified_since_save)
	
	def modified_since_save(self):
		"""Causes tab text to change if modified since last save"""
		return self.parent().tabBar().setTabTextColor(QColor("#fff5ee"))

	def set_tab_width(self, num):
		return self.setTabStopWidth(num)

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.DOC)
		self._SYNTAX_DICT[self.currentIndex()] = "Python"
		self.tab_status_bar.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.DOC())
		self._SYNTAX_DICT[self.currentIndex()] = "PlainText"
		self.tab_status_bar.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.DOC())
		self._SYNTAX_DICT[self.currentIndex()] = "HTML"
		self.tab_status_bar.current_syntax.setText("HTML") 


class PyCodeStatusBar(QStatusBar):
	""" Responsible for individual statusbars' slots and signals"""
	def __init__(self, parent=None):
		super(PyCodeStatusBar, self).__init__(parent)
		self.showMessage("Ready?", 4000)
		
		self.line_count = QLabel()
		self.current_syntax = QLabel()
		self.addPermanentWidget(self.line_count)
		self.addPermanentWidget(self.current_syntax)

	self.parent().cursorPositionChanged.connect(self.column_line_update)

	def column_line_update(self):
		"""updates current cursor position in document"""
		return self.line_count.setText("Line: %d, Column: %d" % (
			self.parent().textCursor().blockNumber()+1, 
			self.parent().textCursor().columnNumber()+1))

	def hide_statusbar(self):
		if self.ALL_ACTIONS.status_hideAct.isChecked():
			self.status.hide()
		else:
			self.status.show()


class FileMenuActions(QMenu):
	"""Responsible for all FileMenu specific actions
		The most common selections in a file menu will be added by default,
		however, all defined by user. Can be
		extended with the create_action method-function.
	"""

	def __init__(self, parent=None):
		super(FileMenu, self).__init__(parent)
		self.ALL_FILE_ACTIONS = {}
		self.create_action("exit_act", "Exit", "Ctrl+Q")
		self.create_action("save_act", "Save", "Ctrl+S")
		self.create_action("save_as_act", "Save as...", "Ctrl+Shift+S")
		self.create_action("save_all_act", "Save All Files")
		self.create_action("newF_act", "New File", "Ctrl+N")
		self.create_action("newW_act", "New Window", "Ctrl+Shift+N")
		self.create_action("closeF_act", "Close Tab", "Ctrl+W")
		self.create_action("closeW_act", "Close Window", "Ctrl+Shift+W")
		self.create_action("openF_act", "Open File", "Ctrl+O")
		self.create_action("reopenF_act", "Reopen Last Tab", "Ctrl+Shift+T")

	# signals defined here
	self.ALL_FILE_ACTIONS.get(exit_act).triggered.connect(self.exit_event)
	self.ALL_FILE_ACTIONS.get(newW_act).triggered.connect(self.new_window)
	self.ALL_FILE_ACTIONS.get(closeW_act).triggered.connect(self.close_window)

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_FILE_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_FILE_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_FILE_ACTIONS.get(name))
	
	
	def new_window(self):
		"""opens a completely new window."""
		self.new_window_instance = PyCodeEditor()
		return self.new_window_instance.show()

	def close_window(self):
		"""Close active window"""
		return self.close()
	
	def exit_event(self):
		"""Exits without prompting"""
		self.write_settings()
		# remove this line after testing
		# self.settings.clear()
		sys.exit()


class EditMenuActions(QMenu):
	def __init__(self, parent=None):
		super(EditMenu, self).__init__(parent)
		self.ALL_EDIT_ACTIONS = {}
		self.create_action("paste_act", "Paste", "Ctrl+V")
		self.create_action("cut_act", "Cut", "Ctrl+X")
		self.create_action("redo_act", "Redo", "Ctrl+Shift+Z")
		self.create_action("undo_act", "Undo", "Ctrl+Z")
		self.create_action("bold_act", "Bold", "Ctrl+B")
		self.create_action("copy_act", "Copy", "Ctrl+C")
		self.create_action("find_act", "Find", "Ctrl+F")
		self.create_action("find_regexp_act", "Find RegExp")
		self.create_action("find_and_replace_act", "Search & Replace")
		self.create_action("Clone", "Clone Current Document")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_EDIT_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_EDIT_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_EDIT_ACTIONS.get(name))



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


class ViewMenuActions(QMenu):
	"""Defines and Holds all view menu specific actions"""
	def __init__(self, parent=None):
		super(ViewMenu, self).__init__(parent)
		self.ALL_VIEW_ACTIONS = {}
		self.create_action("plain_lay_act", "Single Screen")
		self.create_action("split_lay_act", "Split Screen")
		self.create_action("grid_lay_act", "Grid Screen")
		self.create_action("python_syn", "Python")
		self.create_action("plain_syn", "PlainText")
		self.create_action("html_syn", "HTML")
		self.create_action("hide_status_act", "Hide StatusBar")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_VIEW_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_VIEW_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_VIEW_ACTIONS.get(name))

	def create_action_group(self, name=None):
		return self.ACTION_GROUPS[name] = QActionGroup(self)

	def add_to_action_group(self, name=None, actionname=None):
		actionname = self.ALL_VIEW_ACTIONS.get(actionname)
		return self.ACTION_GROUPS.get(name).addAction(actionname)


class ToolMenuActions(QMenu):
	"""Holds and Defines all ToolMenu specific actions"""
	def __init(self, parent=None):
		super(ToolMenu, self).__init__(parent)
		self.ALL_TOOL_ACTIONS = {}
		self.ACTION_GROUPS = {}
		self.create_action("snippet_act", "Code Snippets")
		self.create_action("build_act", "Build")
		self.create_action("tab_act_1", "Set tab width 1")
		self.create_action("tab_act_2", "Set tab width 2")
		self.create_action("tab_act_3", "Set tab width 3")
		self.create_action("tab_act_4", "Set tab width 4")
		self.create_action("tab_act_5", "Set tab width 5")
		self.create_action("tab_act_6", "Set tab width 6")
		self.create_action("tab_act_7", "Set tab width 7")
		self.create_action("tab_act_8", "Set tab width 8")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_TOOL_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_TOOL_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_TOOL_ACTIONS.get(name))

	def create_action_group(self, name=None):
		return self.ACTION_GROUPS[name] = QActionGroup(self)

	def add_to_action_group(self, name=None, actionname=None):
		actionname = self.ALL_VIEW_ACTIONS.get(actionname)
		return self.ACTION_GROUPS.get(name).addAction(actionname)


class PrefMenuActions(QMenu):
	"""Holds and defines all Preference Menu actions"""
	def __init__(self, parent=None):
		super(PrefMenu, self).__init__(parent)
		self.ALL_PREF_ACTIONS = {}
		self.create_action("font_inc_act", "Increase Font Size", "Ctrl+=")
		self.create_action("font_dec_act", "Decrease Font Size", "Ctrl+-")
		self.create_action("serif_font_act", "Serif")
		self.create_action("monospace_font_act", "Monospace")
		self.create_action("sans_serif_font_act", "Sans-Serif")
		self.create_action("invert_act", "Inverse Theme Colors")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_PREF_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_PREF_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_PREF_ACTIONS.get(name))


class PyCodeShortcuts():
	"""Responsible for creating/holding all active Shortcuts"""

	def __init__(self, parent=None):

		self._ALL_SHORTCUTS = {}
		self.create_shortcut("move_right", "Ctrl+Tab", parent, True)
		self.create_shortcut("move_right", "Ctrl+pgup", parent, True)
		self.create_shortcut("move_left", "Ctrl+Shift+Tab", parent, True)
		self.create_shortcut("move_left", "Ctrl+pgdn", parent, True)
		self.create_shortcut("close_focused_win", "Ctrl+Shift+W", parent)
		self.create_shortcut("close_dock", "Esc", parent)

	def create_shortcut(self, name=None, short=None, parent=None, auto=False):
		"""Creates Shortcut"""
		self._ALL_SHORTCUTS[name] = QShortcut(short, parent)
		if auto:
			self._ALL_SHORTCUTS.get(name).setAutoRepeat(auto)

		
		# self.move_right_between_tabs = QShortcut("Ctrl+Tab", parent)
		# self.move_right_between_tabs2 = QShortcut("Ctrl+pgup", parent)
		# self.move_left_between_tabs = QShortcut("Ctrl+Shift+Tab", parent)
		# self.move_left_between_tabs2 = QShortcut("Ctrl+pgdn", parent)
		# self.close_active_window = QShortcut("Ctrl+Shift+W", parent)
		# self.close_dock = QShortcut(QKeySequence(Qt.Key_Escape), parent)

		# # i should probly set this in the main module
		# self.move_left_between_tabs.setAutoRepeat(True)
		# self.move_right_between_tabs.setAutoRepeat(True)


def main():
	pycodeapp = QApplication(sys.argv)
	editor = PyCodeEditor()

	try:
		with open("../PyCodeThemes/PyCodeCrimson.qss") as f:
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
