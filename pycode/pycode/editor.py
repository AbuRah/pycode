import sys, os, time
from exceptions import IOError, AttributeError

from PySide.QtCore import *
from PySide.QtGui import *

from SyntaxClasses import *
from PyCodeActions import *
from PyCodeShortcuts import *



class PyCodeEditor(QMainWindow):
	
	_CLOSED_TAB_LIST = []

	def __init__(self, parent=None):
		super(PyCodeEditor, self).__init__(parent)
		
		self.initUI()
		self.settings = None
		self.setWindowTitle("PyCode Text Editor")


	
	def initUI(self):

		self.TAB_INTERFACE = QTabWidget()
		self.TAB_INTERFACE.setDocumentMode(True)
		self.TAB_INTERFACE.setMovable(True)
		self.TAB_INTERFACE.setTabsClosable(True)
		self.TAB_INTERFACE.addTab(QPlainTextEdit(self.TAB_INTERFACE), "Untitled")
		self.TAB_INTERFACE.setElideMode(Qt.ElideRight)
		self.TAB_INTERFACE.setFocusPolicy(Qt.NoFocus)
		self.TAB_INTERFACE.currentWidget().setFocus()


		CURRENT_WORKAREA = self.TAB_INTERFACE.currentWidget()


		ALL_ACTIONS = PyCodeActions(self)
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
		ALL_ACTIONS.tabW2.triggered.connect(self.tab_width2)
		ALL_ACTIONS.tabW4.triggered.connect(self.tab_width4)
		ALL_ACTIONS.tabW6.triggered.connect(self.tab_width6)
		ALL_ACTIONS.tabW8.triggered.connect(self.tab_width8)
		ALL_ACTIONS.reopenT.triggered.connect(self.reopen_last_tab)
		ALL_ACTIONS.closeF.triggered.connect(self.close_tab)
		ALL_ACTIONS.closeW.triggered.connect(self.close_window)
		ALL_ACTIONS.findAct.triggered.connect(self.find_text)

		ALL_ACTIONS.pythonSyn.toggled.connect(self.python_syntax)
		ALL_ACTIONS.plainSyn.toggled.connect(self.no_syntax)



		self.setCentralWidget(self.TAB_INTERFACE)


		

		



# MENUBAR Specific ==================================================
		# CREATE MENUS HERE
		mainbar = self.menuBar()
		filemenu = mainbar.addMenu("&File")
		editmenu = mainbar.addMenu("Edit")
		viewmenu = mainbar.addMenu("View")
		toolmenu = mainbar.addMenu("Tools")
		preferences = mainbar.addMenu("Preferences")
		
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
		
		syntaxmenu.addAction(ALL_ACTIONS.pythonSyn)
		syntaxmenu.addAction(ALL_ACTIONS.plainSyn)

		# TOOL MENU
		tabwidth = toolmenu.addMenu("Tab Width")
		
		tabwidth.addAction(ALL_ACTIONS.tabW2)
		tabwidth.addAction(ALL_ACTIONS.tabW4)
		tabwidth.addAction(ALL_ACTIONS.tabW6)
		tabwidth.addAction(ALL_ACTIONS.tabW8)
		




		

# STATUSBAR =====================================================
		status = self.statusBar()
		status.showMessage("Ready", 4000)
		# status.addPermamentWidget() <--- add syntax indicator here using

# DockWidget Area ==============================================================

		
		self.main_dock_widget = QDockWidget(self)
		self.main_dock_widget.setAllowedAreas(Qt.BottomDockWidgetArea)
		self.main_dock_widget.setFloating(False)
		self.main_dock_widget.setObjectName('Main Dock')
		self.addDockWidget(Qt.BottomDockWidgetArea, self.main_dock_widget)
		self.main_dock_widget.hide()

# LAYOUT AND FINAL INITIAL SETUP======================================

		# self.mainlayout = QHBoxLayout()
		# self.mainlayout.addWidget(self.TAB_INTERFACE)
		# self.setLayout(self.mainlayout)

# SHORTCUT ==================================================================
		ALL_SHORTCUTS = PyCodeShortcuts(self.TAB_INTERFACE)

		ALL_SHORTCUTS.move_right_between_tabs.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.move_left_between_tabs.activated.connect(self.tab_seek_left)
		ALL_SHORTCUTS.move_right_between_tabs2.activated.connect(self.tab_seek_right)
		ALL_SHORTCUTS.close_active_window.activated.connect(self.close_window)
		ALL_SHORTCUTS.close_dock.activated.connect(self.main_dock_widget.hide)
		

# SLOTS
# =============================================================================	
# FILEMENU SLOTS===============================================================
	def open_file_dialog(self):
		"""opens file in new tab"""

		filename,_ = QFileDialog.getOpenFileName(self,
			"Open File", os.getcwd())

		if filename != '':

			with open(filename, "r") as f:
				
				data = f.read()
				new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
				new_workarea.setPlainText(data)

				nameHolder = QFileInfo(filename)
				nameOfFile = nameHolder.fileName()

				self.TAB_INTERFACE.addTab(new_workarea, nameOfFile)
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

		new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
		PlainText(new_workarea.document())
		new_workarea.setFocus()
		return self.TAB_INTERFACE.addTab(new_workarea, "Untitled")
	
	def new_window(self):
		"""opens a completely new window."""
		self.new_window_instance = PyCodeEditor()
		self.new_window_instance.show()


	def close_window(self):
		"""Close active window"""
		return self.close()
	
	def reopen_last_tab(self):
		"""Opens the last tab closed"""

		if len(self._CLOSED_TAB_LIST) > 0:

			new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
			
			last_file = self._CLOSED_TAB_LIST.pop()
			try:

				with open(last_file, "r") as f:
					data = f.read()
					new_workarea.setPlainText(data)
		

					self.TAB_INTERFACE.addTab(new_workarea, last_file)
		
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
				focusedPage = self.TAB_INTERFACE.currentWidget()
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
		# self.close()

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
		currentPage = self.TAB_INTERFACE.currentWidget()
	
		currentPage.cut()

	def find_text(self):
		"""Find the indicated text within the current tab page"""
		###!!! INCOMPLETE
		### need to add auto-complete, selection and find & replace
		self.main_dock_widget.show()

		user_input = QLineEdit(self)
		self.main_dock_widget.setWidget(user_input)
		user_input.setFocus()

		current_tab_cursor = self.TAB_INTERFACE.currentWidget().textCursor()
		current_tab_doc = self.TAB_INTERFACE.currentWidget().doc
		current_tab_doc.findBlock()
			
	def paste_selection(self):
		"""paste text from clipboard to tab page"""
		currentTab = self.TAB_INTERFACE.currentWidget()
		currentTab.paste()


	def undo_last(self):
		"""Steps back in operation history"""
		currentTab = self.TAB_INTERFACE.currentWidget()
		currentTab.undo()

	def redo_last(self):
		"""Steps forward in operation history"""
		currentTab = self.TAB_INTERFACE.currentWidget()
		currentTab.redo()

# VIEW MENU SLOTS ==============================================================
	# Need to be able to condense the following four functions into one.
	def tab_width2(self):
		return self.TAB_INTERFACE.currentWidget().setTabStopWidth(20)
	
	def tab_width4(self):
		return self.TAB_INTERFACE.currentWidget().setTabStopWidth(40)
	
	def tab_width6(self):
		return self.TAB_INTERFACE.currentWidget().setTabStopWidth(60)
	
	def tab_width8(self):
		return self.TAB_INTERFACE.currentWidget().setTabStopWidth(80)

	def python_syntax(self):
		"""sets selected syntax by user for the current document in focus"""
		
		current_index = self.TAB_INTERFACE.currentIndex()
		current_filename = self.TAB_INTERFACE.tabText(current_index)
		current_workarea = self.TAB_INTERFACE.currentWidget()
		current_data = current_workarea.toPlainText()

		
		new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
		new_workarea.setPlainText(current_data)
		PythonSyntax(new_workarea.document())

		self.TAB_INTERFACE.removeTab(current_index)
		self.TAB_INTERFACE.insertTab(current_index, new_workarea, current_filename)
		self.TAB_INTERFACE.widget(current_index).setFocus()

	def no_syntax(self):

		current_index = self.TAB_INTERFACE.currentIndex()
		current_filename = self.TAB_INTERFACE.tabText(current_index)
		current_data = self.TAB_INTERFACE.currentWidget().toPlainText()
		
		new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
		new_workarea.setPlainText(current_data)

		self.TAB_INTERFACE.removeTab(current_index)
		self.TAB_INTERFACE.insertTab(current_index, new_workarea, current_filename)
		self.TAB_INTERFACE.widget(current_index).setFocus()

#INTERNAL SLOTS=================================================================
	def tab_seek_right(self):
		"""Moves focus one tab to the right, back to start if at the end"""

		total_open_tabs = self.TAB_INTERFACE.count()

		focused_tab_index = self.TAB_INTERFACE.currentIndex()

		if focused_tab_index == total_open_tabs - 1:
			focused_tab_index = 0

		else:
			focused_tab_index += 1

		widget_at_index = self.TAB_INTERFACE.widget(focused_tab_index)
		return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)

	def tab_seek_left(self):
		"""Moves focus one tab to the left, moves to end if at the start"""

		total_open_tabs = self.TAB_INTERFACE.count()

		focused_tab_index = self.TAB_INTERFACE.currentIndex()

		if focused_tab_index == 0:
			focused_tab_index = total_open_tabs - 1

		else:
			focused_tab_index -= 1


		widget_at_index = self.TAB_INTERFACE.widget(focused_tab_index)
		return self.TAB_INTERFACE.setCurrentWidget(widget_at_index)

	def modified_since_save(self):
		"""Causes tab text to change if modified since last save"""
		current_index = self.TAB_INTERFACE.currentIndex()
		return self.TAB_INTERFACE.tabBar().setTabTextColor(current_index,
												 QColor("#fff5ee"))

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
		self.settings.setValue("Window State", self.saveState())
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
					new_workarea = QPlainTextEdit(self.TAB_INTERFACE)
					new_workarea.setPlainText(data)
					self.TAB_INTERFACE.addTab(new_workarea, tabname)
					f.close()
			except IOError:
				pass

		self.settings.endArray()
		self.move(self.settings.value("Position"))
		self.resize(self.settings.value("Size"))
		self.restoreState(self.settings.value("Window State"))
		self.settings.endGroup()



#Classes =====================================================================

class NewWindow(PyCodeEditor):

	def __init__(self, parent=None):
		super(NewWindow, self).__init__(parent)
		self.initUI()
		self.setGeometry(100, 100, 800, 500)
		self.show()

#MAIN =========================================================================

def main():
	pycodeapp = QApplication(sys.argv)

	try:
		with open("PyCodeThemes/PyCodeCrimson.qss") as f:
			stylesheet = f.read()
			pycodeapp.setStyleSheet(stylesheet)
	
	except IOError:
		print "Stylesheet does not exist; falling back to native style"

	editor = PyCodeEditor()
	editor.read_settings()
	editor.show()
	sys.exit(pycodeapp.exec_())


if __name__ == "__main__":
	main()
