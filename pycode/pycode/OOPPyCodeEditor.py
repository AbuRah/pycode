"""
	This file is part of PyCode Text Editor.

    PyCode Text Editor is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyCode Text Editor is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with PyCode Text Editor.  If not, see <http://www.gnu.org/licenses/>.

    Copyright 2014, Abu Rah 82013248a@gmail.com

"""

#-*-coding:utf-8-*-

import sys, os, codecs, re

from PySide.QtCore import *
from PySide.QtGui import *

from SyntaxClasses import *
from functools import partial


class PyCodeAction(QAction):
	"""Reimplemented in order to override __repr__ special method. Besides that,
		there is no difference between this and the original QAction.
	"""
	def __init__(self, name=None, text="default", parent=None):
		super(PyCodeAction, self).__init__(text, parent)
		self.name = name

	def __repr__(self):
		return self.name


class PyCodeMenuBar(QMenuBar):
	"""Responsible for holding all menus and menu actions.

	"""
	def __init__(self, parent=None):
		super(PyCodeMenuBar, self).__init__(parent)
		self.P = parent

		self.FILE = FileMenuTriggers("&File", parent)
		self.EDIT = EditMenuTriggers("Edit", parent)
		self.VIEW = ViewMenuTriggers("View", parent)
		self.TOOL = ToolMenuTriggers("&Tool", parent)
		self.PREF = PrefMenuTriggers("&Preferences", parent)
		self.addMenu(self.FILE)
		self.addMenu(self.EDIT)
		self.addMenu(self.VIEW)
		self.addMenu(self.TOOL)
		self.addMenu(self.PREF)

	def set_CHILD_constant(self):
		"""Sets pycodetop child to all necessary triggers menus
			Be sure that any sub-menus that are trigger classes are updated
			as well...e.g. encoding sub-menus
		"""
		self.FILE.P_C = self.P.CHILD
		self.FILE.update_triggers()
		self.FILE.enc_save.PP_C = self.P.CHILD
		self.FILE.enc_open.PP_C = self.P.CHILD
		self.EDIT.P_C = self.P.CHILD
		self.VIEW.P_C = self.P.CHILD
		self.TOOL.P_C = self.P.CHILD
		self.PREF.P_C = self.P.CHILD
		self.P.CHILD.currentChanged.connect(self.update_triggers)


	def update_triggers(self):
		"""Here, we set all triggermenu actions to appropriate slots
			Everytime the user changes a tab page, all menubar relevant actions
			will point to the current tab page, disconnecting from the previous
			tab page first.
		"""
		self.FILE.enc_save.update_connections()
		self.FILE.enc_open.update_connections()
		self.EDIT.update_connections()
		self.VIEW.update_connections()
		self.TOOL.update_connections()
		self.PREF.update_connections()

	def __repr__(self):
		return "PyCodeMenuBar Instance"


class PyCodeIdentifier(QObject):
	"""Responsible for holding all supported extension types for syntax highlighting.
		If extension type is not supported, syntax setting defaults to plainText.
	"""
	def __init__(self, parent=None):
		super(PyCodeIdentifier, self).__init__(parent)

		self.EXT = {"py": PythonSyntax,
				"html": HtmlSyntax,
				"css": CSSSyntax,
				"txt": PlainText}

	def find_type(self, ext):
		"""Checks for extension in dictionary of supported syntaxs"""

		lst = [i for i in self.EXT.keys()]
		if ext in lst:
			return self.EXT[ext]
		else:
			return PlainText


class PyCodeDialogWindow(QDialog):
	def __init__(self, parent=None):
		super(PyCodeDialogWindow, self).__init__(parent)
		self.set_attributes()

	def set_attributes(self):
		self.setSizeGripEnabled(True)

		
	def initUI(self):
		self.ok = QPushButton("OK", self)
		self.cancel = QPushButton("CANCEL", self)

class PyCodeTabInterface(QTabWidget):
	"""This class and the PyCodePage class are where most of the relevant slots and
		modifications will be. i.e. if you want to find where cursor manipulation takes
		place, it would be in one of these classes.
		
		Whenever the actor changes tabs, the menubar and statusbar will both be automatically
		updated to reflect the pycodepage instance's menubar and statusbar. It will then
		set PyCodeTop to hold these updated status/menubars.
		The _SYNTAX_DICT constant holds the syntax highlighting class applied to it's
		respective document. e.g. if PythonSyntax is set for the first tab page, 
		HTML for the second, their respective entries will look like this::
	
		>> self._SYNTAX_DICT[0]
		"Python"

		>> self._SYNTAX_DICT[1]
		"HTML"

		etc....


	"""


	CLOSED_TABS = []
	SYNTAX_DICT = {}

	def __init__(self, parent=None):
		super(PyCodeTabInterface, self).__init__(parent)
		self.init_setup()
		self.IDENTIFIER = PyCodeIdentifier(self)
		self.P = parent
		# i can set signals here instead...
		

	def init_setup(self):
		"""Sets up all options pertinent to QTabWidget"""
		self.setFocusPolicy(Qt.NoFocus)
		self.setTabsClosable(True)
		self.setMovable(True)
		self.setElideMode(Qt.ElideRight)


	def set_signal_slots(self):
		self.currentChanged.connect(self.grab_sm_bars)
		self.currentChanged.connect(self.set_syntax)
		self.tabCloseRequested.connect(self.close_tab)


	def set_syntax(self):
		"""sets appropriate syntax highlighting"""

		if self.count() and self.SYNTAX_DICT:
			set_syn = self.SYNTAX_DICT.get(self.currentIndex())
			set_syn()

	def grab_sm_bars(self):
		"""grabs menus from mainwindow"""
		self.MENU = self.P.menuBar()
		self.STATUS = self.P.statusBar()

	def new_file(self):
		"""Creates a new file"""
		page = PyCodePage(self)
		PlainText(page.document())
		return self.addTab(page, "Untitled")

		#testing
	def open_file_dialog(self, enc="utf-8"):
		"""opens file in new tab"""

		# does not pass arg if called from open w/ encoding menu...

		file_name,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if file_name != '':

			with codecs.open(file_name, "r", enc) as f:
				
				data = f.read()
				new_page = PyCodePage(self)
				new_page.setPlainText(data)
				f.close()
				
				# codense the following two lines of code
				nameHolder = QFileInfo(file_name)
				nameOfFile = nameHolder.fileName()

				syntax = self.get_syntax_highlighter(nameOfFile)
				syntax(new_page.document())
				
				self.addTab(new_page, nameOfFile)
		else:
			print "open file failed"

	# # practice/testing
	# def testing(self, enc):
	# 	# when opening file use decode(encoding specified)
	# 	data = f.read()
	# 	data.decode(enc)
	# 	# when writing to file, use encode(encoding specified)


	def get_syntax_highlighter(self, file_name):
		"""Sets the new file's syntax highlighting,
			Defaulting to PlainText if not supported.
			"""
		ext = self.get_extension(file_name)
		set_syntax = self.IDENTIFIER.find_type(ext)
		return set_syntax

	def get_extension(self, file_name):
		"""retrieves file object extension"""
		pattern = re.compile("(?<=\.).*\.?.*$")
		result = re.search(pattern, file_name)
		if result:
			return result.group()
		else:
			return "txt"


	def save_event(self, enc="utf-8"):
		"""Saves current file, except if "Untitled"; it will prompt user
			to save.
		"""
			
		file_name = self.tabText(self.currentIndex())		
		save_file = QFile(file_name)

		if file_name != "Untitled":
			f = open(file_name, "w")

			with f:
				data = self.currentWidget().toPlainText()
				try:
					codecs.encode(data, enc)
					f.write(data)

				except ValueError:
					print "error processing goes here"

				finally:
					f.close()
				
				self.P.statusBar().showMessage(
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

		return self.P.statusBar().showMessage(
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

				syntax = self.get_syntax_highlighter(nameOfFile)
				syntax(new_page.document())

				self.setTabText(self.currentIndex(), nameOfFile)
		
		else:
			pass

	def reopen_last_tab(self):
		"""Opens the last tab closed"""

		if len(self.CLOSED_TABS) > 0:

			new_page = PyCodePage(self)
			last_file = self.CLOSED_TABS.pop()

			try:

				with open(last_file, "r") as f:
					data = f.read()
					new_page.setPlainText(data)

					syntax = self.get_syntax_highlighter(last_file)
					syntax(new_page.document())
		
					self.addTab(new_page, last_file)
					self.currentWidget().setFocus()
		
			except IOError:
				pass

		else:
			pass

	def close_tab(self):
		"""Closes focused tab"""
		
		file_name = self.tabText(self.currentIndex())

		self.CLOSED_TABS.append(file_name)
		self.removeTab(self.currentIndex())


		try:
			return self.currentWidget().setFocus()
		
		except AttributeError:
			pass

	def close_all(self):
		"""Closes all open files"""
		for i in xrange(self.count()):
			self.close_tab()

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
	

	

	# broken
	# def find_text(self):
	# 	"""Find the indicated text within the current tab page"""
	# 	### need to add auto-complete, find & replace
	# 	Dock_widget = self.P.parent().DOCKW
	# 	Dock_widget.show()
	# 	Dock_widget.user_input.setFocus()

	# 	_TESTING = QTextCursor(self.currentWidget().textCursor())
		
	# 	if self.currentWidget().textCursor().position() != 0:
			
	# 		update = self.currentWidget().DOC.find(self.user_input.text())
	# 		self.currentWidget().setTextCursor(update)
	# 		self.currentWidget().textCursor().select(QTextCursor.WordUnderCursor)

	def __repr__(self):
		return "PyCodeTabInterface"


class PyCodePage(QTextEdit):
	"""Responsible for all signals and method-functions related ONLY to QTextEdit.
		I may make a class specifically for all QTextEdit related signal connections.
		Use the PyCodePage.Doc in order to access the current QTextDocument.
		

	"""
	def __init__(self, parent=None):
		super(PyCodePage, self).__init__(parent)
		self.tmp_counter = 0
		self.TI = parent
		self.setTabStopWidth(40)
		# i could change this...
		self.grab_sm_bars()

		self.textChanged.connect(self.modified_since_save)
		self.cursorPositionChanged.connect(self.column_line_update)

	def grab_sm_bars(self):
		"""Takes control of menu and status bars
			Should only run once as a part of initial set-up
		"""
		self.STATUS = self.TI.STATUS
		self.MENU = self.TI.MENU

	def modified_since_save(self):
		"""Causes tab text to change if modified since last save"""
		return self.TI.tabBar().setTabTextColor(
			self.TI.currentIndex(), QColor("#fff5ee"))

	def set_tab_width(self, num):
		return self.setTabStopWidth(num)

	def column_line_update(self):
		"""updates current cursor position in document"""
		return self.STATUS.line_count.setText("Line: %d, Column: %d" % (
			self.textCursor().blockNumber()+1, 
			self.textCursor().columnNumber()+1))

	def clone_line(self):
		"""Clones current line cursor is found in"""
		cursor = self.textCursor()
		cursor.beginEditBlock()
		cursor.movePosition(QTextCursor.StartOfLine)
		cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)
		self.copy()
		cursor.clearSelection()
		cursor.movePosition(QTextCursor.Down)
		cursor.insertBlock()
		self.setTextCursor(cursor)
		self.paste()
		cursor.movePosition(QTextCursor.StartOfBlock)
		cursor.endEditBlock()

	def line_up(self):
		"""Moves current line block up one block level"""
		cursor = self.textCursor()
		cursor.beginEditBlock()

		cursor.endEditBlock()
	
	def line_down(self):
		"""Moves current line block down one level"""
		cursor = self.textCursor()

	def current_line_select(self):
		"""Selects current line cursor is found in"""
		cursor = self.textCursor()
		cursor.movePosition(QTextCursor.StartOfLine)
		cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
		self.setTextCursor(cursor)

	def delete_line(self):
		"""Deletes current line cursor is found in"""
		cursor = self.textCursor()
		cursor.beginEditBlock()
		
		if cursor.hasSelection():
			cursor.removeSelectedText()
		else:
			cursor.movePosition(QTextCursor.StartOfLine)
			cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
			cursor.removeSelectedText()
		cursor.endEditBlock()

	def paste_and_indent(self):
		"""Paste from clipboard with indent"""
		# cursor = self.textCursor()
		# oldpos = self.textCursor().position()
		indent = self.document().indentWidth()
		self.insertPlainText(indent)
		# cursor.setPosition(oldpos + indent)
		# self.setTextCursor(cursor)
		self.paste()


	# i may need to create a class to hold all syntax slots
	def css_syntax(self):
		"""sets CSS syntax highlighting"""
		CSSSyntax(self.document())
		self.TI.SYNTAX_DICT[self.TI.currentIndex()] = self.css_syntax
		self.STATUS.current_syntax.setText("CSS")

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.document())
		self.TI.SYNTAX_DICT[self.TI.currentIndex()] = self.python_syntax
		self.STATUS.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.document())
		self.TI.SYNTAX_DICT[self.TI.currentIndex()] = self.plain_text
		self.STATUS.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.document())
		self.TI.SYNTAX_DICT[self.TI.currentIndex()] = self.html_syntax
		self.STATUS.current_syntax.setText("HTML") 

	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		return self.paste()

	def undo_last(self):
		"""Steps back in operation history"""
		return self.undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		return self.redo()

	def clone_doc(self):
		"""clones current document in focus"""
		cloned_doc = self.document().clone(self)
		new_page = PyCodePage(self.TI)
		new_page.setDocument(cloned_doc)
		return self.TI.addTab(new_page, "Untitled")

	def find_regexp(self):
		"""finds text in doc using regexp"""
		pass

	def increase_font_size(self):
		"""Incrementally increases font point size"""
		self.selectAll()
		currentF = self.currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()+ 1)
		self.setCurrentCharFormat(currentF)
		# cursor = self.textCursor()
		# cursor.clearSelection()
		# self.setTextCursor(cursor)

	def decrease_font_size(self):
		"""Incrementally decreases font point size"""
		self.selectAll()
		currentF = self.currentCharFormat()
		currentF.setFontPointSize(currentF.fontPointSize()- 1)
		if currentF.fontPointSize() > 0:
			return self.setCurrentCharFormat(currentF)
		else:
			pass

	def set_word_wrap(self):

		off = QTextOption.NoWrap

		if self.wordWrapMode() != off:
			print "shuting off"
			self.setWordWrapMode(QTextOption.NoWrap)
		else:
			print "turning on"
			self.setWordWrapMode(QTextOption.WordWrap)


	#testing zoom functions
	def zoom_in(self):
		return self.zoomIn()

	def zoom_out(self):
		return self.zoomOut()

	def set_serif(self):
		"""Set all text to serif font family"""
		self.selectAll()
		currentF = self.currentCharFormat()
		currentF.setFontFamily("serif")
		self.setCurrentCharFormat(currentF)

	def set_monospace(self):
		"""Set all text to monospace font family"""
		self.selectAll()
		currentF = self.currentCharFormat()
		currentF.setFontFamily("monospace")
		self.setCurrentCharFormat(currentF)

	def set_sansserif(self):
		"""Set all text to sans-serif font family"""
		self.selectAll()
		currentF = self.currentCharFormat()
		currentF.setFontFamily("sans-serif")
		self.setCurrentCharFormat(currentF)

	def copy_selection(self):
		"""Copies current text selection"""
		if self.textCursor().hasSelection():
			return self.copy()
		else:
			cursor = self.textCursor()
			cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
			self.setTextCursor(cursor)
			self.copy()
			cursor.clearSelection()
			self.setTextCursor(cursor)

	def cut_selection(self):
		"""copy/cut selected text"""
		if self.textCursor().hasSelection():
			return self.cut()
		else:
			cursor = self.textCursor()
			cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
			cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
			self.setTextCursor(cursor)
			self.cut()

	def hide_statusbar(self):
		"""Hides status bar"""
		if self.tmp_counter == 0:
			self.STATUS.hide()
			self.tmp_counter += 1
		else:
			self.STATUS.show()
			self.tmp_counter -= 1


# testing remove afterwards
class PyCodeSyntaxSlots(QObject):
	"""Responsible for holding all syntax slots
		In experimental
	"""
	def __init__(self, parent=None):
		super(PyCodeSyntaxSlots, self).__init__(parent)
		self.P = parent

	def css_syntax(self):
		"""sets CSS syntax highlighting"""
		CSSSyntax(self.P.document())
		self.P.TI.SYNTAX_DICT[self.P.TI.currentIndex()] = self.css_syntax
		self.P.STATUS.current_syntax.setText("CSS")

	def python_syntax(self):
		"""sets python syntax highlighting for textdocument in focus"""
		PythonSyntax(self.P.document())
		self.P.TI.SYNTAX_DICT[self.P.TI.currentIndex()] = self.python_syntax
		self.P.STATUS.current_syntax.setText("Python")

	def plain_text(self):
		"""Sets plain text syntax highlighting for textdocument in focus"""
		PlainText(self.P.document())
		self.P.TI.SYNTAX_DICT[self.P.TI.currentIndex()] = self.plain_text
		self.P.STATUS.current_syntax.setText("PlainText")

	def html_syntax(self):
		"""sets syntax highlighting to HTML"""
		HtmlSyntax(self.P.document())
		self.P.TI.SYNTAX_DICT[self.P.TI.currentIndex()] = self.html_syntax
		self.P.STATUS.current_syntax.setText("HTML") 


class PyCodeStatusBar(QStatusBar):
	""" Responsible for individual statusbars' slots and signals"""
	def __init__(self, parent=None):
		super(PyCodeStatusBar, self).__init__(parent)
		self.showMessage("Ready", 4000)
		
		self.line_count = QLabel()
		self.current_syntax = QLabel()
		self.addPermanentWidget(self.line_count)
		self.addPermanentWidget(self.current_syntax)

	def __repr__(self):
		return "PyCodeStatusBar Instance"


# MENU CLASSES=================

	
class PyCodeMenu(QMenu):
	""" This Menu will hold all of the common functionality between 
		the pycode menus
		"""
	def __init__(self, name="Default", parent=None):
		super(PyCodeMenu, self).__init__(parent)
		self.name = name
		self.ALL_ACTIONS = {}
		self.ACTION_GROUPS = {}
		self.P = parent
		self.setTitle(str(name))
		
	def create_action(self, name=None, menutext=None, short=None, status=None):
		"""Creates a new action and automatically adds it to itself"""
		self.ALL_ACTIONS[str(name)] = PyCodeAction(name, menutext, self)
		if short:
			self.ALL_ACTIONS.get(name).setShortcut(short)
		if status:
			self.ALL_ACTIONS.get(name).setStatusTip(status)
		self.addAction(self.ALL_ACTIONS.get(name))

	def create_action_group(self, name=None):
		self.ACTION_GROUPS[name] = QActionGroup(self)

	def add_to_action_group(self, name=None, actionname=None):
		actionname = self.ALL_ACTIONS.get(actionname)
		return self.ACTION_GROUPS.get(name).addAction(actionname)

	def __repr__(self):
		return self.name


class FileMenu(PyCodeMenu):
	"""Responsible for all FileMenu specific actions, signal/slot connections 
		are NOT to be made here.
		The most common selections in a file menu will be added by default,
		however, all defined by user. Can be
		extended with the create_action method-function.
	"""

	def __init__(self, name="Default", parent=None):
		super(FileMenu, self).__init__(name, parent)
		self.enc_open = OpenEncMenuTriggers("Open With Encoding", self)
		self.enc_save = SaveEncMenuTriggers("Save With Encoding", self)
		self.FILE_ACTIONS = self.ALL_ACTIONS

		self.addSeparator()
		self.create_action("newF_act", "New File", "Ctrl+N", "Create New document")
		self.create_action("newW_act", "New Window", "Ctrl+Shift+N", "Create New Window")
		self.create_action("openF_act", "Open File", "Ctrl+O", "Open File")
		self.addMenu(self.enc_open)
		self.create_action("reopenF_act", "Reopen Last Tab", "Ctrl+Shift+T", "Re-open last tab")
		self.addSeparator()
		self.create_action("save_act", "Save", "Ctrl+S", "Save Current Document")
		self.create_action("save_as_act", "Save as...", "Ctrl+Shift+S", "Save file as...")
		self.create_action("save_all_act", "Save All Files")
		self.addMenu(self.enc_save)
		self.addSeparator()
		self.create_action("closeF_act", "Close Tab", "Ctrl+W", "Close current Tab Page")
		self.create_action("closeW_act", "Close Window", "Ctrl+Shift+W", "Close Active Window")
		self.create_action("close_all_act", "Close all Files", status="Close all open tabs")
		self.create_action("exit_act", "Exit", "Ctrl+Q", "Exit the Application")


class EditMenu(PyCodeMenu):

	def __init__(self, name="Default", parent=None):
		super(EditMenu, self).__init__(name, parent)
		self.EDIT_ACTIONS = self.ALL_ACTIONS
		self.create_action("redo_act", "Redo", "Ctrl+Shift+Z")
		self.create_action("undo_act", "Undo", "Ctrl+Z")
		self.addSeparator()
		self.create_action("paste_act", "Paste", "Ctrl+V")
		self.create_action("cut_act", "Cut", "Ctrl+X")
		self.create_action("copy_act", "Copy", "Ctrl+C")
		self.create_action("clone_act", "Clone Current Document", 
						status="Clones currently opened file")
		self.addSeparator()
		self.create_action("bold_act", "Bold", "Ctrl+B")
		self.addSeparator()
		self.create_action("find_act", "Find", "Ctrl+F")
		self.create_action("find_regexp_act", "Find RegExp")
		self.create_action("find_and_replace_act", "Search & Replace")
		self.addSeparator()
		self.create_action("delete_line", "Delete Line", "Ctrl+k")
		self.create_action("line_up", "Move line up", "Ctrl+Shift+Up")
		self.create_action("line_down", "Move line down", "Ctrl+Shift+Down")
		self.create_action("clone_line", "Clone current line", "Ctrl+Shift+D")
		self.create_action("line_select", "Select current line", "Ctrl+L")
		self.create_action("indent_paste", "Paste and indent", "Shift+Ctrl+V")


class ViewMenu(PyCodeMenu):
	"""Defines and Holds all view menu specific actions
		If there are any sub-menus for the view menu, be sure to update
		the main self.VIEW_ACTIONS dictionary appropriately.
	"""
	def __init__(self, name="Default", parent=None):
		super(ViewMenu, self).__init__(name, parent)
		self.VIEW_ACTIONS = self.ALL_ACTIONS
		self.create_action("zoom_in", "Zoom In")
		self.create_action("zoom_out", "Zoom Out")
		self.addSeparator()
		self.create_action("plain_lay_act", "Single Screen")
		self.create_action("split_lay_act", "Split Screen")
		self.create_action("grid_lay_act", "Grid Screen")
		self.addSeparator()
		syntax_menu = SyntaxMenu("Syntax", self)
		self.VIEW_ACTIONS.update(syntax_menu.SYN_ACTIONS)
		self.addMenu(syntax_menu)
		self.create_action("hide_status_act", "Hide Status Bar")
		self.VIEW_ACTIONS.get("hide_status_act").setCheckable(True)
		self.addSeparator()
		self.create_action("word_wrap_act", "Word Wrapping")
		self.VIEW_ACTIONS.get("word_wrap_act").setCheckable(True)
		self.VIEW_ACTIONS.get("word_wrap_act").setChecked(True)


class ToolMenu(PyCodeMenu):
	"""Holds and Defines all ToolMenu specific actions
		if ANY sub-menus are added, be sure to update the TOOL_ACTIONS
		dictionary.
	"""
	def __init__(self, name="Default", parent=None):
		super(ToolMenu, self).__init__(name, parent)
		self.TOOL_ACTIONS = self.ALL_ACTIONS
		tab_width_menu = TabWidthMenu("Tab Width", self)
		self.TOOL_ACTIONS.update(tab_width_menu.TABW_ACTIONS)
		self.addMenu(tab_width_menu)
		self.addSeparator()
		# not yet implemented
		self.create_action("snippet_act", "Code Snippets", status="Browse Snippet lib")
		self.create_action("build_act", "Build", status="builds current code")
		self.addSeparator()


class PrefMenu(PyCodeMenu):
	"""Holds and defines all Preference Menu actions
		If **Any** sub-menus are added, be sure to update the main
		PREF_ACTIONS dictionary.
	"""
	def __init__(self, name=None, parent=None):
		super(PrefMenu, self).__init__(name, parent)
		self.PREF_ACTIONS = self.ALL_ACTIONS
		font_menu = PrefFontMenu("Font", self)
		theme_menu = ThemesMenu("Themes", self)
		self.PREF_ACTIONS.update(font_menu.PREF_FONT_ACTIONS)
		self.PREF_ACTIONS.update(theme_menu.THEMES_ACTIONS)
		self.addMenu(font_menu)
		self.addMenu(theme_menu)
		# usermenu = preferences.addMenu("User Settings")


class TabWidthMenu(PyCodeMenu):
	def __init__(self, name=None, parent=None):
		super(TabWidthMenu, self).__init__(name, parent)
		self.TABW_ACTIONS = self.ALL_ACTIONS
		self.create_action("tab_act_1", "Set tab width 1")
		self.create_action("tab_act_2", "Set tab width 2")
		self.create_action("tab_act_3", "Set tab width 3")
		self.create_action("tab_act_4", "Set tab width 4")
		self.create_action("tab_act_5", "Set tab width 5")
		self.create_action("tab_act_6", "Set tab width 6")
		self.create_action("tab_act_7", "Set tab width 7")
		self.create_action("tab_act_8", "Set tab width 8")


class PrefFontMenu(PyCodeMenu):
	def __init__(self, name=None, parent=None):
		super(PrefFontMenu, self).__init__(name, parent)
		self.PREF_FONT_ACTIONS = self.ALL_ACTIONS
		self.create_action("font_inc_act", "Increase Font Size", "Ctrl+=")
		self.create_action("font_dec_act", "Decrease Font Size", "Ctrl+-")
		self.addSeparator()
		self.create_action("serif_font_act", "Serif")
		self.create_action("monospace_font_act", "Monospace")
		self.create_action("sans_serif_font_act", "Sans-Serif")


class ThemesMenu(PyCodeMenu):
	def __init__(self, name=None, parent=None):
		super(ThemesMenu, self).__init__(name, parent)
		self.THEMES_ACTIONS = self.ALL_ACTIONS
		self.create_action("invert_act", "Inverse Theme Colors")


class SyntaxMenu(PyCodeMenu):
	"""The Syntax sub-menu is defined here. If any additions need to be made,
		make them here.
	"""
	def __init__(self, name=None, parent=None):
		super(SyntaxMenu, self).__init__(name, parent)
		self.SYN_ACTIONS = self.ALL_ACTIONS
		self.create_action("python_syn", "Python")
		self.create_action("plain_syn", "PlainText")
		self.create_action("html_syn", "HTML")
		self.create_action("css_syn", "CSS")


class WindowsEncodingMenu(PyCodeMenu):
	"""Responsible for holding all Windows specific charset encodings"""
	def __init__(self, name=None, parent=None):
		super(WindowsEncodingMenu, self).__init__(name, parent)
		self.WIN_ENC = self.ALL_ACTIONS
		self.create_action("windows1250_act", "Central European(Windows1250)", status="Windows1250")
		self.create_action("windows1251_act", "Cyrillic(Windows1251)", status="Windows1251")
		self.create_action("windows1252_act", "Western(Windows1252)", status="Windows1252")
		self.create_action("windows1253_act", "Greek(Windows1253)", status="Windows1253")
		self.create_action("windows1254_act", "Turkish(Windows1254)", status="Windows1254")
		self.create_action("windows1255_act", "Hebrew(Windows1255)", status="Windows1255")
		self.create_action("windows1256_act", "Arabic(Windows1256)", status="Windows1256")
		self.create_action("windows1257_act", "Baltic(Windows1257)", status="Windows1257")
		self.create_action("windows1258_act", "Vietnamese(Windows1258)", status="Windows1258")


class EuropeanEncodingMenu(PyCodeMenu):
	"""Responsible for carrying all Eastern European charset Encodings."""
	def __init__(self, name=None, parent=None):
		super(EuropeanEncodingMenu, self).__init__(name, parent)
		self.ISO_ENC = self.ALL_ACTIONS
		# need to check these out, some may be redundant
		self.create_action("iso8859_1_act", "Western (ISO8859-1)", status="ISO8859-1")
		self.create_action("iso8859_2_act", "Western && Central Europe (ISO8859-2)", status="ISO8859-2")
		self.create_action("iso8859_3_act", "Western/Southern European (ISO8859-3)", status="ISO8859-3")
		self.create_action("iso8859_4_act", "W Europe && Baltic (ISO8859-4)", status="ISO8859-4")
		self.create_action("iso8859_5_act", "Cyrillic (ISO8859-5)", status="ISO8859-5")
		self.create_action("iso8859_6_act", "Arabic (ISO8859-6)", status="ISO8859-6")
		self.create_action("iso8859_7_act", "Greek (ISO8859-7)", status="ISO8859-7")
		self.create_action("iso8859_8_act", "Hebrew (ISO8859-8)", status="ISO8859-8")
		self.create_action("iso8859_9_act", "W Europe w/Turkish set (ISO8859-9)", status="ISO8859-9")
		self.create_action("iso8859_10_act", "W Europe w/Nordic Icelandic set (ISO8859-10)", status="ISO8859-10")
		self.create_action("iso8859_11_act", "Thai (ISO8859-11)", status="ISO8859-11")
		self.create_action("iso8859_13_act", "Baltic w/Polish set (ISO8859-13)", status="ISO8859-13")
		self.create_action("iso8859_14_act", "Celtic (ISO8859-14)", status="ISO8859-14")
		self.create_action("iso8859_15_act", "unknown (ISO8859-15)", status="ISO8859-15")
		self.create_action("iso8859_16_act", "Central/Eastern/Southern European (ISO8859-16)", status="ISO8859-16")


class MainEncodingMenu(PyCodeMenu):
	"""Displays the more commonly used char set encodings.
		The actions from it's sub-menus are added with update_dict()
		The menus must be created first otherwise the program will not run.
	"""
	def __init__(self, name=None, parent=None):
		super(MainEncodingMenu, self).__init__(name, parent)
		self.make_menus()
		self.update_dict()
		self.create_action("utf8_act", "UTF-8", status="UTF-8")
		self.create_action("utf16_act", "UTF-16LE", status="UTF-16 Little Endian")
		self.create_action("utf16_act", "UTF-16BE", status="UTF-16 Big Endian")
		self.create_action("utf32_act", "UTF-32", status="UTF-32")
		self.create_action("macos_roman_act", "Mac Roman", status="Mac OS Roman")
		self.create_action("k018_u_act", "Russian(K018-U)", status="K018-U")
		self.create_action("k018_r_act", "Russian(K018-R)", status="K018-R")
		self.create_action("k017_act", "Russian(K017)", status="K017")
		self.create_action("mik_act", "DOS Cyrillic", status="MIK")
		self.addSeparator()
		self.addMenu(self.win_menu)
		self.addMenu(self.iso_menu)
		self.create_action("shift_jis_act", "Japenese(Shift_JIS)", status="Shift_JIS")
		self.create_action("iso_2022_jp_act", "Japenese(ISO-2022-JP)", status="ISO-2022-JP")
		self.create_action("iscii_act", "Indian(ISCII)", status="ISCII")
		self.create_action("gbk_act", "Chinese Simplified(GBK)", status="GBK")
		self.create_action("gb18030_act", "Chinese Simplified(GB18030)", status="GB18030")
		self.create_action("big5_act", "Chinese Traditional(Big5)", status="Big-5")
		self.create_action("big5_act", "Chinese Traditional(Big5-HKSCS)", status="Big-5")
		
		# may remove later
		# self.create_action("gb2312_act", "Chinese", "GB2312") may not use
		# self.create_action("ksx1001_act", "UTF-8") may not use
		# self.create_action("euc-kr_act", "UTF-8") may not use
		# self.create_action("jis_x_0208_act", "Japenese", ) may not use
		# self.create_action("euc_jis_act", "UTF-8") may not use
		# self.create_action("iso-2022_act", "UTF-8") may not use

	def update_dict(self):
		"""Adds all actions to main dictionary"""
		self.ENC_MAIN = self.ALL_ACTIONS
		self.ENC_MAIN.update(self.win_menu.ALL_ACTIONS)
		self.ENC_MAIN.update(self.iso_menu.ALL_ACTIONS)

	# i may be able to make a general method in pycodemenu base.
	def make_menus(self):
		"""Constructs submenu constants."""
		self.win_menu = WindowsEncodingMenu("Windows", self)
		self.iso_menu = EuropeanEncodingMenu("European", self)


# TRIGGER CLASSES ============
class OpenEncMenuTriggers(MainEncodingMenu):
	"""defines all encoding Menu signal/slot connections
		This is constructed in the Filemenu class. Watch for 
		dependencies.
	"""
	def __init__(self, name=None, parent=None):
		super(OpenEncMenuTriggers, self).__init__(name, parent)
		self.ENC_GET = self.ENC_MAIN.get
		self.PP_C = parent.parent()

	def update_connections(self):
		"""Calls the relevant update functions"""
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		"""Here we reset all available connections, then call 
			update_triggers() to set to current tab page.
		"""
		for action in self.ENC_MAIN.values():
			action.disconnect(self.PP_C)


	def update_triggers(self):
		"""This method sets all Edit menu actions' connections"""

		# testing...
		# broken; calls open_file_dialog multiple times when used with partial().
		for key, action in self.ENC_MAIN.items():
			action.triggered.connect(self.PP_C.open_file_dialog, key[:-4])

		# will update connections later
		# This is only here for name reference; will remove after testing.
		# self.ENC_GET("utf8_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("utf16_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("utf32_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("macos_roman_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("k018_u_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("k018_r_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1250_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1251_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1252_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1253_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1254_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1255_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1256_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1257_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("windows1258_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_1_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_2_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_3_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_4_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_5_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_6_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_7_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_8_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_9_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_10_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_13_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_14_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_15_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("iso8859_16_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("shift_jis_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("gbk_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("gb18030_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("big5_act").triggered.connect(self.PP_C.open_file_dialog)
		# self.ENC_GET("big5_act").triggered.connect(self.PP_C.open_file_dialog)


class SaveEncMenuTriggers(MainEncodingMenu):
	def __init__(self, name=None, parent=None):
		super(SaveEncMenuTriggers, self).__init__(name, parent)
		self.ENC_S_GET = self.ENC_MAIN.get
		self.PP_C = parent.parent()

	def update_connections(self):
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		for action in self.ENC_MAIN.values():
			action.disconnect(self.PP_C)

	def update_triggers(self):

		for action in self.ENC_MAIN.values():
			action.triggered.connect(self.PP_C.save_event)

		# this is here only for name reference; will remove once done testing.
		# self.ENC_S_GET("utf8_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("utf16_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("utf32_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("macos_roman_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("k018_u_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("k018_r_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1250_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1251_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1252_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1253_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1254_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1255_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1256_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1257_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("windows1258_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_1_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_2_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_3_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_4_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_5_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_6_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_7_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_8_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_9_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_10_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_13_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_14_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_15_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("iso8859_16_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("shift_jis_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("gbk_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("gb18030_act").triggered.connect(self.PP_C.save_event)
		# self.ENC_S_GET("big5_act").triggered.connect(self.PP_C.save_event)


class FileMenuTriggers(FileMenu):
	""" This class holds all file menu action signals and slots.
		P_C holds the Pycode tab interface.

	"""
	def __init__(self, name=None, parent=None):
		super(FileMenuTriggers, self).__init__(name, parent)

		self.F_DICT = self.FILE_ACTIONS.get
		self.P_C = parent
		self.TOP = parent

		self.F_DICT("exit_act").triggered.connect(self.exit_event)
		self.F_DICT("newW_act").triggered.connect(self.new_window)
		self.F_DICT("closeW_act").triggered.connect(self.close_window)

	def update_triggers(self):
		"""updates pertinent triggers to respective slots"""
		# these need to be set after init....
		self.F_DICT("save_act").triggered.connect(self.P_C.save_event)
		self.F_DICT("openF_act").triggered.connect(self.P_C.open_file_dialog)
		self.F_DICT("save_as_act").triggered.connect(self.P_C.save_file_as)
		self.F_DICT("newF_act").triggered.connect(self.P_C.new_file)
		self.F_DICT("save_all_act").triggered.connect(self.P_C.save_all)
		self.F_DICT("close_all_act").triggered.connect(self.P_C.close_all)
		self.F_DICT("reopenF_act").triggered.connect(self.P_C.reopen_last_tab)
		self.F_DICT("closeF_act").triggered.connect(self.P_C.close_tab)


	def new_window(self):
		"""opens a completely new window."""
		self.new_window_instance = PyCodeTop()
		return self.new_window_instance.show()

	def close_window(self):
		"""Close active window"""
		return self.parent().close()
	
	def exit_event(self):
		"""Exits without prompting"""
		self.TOP.SETTINGS.write_settings()
		sys.exit()


class EditMenuTriggers(EditMenu):
	"""Responsible for all edit menu specific triggers.

	"""
	def __init__(self, name=None, parent=None):
		super(EditMenuTriggers, self).__init__(name, parent)
		self.E_DICT = self.EDIT_ACTIONS.get
		# be wary of this....
		self.P_C, self.P_C_T = parent, parent

	def update_connections(self):
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		"""Here we reset all available connections, then call 
			update_triggers() to set to current tab page.
		"""
		for action in self.EDIT_ACTIONS.values():
				try:
					action.disconnect(self.P_C_T)
				except TypeError, AttributeError:
					print "error processed successfully for EDITS"


	def update_triggers(self):
		"""This method sets all Edit menu actions' connections"""
		self.P_C_T = self.P_C.currentWidget()

		if self.P_C_T:
			# Not yet implemented
			# self.E_DICT("find_act").triggered.connect(self.P_C.currentWidget().find_text)
			self.E_DICT("redo_act").triggered.connect(self.P_C.currentWidget().redo_last)
			self.E_DICT("undo_act").triggered.connect(self.P_C.currentWidget().undo_last)
			self.E_DICT("cut_act").triggered.connect(self.P_C.currentWidget().cut_selection)
			self.E_DICT("paste_act").triggered.connect(self.P_C.currentWidget().paste_selection)
			self.E_DICT("copy_act").triggered.connect(self.P_C.currentWidget().copy_selection)
			self.E_DICT("clone_act").triggered.connect(self.P_C.currentWidget().clone_doc)
			self.E_DICT("delete_line").triggered.connect(self.P_C.currentWidget().delete_line)
			self.E_DICT("line_up").triggered.connect(self.P_C.currentWidget().line_up)
			self.E_DICT("line_down").triggered.connect(self.P_C.currentWidget().line_down)
			self.E_DICT("clone_line").triggered.connect(self.P_C.currentWidget().clone_line)
			self.E_DICT("line_select").triggered.connect(self.P_C.currentWidget().current_line_select)
			self.E_DICT("indent_paste").triggered.connect(self.P_C.currentWidget().paste_and_indent)


class ViewMenuTriggers(ViewMenu):
	"""This class holds all view action connections. i.e. signals and slots 
		for the view menu
	"""
	def __init__(self, name=None, parent=None):
		super(ViewMenuTriggers, self).__init__(name, parent)
		self.V_GET = self.VIEW_ACTIONS.get
		self.P_C, self.P_C_T = parent, parent

	def update_connections(self):
		"""Updates all signal/slot connections"""
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		"""Here we reset all available connections, then call 
			update_triggers() to set to current tab page.
		"""
		for action in self.VIEW_ACTIONS.values():
			try:
				action.disconnect(self.P_C_T)
			except TypeError, AttributeError:
				print "error bypass set for VIEWS"


	def update_triggers(self):
		self.P_C_T = self.P_C.currentWidget()

		if self.P_C_T:
			self.V_GET("hide_status_act").triggered.connect(self.P_C.currentWidget().hide_statusbar)
			self.V_GET("python_syn").triggered.connect(self.P_C.currentWidget().python_syntax)
			self.V_GET("plain_syn").triggered.connect(self.P_C.currentWidget().plain_text)
			self.V_GET("html_syn").triggered.connect(self.P_C.currentWidget().html_syntax)
			self.V_GET("css_syn").triggered.connect(self.P_C.currentWidget().css_syntax)
			self.V_GET("zoom_in").triggered.connect(self.P_C.currentWidget().zoom_in)
			self.V_GET("zoom_out").triggered.connect(self.P_C.currentWidget().zoom_out)
			self.V_GET("word_wrap_act").triggered.connect(self.P_C.currentWidget().set_word_wrap)

			# not yet implemented
			# self.V_GET(plainL).triggered.connect(self.plain_layout)
			# self.V_GET(splitL).triggered.connect(self.split_screen_layout)
			# self.V_GET(gridL).triggered.connect(self.grid_layout)


class ToolMenuTriggers(ToolMenu):
	"""This class holds all tool action connections. i.e. signals and slots 
		for the tool menu.
		The functools; partial import is used here.
	"""
	def __init__(self, name=None, parent=None):
		super(ToolMenuTriggers, self).__init__(name, parent)
		self.T_GET = self.TOOL_ACTIONS.get
		self.P_C, self.P_C_T = parent, parent

	def update_connections(self):
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		"""Here we reset all available connections, then call 
			update_triggers() to set to current tab page.
		"""
		for action in self.TOOL_ACTIONS.values():
			try:
				action.disconnect(self.P_C_T)
			except TypeError, AttributeError:
				print "error bypass set for TOOLS"

	def update_triggers(self):
		
		self.P_C_T = self.P_C.currentWidget()
		
		if self.P_C_T:
			
			width = 10
			for action in self.TOOL_ACTIONS.values():
				action.triggered.connect(partial(self.P_C_T.set_tab_width, width))
				width += 10


class PrefMenuTriggers(PrefMenu):
	"""This class is responsible for all preference specific action triggers."""
	def __init__(self, name=None, parent=None):
		super(PrefMenuTriggers, self).__init__(name, parent)
		self.P_GET = self.PREF_ACTIONS.get
		self.P_C, self.P_C_T = parent, parent

	def update_connections(self):
		self.reset_all()
		self.update_triggers()

	def reset_all(self):
		"""Here we reset all available connections, then call 
			update_triggers() to set to current tab page.
		"""
		for action in self.PREF_ACTIONS.values():
			try:
				action.disconnect(self.P_C_T)
			except TypeError, AttributeError:
				print "error bypass for Preferences"

	def update_triggers(self):
		self.P_C_T = self.P_C.currentWidget()

		if self.P_C_T:
			self.P_GET("font_inc_act").triggered.connect(self.P_C.currentWidget().increase_font_size)
			self.P_GET("font_dec_act").triggered.connect(self.P_C.currentWidget().decrease_font_size)
			self.P_GET("serif_font_act").triggered.connect(self.P_C.currentWidget().set_serif)
			self.P_GET("monospace_font_act").triggered.connect(self.P_C.currentWidget().set_monospace)
			self.P_GET("sans_serif_font_act").triggered.connect(self.P_C.currentWidget().set_sansserif)


# MISC CLASSES================

# broken
class PyCodeDockWidget(QDockWidget):
	"""This class holds the main window dock widget for pop-ups, i.e. search & replace, find
		etc.
	"""
	
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
	""" Here the user specific settings are written and kept.

	"""

	def __init__(self, parent=None):
		super(PyCodeSettings, self).__init__(parent)
		self.settings = QSettings(QSettings.UserScope, 
						"AD Engineering", "PyCode Text Editor")
		self.P = parent
		self.P_C = self.P

	def write_settings(self):
		"""Writes the current user settings"""

		files = [self.P_C.tabText(i) for i in xrange(self.P_C.count())]
		
		self.settings.beginGroup("Main Window")
		
		# save opened tabs
		self.settings.beginWriteArray("files")
		for i in xrange(len(files)):
			self.settings.setArrayIndex(i)
			self.settings.setValue("filename", files[i] )
		self.settings.endArray()

		self.settings.setValue("Position", self.P.pos())
		self.settings.setValue("Size", self.P.size())
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
					f.close()
					new_page = PyCodePage(self.P_C)
					new_page.setPlainText(data)
					syntax = self.P_C.get_syntax_highlighter(tabname)
					syntax(new_page.document())
					self.P_C.addTab(new_page, tabname)
					
			except IOError:
				pass

		self.settings.endArray()

		self.P.move(self.settings.value("Position"))
		self.P.resize(self.settings.value("Size"))
		self.settings.endGroup()


class PyCodeShortcuts(QObject):
	"""Responsible for creating/holding all pycode Shortcuts
		Shortcut context needs to be set for instantiated objects.

	"""

	def __init__(self, parent=None):
		super(PyCodeShortcuts, self).__init__(parent)

		self._ALL_SHORTCUTS = {}
		self.create_shortcut("move_right", "Ctrl+pgup", parent, True)
		self.create_shortcut("move_right2", "Ctrl+Tab", parent, True)
		self.create_shortcut("move_left", "Ctrl+pgdn", parent, True)
		self.create_shortcut("move_left2", "Ctrl+Shift+Tab", parent, True)
		self.create_shortcut("close_focused_win", "Ctrl+Shift+W", parent)
		self.create_shortcut("close_dock", "Esc", parent)
		self.create_shortcut("cut_act", "Ctrl+X", parent)
		# self.create_shortcut("delete_line", "Ctrl+K", parent, True)
		# self.create_shortcut("clone_line", "Ctrl+Shift+D", parent, True)

	def create_shortcut(self, name=None, short=None, parent=None, auto=False):
		"""Creates Shortcut"""
		self._ALL_SHORTCUTS[str(name)] = QShortcut(short, parent)
		if auto:
			self._ALL_SHORTCUTS.get(name).setAutoRepeat(auto)


class PyCodeShortcutTriggers(PyCodeShortcuts):
	"""This class is Responsible for holding all shortcut signals and their 
		respective slots. P_C is a naming convention. Wherever this appears, 
		it refers to parent.child.

	"""

	def __init__(self, parent=None):
		super(PyCodeShortcutTriggers, self).__init__(parent)
		self.SHORT_GET = self._ALL_SHORTCUTS.get
		self.parent = parent
		self.P_C = self.parent

	def set_shortcut_slots(self):
		# should think about connecting to Qactions instead....
		self.SHORT_GET("move_right").activated.connect(self.P_C.tab_seek_right)
		self.SHORT_GET("move_right2").activated.connect(self.P_C.tab_seek_right)
		self.SHORT_GET("move_left").activated.connect(self.P_C.tab_seek_left)
		self.SHORT_GET("move_left2").activated.connect(self.P_C.tab_seek_left)
		self.SHORT_GET("close_focused_win").activated.connect
		self.SHORT_GET("close_dock").activated.connect


class PyCodeTop(QMainWindow):
	"""This will bring all classes together to make up the final application.
		All children after PyCodeTabInterface DEPEND upon the self.CHILD constant.
	"""
	def __init__(self, parent=None):
		super(PyCodeTop, self).__init__(parent)
		self.initUI()
		self.set_child_connections()
		self.SETTINGS.read_settings()
		if not self.CHILD.currentWidget():
			self.CHILD.new_file()
		self.set_stylesheet()

	def set_child_connections(self):
		"""Here most of the interdependent connections take place.
			If there's a bug, this is a good place to check...
		"""
		self.CHILD = self.findChild(PyCodeTabInterface)
		self.SETTINGS.P_C = self.CHILD
		self.SHORT.P_C = self.CHILD
		self.SHORT.set_shortcut_slots()
		self.CHILD.grab_sm_bars()
		self.CHILD.set_signal_slots()
		self.menuBar().set_CHILD_constant()

	def initUI(self):
		"""sets up intial interface"""
		self.setWindowTitle("PyCode Text Editor")
		status = PyCodeStatusBar(self)
		menu = PyCodeMenuBar(self)
		self.setMenuBar(menu)
		self.setStatusBar(status)
		main = PyCodeTabInterface(self)
		self.SETTINGS = PyCodeSettings(self)
		self.SHORT = PyCodeShortcutTriggers(self)
		self.setCentralWidget(main)
		

	def set_stylesheet(self):
		"""sets PyCode Stylesheet"""
		# need to make this customizable.i.e. load user settings.
		try:
			with open("../PyCodeThemes/PyCodeCrimson.qss") as f:
				stylesheet = f.read()
				self.setStyleSheet(stylesheet)
		except IOError:
			print "Cannot find Stylesheet; falling back to native style"

		
def main():
	pycodeapp = QApplication(sys.argv)
	pyeditor = PyCodeTop()
	pyeditor.show()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
