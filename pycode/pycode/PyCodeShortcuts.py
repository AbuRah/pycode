#Default Shortcuts

from PySide.QtGui import QShortcut, QKeySequence
from PySide.QtCore import Qt

class PyCodeShortcuts():

	def __init__(self, parent=None):

		self._ALL_SHORTCUTS = {}
		# self.create_shortcut("move_right", "Ctrl+Tab", parent, True)
		# self.create_shortcut("move_right", "Ctrl+pgup", parent, True)
		# self.create_shortcut("move_left", "Ctrl+Shift+Tab", parent, True)
		# self.create_shortcut("move_left", "Ctrl+pgdn", parent, True)
		# self.create_shortcut("close_focused_win", "Ctrl+Shift+W", parent)
		# self.create_shortcut("close_dock", "Esc", parent)


		
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

	def create_shortcut(self, name=None, short=None, parent=None, setauto=False):
		"""Creates Shortcut"""
		self._ALL_SHORTCUTS[name] = QShortcut(short, parent)
		if setauto:
			self._ALL_SHORTCUTS.get(name).setAutoRepeat(setauto)


		


