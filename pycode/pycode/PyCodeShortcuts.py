#Default Shortcuts

from PySide.QtGui import QShortcut, QKeySequence
from PySide.QtCore import Qt

class PyCodeShortcuts():

	def __init__(self, parent=None):

		
		self.move_right_between_tabs = QShortcut("Ctrl+Tab", parent)
		self.move_right_between_tabs2 = QShortcut("Ctrl+pgup", parent)

		self.move_left_between_tabs = QShortcut("Ctrl+Shift+Tab", parent)
		# the following shortcut isn't working
		self.move_left_between_tabs2 = QShortcut("Ctrl+pgdn", parent)

		self.close_active_window = QShortcut("Ctrl+Shift+W", parent)
		self.close_dock = QShortcut(QKeySequence(Qt.Key_Escape), parent)

		# i should probly set this in the main module
		self.move_left_between_tabs.setAutoRepeat(True)
		self.move_right_between_tabs.setAutoRepeat(True)


		


