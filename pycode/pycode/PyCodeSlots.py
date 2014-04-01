# I will attempt to collate as many slots as possible here
# As of now, it is becoming more complex unnecessarily so.
from PySide.QtGui import *
from PySide.QtCore import *

class PyCodeSlots():
	def __init__(self, parent=None, widget=None):
		self.parent = parent

		def tab_width2(parent):
			return parent.setTabStopWidth(20)
		
		def new_window(parent):
			"""opens a completely new window."""

			new_window_instance = PyCodeEditor()
			self.new_window_instance.show()

		def python_syntax(self):
			"""sets selected syntax by user for the current document in focus"""
			
			current_index = parent.TAB_INTERFACE.currentIndex()
			current_filename = parent.TAB_INTERFACE.tabText(current_index)
			current_workarea = parent.TAB_INTERFACE.currentWidget()
			current_data = current_workarea.toPlainText()

			
			new_workarea = QPlainTextEdit(parent.TAB_INTERFACE)
			new_workarea.setPlainText(current_data)
			PythonSyntax(new_workarea.document())

			parent.TAB_INTERFACE.removeTab(current_index)
			parent.TAB_INTERFACE.insertTab(current_index, new_workarea, current_filename)
			parent.TAB_INTERFACE.widget(current_index).setFocus()

		def no_syntax(self):

			current_index = self.tabinterface.currentIndex()
			current_filename = self.tabinterface.tabText(current_index)
			current_data = self.tabinterface.currentWidget().toPlainText()
			
			new_workarea = QPlainTextEdit(self.tabinterface)
			new_workarea.setPlainText(current_data)

			self.tabinterface.removeTab(current_index)
			self.tabinterface.insertTab(current_index, new_workarea, current_filename)
			self.tabinterface.widget(current_index).setFocus()
# Custom Classes ===============================================

class NewWindow(PyCodeEditor):

	def __init__(self, parent=None):
		super(NewWindow, self).__init__(parent)
		self.initUI()
		self.setGeometry(100, 100, 800, 500)
		self.show()

