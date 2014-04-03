""" All of the syntax classes will be placed here"""
# I will clean this up later

from PySide.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, 
			QFont)

from PySide.QtCore import QRegExp, Qt
class PlainText(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(PlainText, self).__init__(parent)

	def highlightBlock(self, text):
		pass


class PythonSyntax(QSyntaxHighlighter):
	""" Highlights regular python syntax"""

	def __init__(self, parent=None):
		super(PythonSyntax, self).__init__(parent)
		
		self.highlighting_rules = []

		common_wordF = QTextCharFormat()
		builtin_functionsF = QTextCharFormat()
		reserved_classesF = QTextCharFormat()
		assignment_operatorF = QTextCharFormat()
		numberF = QTextCharFormat()
		stringF = QTextCharFormat()
		

		common_wordF.setForeground(QColor("#ffa812"))
		common_wordF.setFontWeight(QFont.Bold)
		common_words = ["for", "in", "while", "print", "from", "import"]

		for word in common_words:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern,common_wordF)
			self.highlighting_rules.append(rule)

		reserved_classesF.setForeground(QColor("#5d8aa8"))
		reserved_classesF.setFontWeight(QFont.Bold)
		predefined = ["class", "def", "list", "dict", "tuple"]

		for word in predefined:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern,reserved_classesF)
			self.highlighting_rules.append(rule)
		
		# assignment operator
		# assignment_operatorF.setForeground(Qt.darkGreen)
		# assignment_operatorF.setFontWeight(QFont.Bold)
		# pattern = QRegExp("(<){1,2}-")
		# rule = HighlightingRule(pattern, assignment_operatorF)
		# self.highlighting_rules.append(rule)


		numberF.setForeground(Qt.magenta)
		pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
		pattern.setMinimal(True)
		rule = HighlightingRule(pattern, numberF)
		self.highlighting_rules.append(rule)

		# This will hold all well builtin function common_wordFs
		builtin_functionsF.setForeground(QColor("#de5d83"))
		python_builtin_functionsF = ["abs",	"divmod", "input", "open",
							"staticmethod",	"all", "enumerate", "int", "ord", 
							"str", "any", "eval", "isinstance", "pow", "sum", 
							"basestring", "execfile", "issubclass", "print", 
							"super", "bin", "file", "iter", "property", 
							"tuple", "bool", "filter", "len", "range", "type", 
							"bytearray", "float", "list", "raw_input", "unichr",
							"callable", "format", "locals", "reduce", "unicode",
							"chr", "frozenset", "long", "reload", "vars",
							"classmethod", "getattr", "map", "repr", "xrange",
							"cmp", "globals", "max", "reversed", "zip",
							"compile", "hasattr", "memoryview", "round", 
							"__import__", "complex", "hash", "min", "set", 
							"apply", "delattr", "help", "next", "setattr", 
							"buffer", "dict", "hex", "object", "slice", "coerce",
							"dir", "id", "oct", "sorted", "intern"]
		
		for word in python_builtin_functionsF:
			pattern = QRegExp("\\b"+word+"\\b")
			rule = HighlightingRule(pattern, builtin_functionsF)
			self.highlighting_rules.append(rule)


		stringF.setBackground(QColor("#e3dac9"))
		pattern = QRegExp("\".*\"")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		stringF.setBackground(QColor("#e3dac9"))
		pattern = QRegExp("\'.*\'")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		commentF = QTextCharFormat()
		commentF.setForeground(QColor("#f0f8ff"))
		pattern = QRegExp("#[^\n]*")
		rule = HighlightingRule(pattern, commentF)
		self.highlighting_rules.append(rule)



	def highlightBlock( self, text ):
		for rule in self.highlighting_rules:
			expression = QRegExp( rule.pattern )
			index = expression.indexIn( text )
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat( index, length, rule.format )
				index = expression.indexIn( text, index + length )
		self.setCurrentBlockState( 0 )

class HtmlSyntax(QSyntaxHighlighter):
	pass


class HighlightingRule():

  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format