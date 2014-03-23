import sys, os
from PySide import QtGui, QtCore

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class FileView(QtGui.QWidget):

	def __init__(self):

		super(FileView, self).__init__()

		self.initUI()

	def initUI(self):
		
		filemodel = QtGui.QFileSystemModel()
		filemodel.setRootPath(QtCore.QDir.currentPath())



		tree = QtGui.QTreeView()
		tree.setModel(filemodel)



		self.setGeometry(150, 150, 300, 300)
		self.setWindowTitle("testing")
		self.show()

	# here i'm experimenting with creating my own file dialog
	
	dialog = QtGui.QFileDialog(self)
	dialog.setFileMode(Qtgui.QFileDialog.AnyFile)
	dialog.setViewMode(QtGui.QFileDialog.List)