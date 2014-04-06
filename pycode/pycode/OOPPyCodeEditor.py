# IMPORTANT! This is under active development. The code is being restructured to OOP
import sys, os
# import re

from PySide.QtCore import *
from PySide.QtGui import *

from SyntaxClasses import *
from functools import partial


class PyCodeEditor(QMainWindow):
	"""Main Program win. Creates new instance of pycode editor"""	

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
		self.initUI()
		self.setStyleSheet("""QStatusBar::item{border: none;}""")
		self.setWindowTitle("PyCode Text Editor")

	def initUI(self):
		"puts together the main window"
		self.MENU = PyCodeMenuBar(self)
		self.DOCKW = PyCodeDockWidget(self)
		self.setMenuBar(self.MENU)
		self.setCentralWidget(self.MENU.tab_interface)
		self.set_status_bar()

	def set_status_bar(self):
		"Updates and sets the current status bar"
		self.setStatusBar(self.MENU.tab_page.tab_status_bar)
		
		


# OOP Restructuring============================================================
class PyCodeDockWidget(QDockWidget):
	
	def __init__(self, parent=None):
		super(PyCodeDockWidget, self).__init__(parent)

		self.user_input = QLineEdit(self)
		self.setAllowedAreas(Qt.BottomDockWidgetArea)
		self.setFloating(False)
		self.setObjectName('Main Dock')
		self.setWidget(self.user_input)
		# self.parent().addDockWidget(Qt.BottomDockWidgetArea, self)
		self.hide()

		self.user_input.returnPressed.connect(self.select_current_text)
		# self.user_input.textChanged.connect(self.find_text)

	def select_current_text(self):
		"""Selects text in find bar when enter is pressed"""
		self.user_input.setSelection(0, len(self.user_input.text()))


class PyCodeSettings(QSettings):

	def __init__(self, parent=None):
		super(PyCodeSettings, self).__init__(parent)
		self.settings = QSettings(QSettings.UserScope, 
						"AD Engineering", "PyCode Text Editor")

	def write_settings(self):
		"""Writes the current user settings"""

		files = [self.parent().tabText(i) for i in xrange(self.parent().count())]
		
		self.settings.beginGroup("Main Window")
		# save opened tabs
		self.settings.beginWriteArray("files")
		for i in xrange(len(files)):
			self.settings.setArrayIndex(i)
			self.settings.setValue("filename", files[i] )
		self.settings.endArray()

		self.settings.setValue("Position", self.pos())
		self.settings.setValue("Size", self.size())
		self.settings.endGroup()


	def read_settings(self):
		"""Loads the saved settings from a previous session"""
		# self.settings = QSettings("AD Engineering", 
		# 							"PyCode Text Editor")

		self.settings.beginGroup("Main Window")
		
		# get and set files from last session
		size = self.settings.beginReadArray("files")
		for i in xrange(size):
			self.settings.setArrayIndex(i)
			tabname = self.settings.value("filename")
			try:
				with open(tabname, "r") as f:
					data = f.read()
					new_page = TabPage(self.parent())
					new_page.setPlainText(data)
					self.parent().addTab(new_page, tabname)
					f.close()
			except IOError:
				pass

		self.settings.endArray()

		self.move(self.settings.value("Position"))
		self.resize(self.settings.value("Size"))
		self.settings.endGroup()


class PyCodeMenuBar(QMenuBar):
	"""Responsible for holding all menus and respective trigger connections"""
	def __init__(self, parent=None):
		super(PyCodeMenuBar, self).__init__(parent)
		self.tab_interface = TabInterface(self)
		self.tab_page = self.tab_interface.currentWidget()

		self.file_menu = FileMenuTriggers(self)
		self.edit_menu = EditMenuTriggers(self)
		self.view_menu = ViewMenuTriggers(self)
		self.tool_menu = ToolMenuTriggers(self)
		self.pref_menu = PrefMenuTriggers(self)
		self.addMenu(self.file_menu)
		self.addMenu(self.edit_menu)
		self.addMenu(self.view_menu)
		self.addMenu(self.tool_menu)
		self.addMenu(self.pref_menu)


	# Could probaly make more classes for each specific menu triggers
	# file menu triggers
		self.tab_interface.Short_dict("close_focused_win").activated.connect(
												self.file_menu.close_window)


class TabInterface(QTabWidget):
	"""Responsible for all QTabWidget/QTabBar related signals and slots.
	Holds all file-related slots(method-functions) and signals IF not in TabPage

	"""

	def __init__(self, parent=None):
		super(TabInterface, self).__init__(parent)

		self._CLOSED_TAB_LIST = []
		self._SHORTCUTS = PyCodeShortcuts(self)
		self.Short_dict = self._SHORTCUTS._ALL_SHORTCUTS.get
		self.setDocumentMode(True)
		self.setMovable(True)
		self.setTabsClosable(True)
		self.setElideMode(Qt.ElideRight)
		self.setFocusPolicy(Qt.NoFocus)
		# here i will check for previously opened tabs
		self.new_file()
		self.CURRENT_DOC = self.currentWidget().DOC

	# signals go here for now
		self.tabCloseRequested.connect(self.close_tab)
		self.currentChanged.connect(self.currentWidget().update_status_bar)
		self.Short_dict("move_right").activated.connect(self.tab_seek_right)
		self.Short_dict("move_right2").activated.connect(self.tab_seek_right)
		self.Short_dict("move_left").activated.connect(self.tab_seek_left)
		self.Short_dict("move_left2").activated.connect(self.tab_seek_left)
		self.Short_dict("close_dock").activated.connect(self.hide_dock)

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
					self.currentWidget().setFocus()
		
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
	# def open_file(self, file_name=None):
	# 	"""Opens file without prompting user"""

	# 	if file_name:
	# 		with open(file_name, "r") as f:
	# 			data = f.read()
	# 			new_page = TabPage(self)
	# 			new_page.setPlainText(data)
	# 			f.close()
	# 			self.addTab(new_page, file_name)
	# 	else:
	# 		print "no filename supplied"

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
				self.parent().statusBar().showMessage(
										"Saved %s" % file_name, 4000)

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
			else:
				self.save_file_as()

		return self.parent().statusBar().showMessage(
									"Saved All Opened Files", 4000)

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

				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()

				self.setTabText(self.currentIndex(), nameOfFile)
		
		else:
			pass

	def tab_seek_right(self):
		"""Moves focus one tab to the right, back to start if at the end"""

		if self.currentIndex() == self.count() - 1:
			return self.setCurrentWidget(self.widget(0))

		else:
			widget_at_index = self.widget(self.currentIndex() + 1)
			return self.setCurrentWidget(widget_at_index)

	def tab_seek_left(self):
		"""Moves focus one tab to the left, moves to end if at the start"""

		if self.currentIndex() == 0:
			return self.setCurrentWidget(self.widget(self.count() - 1))

		else:
			widget_at_index = self.widget(self.currentIndex() - 1)
			return self.setCurrentWidget(widget_at_index)

	def cut_selection(self):
		"""copy/cut selected text"""
		return self.currentWidget().cut()

	def find_text(self):
		"""Find the indicated text within the current tab page"""
		### need to add auto-complete, find & replace
		Dock_widget = self.parent().parent().DOCKW
		Dock_widget.show()
		Dock_widget.user_input.setFocus()

		_TESTING = QTextCursor(self.currentWidget().textCursor())
		
		if self.currentWidget().textCursor().position() != 0:
			
			update = self.currentWidget().DOC.find(self.user_input.text())
			self.currentWidget().setTextCursor(update)
			self.currentWidget().textCursor().select(QTextCursor.WordUnderCursor)
	
	def hide_dock(self):
		"""hides Main Window dock """
		return self.parent().parent().DOCKW.hide()
		

	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		return self.currentWidget().paste()

	def undo_last(self):
		"""Steps back in operation history"""
		return self.currentWidget().undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		return self.currentWidget().redo()

	def clone_doc(self):
		"""clones current document in focus"""
		cloned_doc = self.CURRENT_DOC.clone(self)
		cloned_doc.setDocumentLayout(QPlainTextDocumentLayout(cloned_doc))
		new_page = TabPage(self)
		new_page.setDocument(cloned_doc)
		return self.addTab(new_page, "Untitled")

	def find_regexp(self):
		"""finds text in doc using regexp"""
		pass

	def increase_font_size(self):
		"""Incrementally increases font point size"""
		self.currentWidget().selectAll()
		currentF = self.currentWidget().currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()+ 5)
		self.currentWidget().setCurrentCharFormat(currentF)

	def decrease_font_size(self):
		"""Incrementally decreases font point size"""
		self.currentWidget().selectAll()
		currentF = self.currentWidget().currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()- 5)
		if currentF.fontPointSize() > 0:
			return self.currentWidget().setCurrentCharFormat(currentF)
		else:
			pass

	def set_serif(self):
		"""Set all text to serif font family"""
		self.currentWidget().selectAll()
		currentF = self.currentWidget().currentCharFormat()
		currentF.setFontFamily("serif")
		self.currentWidget().setCurrentCharFormat(currentF)

	def set_monospace(self):
		"""Set all text to monospace font family"""
		self.currentWidget().selectAll()
		currentF = self.currentWidget().currentCharFormat()
		currentF.setFontFamily("monospace")
		self.currentWidget().setCurrentCharFormat(currentF)

	def set_sansserif(self):
		"""Set all text to sans-serif font family"""
		self.currentWidget().selectAll()
		currentF = self.currentWidget().currentCharFormat()
		currentF.setFontFamily("sans-serif")
		self.currentWidget().setCurrentCharFormat(currentF)


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
		return self.parent().parent().tabBar().setTabTextColor(
			self.parent().parent().currentIndex(), QColor("#fff5ee"))

	def set_tab_width(self, num):
		return self.setTabStopWidth(num)

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.DOC)
		self._SYNTAX_DICT[self.parent().currentIndex()] = "Python"
		self.tab_status_bar.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.DOC)
		self._SYNTAX_DICT[self.parent().currentIndex()] = "PlainText"
		self.tab_status_bar.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.DOC)
		self._SYNTAX_DICT[self.parent().currentIndex()] = "HTML"
		self.tab_status_bar.current_syntax.setText("HTML") 

	def update_status_bar(self):
		"""Make all menu and statubs bar options reflect current/active page"""
		
		try:
			self.tab_status_bar.current_syntax.setText(self._SYNTAX_DICT.get(
				self.parent().currentIndex()))
		
		except ValueError, KeyError:
			print "Key or Value missing from Syntax Dict"

	def hide_statusbar(self):
		if self.parent().status_hideAct.isChecked():
			self.tab_status_bar.hide()
		else:
			self.tab_status_bar.show()


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
			self.textCursor().blockNumber()+1, 
			self.textCursor().columnNumber()+1))


class FileMenuActions(QMenu):
	"""Responsible for all FileMenu specific actions
		The most common selections in a file menu will be added by default,
		however, all defined by user. Can be
		extended with the create_action method-function.
	"""

	def __init__(self, parent=None):
		super(FileMenuActions, self).__init__(parent)
		self.ALL_FILE_ACTIONS = {}
		self.setTitle("&File")
		self.create_action("exit_act", "Exit", "Ctrl+Q")
		self.create_action("save_act", "Save", "Ctrl+S")
		self.create_action("save_as_act", "Save as...", "Ctrl+Shift+S")
		self.create_action("save_all_act", "Save All Files")
		self.create_action("newF_act", "New File", "Ctrl+N")
		self.create_action("newW_act", "New Window", "Ctrl+Shift+N")
		self.create_action("closeF_act", "Close Tab", "Ctrl+W")
		self.create_action("closeW_act", "Close Window", "Ctrl+Shift+W")
		self.create_action("close_all_act", "Close all open windows")
		self.create_action("openF_act", "Open File", "Ctrl+O")
		self.create_action("reopenF_act", "Reopen Last Tab", "Ctrl+Shift+T")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_FILE_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_FILE_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_FILE_ACTIONS.get(name))
	

class EditMenuActions(QMenu):
	def __init__(self, parent=None):
		super(EditMenuActions, self).__init__(parent)
		self.ALL_EDIT_ACTIONS = {}
		self.setTitle("Edit")
		self.create_action("paste_act", "Paste", "Ctrl+V")
		self.create_action("cut_act", "Cut", "Ctrl+X")
		self.create_action("redo_act", "Redo", "Ctrl+Shift+Z")
		self.create_action("undo_act", "Undo", "Ctrl+Z")
		self.create_action("bold_act", "Bold", "Ctrl+B")
		self.create_action("copy_act", "Copy", "Ctrl+C")
		self.create_action("find_act", "Find", "Ctrl+F")
		self.create_action("find_regexp_act", "Find RegExp")
		self.create_action("find_and_replace_act", "Search & Replace")
		self.create_action("clone_act", "Clone Current Document")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_EDIT_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_EDIT_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_EDIT_ACTIONS.get(name))


class ViewMenuActions(QMenu):
	"""Defines and Holds all view menu specific actions"""
	def __init__(self, parent=None):
		super(ViewMenuActions, self).__init__(parent)
		self.ALL_VIEW_ACTIONS = {}
		self.setTitle("View")
		self.create_action("plain_lay_act", "Single Screen")
		self.create_action("split_lay_act", "Split Screen")
		self.create_action("grid_lay_act", "Grid Screen")
		self.create_action("python_syn", "Python")
		self.create_action("plain_syn", "PlainText")
		self.create_action("html_syn", "HTML")
		self.create_action("hide_status_act", "Hide StatusBar")
		self.ALL_VIEW_ACTIONS.get("hide_status_act").setCheckable(True)

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_VIEW_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_VIEW_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_VIEW_ACTIONS.get(name))

	def create_action_group(self, name=None):
		self.ACTION_GROUPS[name] = QActionGroup(self)

	def add_to_action_group(self, name=None, actionname=None):
		actionname = self.ALL_VIEW_ACTIONS.get(actionname)
		return self.ACTION_GROUPS.get(name).addAction(actionname)


class ToolMenuActions(QMenu):
	"""Holds and Defines all ToolMenu specific actions"""
	def __init__(self, parent=None):
		super(ToolMenuActions, self).__init__(parent)
		self.ACTION_GROUPS = {}
		self.ALL_TOOL_ACTIONS = {}
		self.setTitle("&Tool")
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
		self.ACTION_GROUPS[name] = QActionGroup(self)

	def add_to_action_group(self, name=None, actionname=None):
		actionname = self.ALL_VIEW_ACTIONS.get(actionname)
		return self.ACTION_GROUPS.get(name).addAction(actionname)


class PrefMenuActions(QMenu):
	"""Holds and defines all Preference Menu actions"""
	def __init__(self, parent=None):
		super(PrefMenuActions, self).__init__(parent)
		self.ALL_PREF_ACTIONS = {}
		self.setTitle("Preferences")
		self.create_action("font_inc_act", "Increase Font Size", "Ctrl+=")
		self.create_action("font_dec_act", "Decrease Font Size", "Ctrl+-")
		self.create_action("serif_font_act", "Serif")
		self.create_action("monospace_font_act", "Monospace")
		self.create_action("sans_serif_font_act", "Sans-Serif")
		self.create_action("invert_act", "Inverse Theme Colors")
		
		# usermenu = preferences.addMenu("User Settings")
		# fontmenu = preferences.addMenu("Font Size")
		# fontstylemenu = preferences.addMenu("Font Style")
		# themesmenu = preferences.addMenu("PyCodeThemes")

	def create_action(self, name=None, menutext=None, shortcut=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_PREF_ACTIONS[str(name)] = QAction(menutext, self)
		if shortcut:
			self.ALL_PREF_ACTIONS.get(name).setShortcut(shortcut)
		self.addAction(self.ALL_PREF_ACTIONS.get(name))


class FileMenuTriggers(FileMenuActions):
	def __init__(self, parent=None):
		super(FileMenuTriggers, self).__init__(parent)

		self.F_DICT = self.ALL_FILE_ACTIONS.get

		self.F_DICT("exit_act").triggered.connect(self.exit_event)
		self.F_DICT("newW_act").triggered.connect(self.new_window)
		self.F_DICT("closeW_act").triggered.connect(self.close_window)

		self.F_DICT("save_act").triggered.connect(self.parent().tab_interface.save_event)
		self.F_DICT("openF_act").triggered.connect(self.parent().tab_interface.open_file_dialog)
		self.F_DICT("save_as_act").triggered.connect(self.parent().tab_interface.save_file_as)
		self.F_DICT("newF_act").triggered.connect(self.parent().tab_interface.new_file)
		self.F_DICT("save_all_act").triggered.connect(self.parent().tab_interface.save_all)
		self.F_DICT("close_all_act").triggered.connect(self.parent().tab_interface.close_all)
		self.F_DICT("reopenF_act").triggered.connect(self.parent().tab_interface.reopen_last_tab)
		self.F_DICT("closeF_act").triggered.connect(self.parent().tab_interface.close_tab)

	def new_window(self):
		"""opens a completely new window."""
		self.new_window_instance = PyCodeEditor()
		return self.new_window_instance.show()

	def close_window(self):
		"""Close active window"""
		return self.close()
	
	def exit_event(self):
		"""Exits without prompting"""
		sys.exit()


class EditMenuTriggers(EditMenuActions):
	def __init__(self, parent=None):
		super(EditMenuTriggers, self).__init__(parent)

		# edit menu triggers
		self.E_DICT = self.ALL_EDIT_ACTIONS.get

		self.E_DICT("find_act").triggered.connect(self.parent().tab_interface.find_text)
		self.E_DICT("redo_act").triggered.connect(self.parent().tab_interface.redo_last)
		self.E_DICT("undo_act").triggered.connect(self.parent().tab_interface.undo_last)
		self.E_DICT("cut_act").triggered.connect(self.parent().tab_interface.cut_selection)
		self.E_DICT("paste_act").triggered.connect(self.parent().tab_interface.paste_selection)
		self.E_DICT("clone_act").triggered.connect(self.parent().tab_interface.clone_doc)


class ViewMenuTriggers(ViewMenuActions):
	def __init__(self, parent=None):
		super(ViewMenuTriggers, self).__init__(parent)

		# view menu triggers
		self.V_DICT = self.ALL_VIEW_ACTIONS.get

		self.V_DICT("hide_status_act").triggered.connect(self.parent().tab_page.hide_statusbar)
		self.V_DICT("python_syn").triggered.connect(self.parent().tab_page.python_syntax)
		self.V_DICT("plain_syn").triggered.connect(self.parent().tab_page.plain_text)
		self.V_DICT("html_syn").triggered.connect(self.parent().tab_page.html_syntax)
		# self.V_DICT(plainL).triggered.connect(self.plain_layout)
		# self.V_DICT(splitL).triggered.connect(self.split_screen_layout)
		# self.V_DICT(gridL).triggered.connect(self.grid_layout)


class ToolMenuTriggers(ToolMenuActions):
	def __init__(self, parent=None):
		super(ToolMenuTriggers, self).__init__(parent)

		# tool menu triggers
		self.T_DICT = self.ALL_TOOL_ACTIONS.get

		# self.T_DICT("tab_act_1").triggered.connect(partial(self.tab_page.set_tab_width, 10))
		# self.T_DICT("tab_act_2").triggered.connect(partial(self.tab_page.set_tab_width, 20))
		# self.T_DICT("tab_act_3").triggered.connect(partial(self.tab_page.set_tab_width, 30))
		# self.T_DICT("tab_act_4").triggered.connect(partial(self.tab_page.set_tab_width, 40))
		# self.T_DICT("tab_act_5").triggered.connect(partial(self.tab_page.set_tab_width, 50))
		# self.T_DICT("tab_act_6").triggered.connect(partial(self.tab_page.set_tab_width, 60))
		# self.T_DICT("tab_act_7").triggered.connect(partial(self.tab_page.set_tab_width, 70))
		# self.T_DICT('tab_act_8').triggered.connect(partial(self.tab_page.set_tab_width, 80))


class PrefMenuTriggers(PrefMenuActions):
	def __init__(self, parent=None):
		super(PrefMenuTriggers, self).__init__(parent)

		# preferences menu triggers
		self.P_DICT = self.ALL_PREF_ACTIONS.get
		self.P_DICT("font_inc_act").triggered.connect(self.parent().tab_interface.increase_font_size)
		self.P_DICT("font_dec_act").triggered.connect(self.parent().tab_interface.decrease_font_size)
		self.P_DICT("serif_font_act").triggered.connect(self.parent().tab_interface.set_serif)
		self.P_DICT("monospace_font_act").triggered.connect(self.parent().tab_interface.set_monospace)
		self.P_DICT("sans_serif_font_act").triggered.connect(self.parent().tab_interface.set_sansserif)

		
class PyCodeShortcuts(object):
	"""Responsible for creating/holding all active Shortcuts"""

	def __init__(self, parent=None):

		self._ALL_SHORTCUTS = {}
		self.create_shortcut("move_right", "Ctrl+pgup", parent, True)
		self.create_shortcut("move_right2", "Ctrl+Tab", parent, True)
		self.create_shortcut("move_left", "Ctrl+pgdn", parent, True)
		self.create_shortcut("move_left2", "Ctrl+Shift+Tab", parent, True)
		self.create_shortcut("close_focused_win", "Ctrl+Shift+W", parent)
		self.create_shortcut("close_dock", "Esc", parent)

	def create_shortcut(self, name=None, short=None, parent=None, auto=False):
		"""Creates Shortcut"""
		self._ALL_SHORTCUTS[name] = QShortcut(short, parent)
		if auto:
			self._ALL_SHORTCUTS.get(name).setAutoRepeat(auto)



def main():
	pycodeapp = QApplication(sys.argv)
	editor = PyCodeEditor()

	try:
		with open("../PyCodeThemes/PyCodeCrimson.qss") as f:
			stylesheet = f.read()
			pycodeapp.setStyleSheet(stylesheet)
	except IOError:
		print "Cannot find Stylesheet; falling back to native style"

	editor.show()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
