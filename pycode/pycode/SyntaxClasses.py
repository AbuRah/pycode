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
from PySide.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, 
			QFont)

from PySide.QtCore import QRegExp, Qt
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class PythonHighlight(QSyntaxHighlighter):
	def __init__(self, parent=None):
		super(PythonHighlight, self).__init__(parent)

	def highlightBlock(self):
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
		special_methodF = QTextCharFormat()
		between_parensF = QTextCharFormat()
		after_constructF = QTextCharFormat()
		
		# common statement words
		common_wordF.setForeground(QColor("#ffa812"))
		common_wordF.setFontWeight(QFont.Bold)
		common_words = ["for", "in", "while", "print", "from", 
				"import", "not", "None", "self", "return", "pass", 
				"True", "False"]

		for word in common_words:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern,common_wordF)
			self.highlighting_rules.append(rule)

		# special methods
		special_methodF.setForeground(QColor("#cc4e5c"))
		special_methodF.setFontWeight(QFont.Bold)
		special_methods = ["__init__", 
				"__getitem__","__new__", "__del__", "__repr__",
				 "__str__", "__lt__", "__le__", "__eq__", 
				 "__ne__", "__gt__", "__ge__", "__rcmp__", 
				 "__hash__", "__nonzero__", "__unicode__", 
				 "__getattr__", "__setattr__", "__delattr__",
				 "__getattribute__", "__get__", "__set__", 
				 "__delete__", "__slots__", "__metaclass__", 
				 "__instancecheck__", "__subclasscheck__", 
				 "__len__", "__setitem__", "__delitem__", 
				 "__iter__", "__reversed__", "__contains__",
				 "__getslice__", "__setslice__", 
				 "__delslice__", "__add__", "__sub__", 
				 "__mul__", "__floordiv__", "__mod__", 
				 "__divmod__", "__pow__", "__lshift__", "__rshift__", 
				 "__and__", "__xor__", "__or__", "__div__", "__truediv__", 
				 "__radd__", "__rsub__", "__rmul__", "__rdiv__",
				 "__rfloordiv__", "__rmod__", "__rdivmod__", "__rpow__", 
				 "__rlshift__", "__rrshift__", "__rand__", "__rxor__", 
				 "__ror__", "__iadd__", "__isub__", "__imul__", 
				 "__ifloordiv__", "__imod__", "__idivmod__", 
				 "__itruediv__", "__idiv__", "__ipow__", "__ilshift__", 
				 "__irshift__", "__iand__", "__ixor__", "__ior__", 
				 "__neg__", "__pos__", "__abs__", "__invert__", "__complex__", 
				 "__int__", "__long__", "__float__", "__oct__", "__hex__", 
				 "__index__", "__coerce__", "__enter__", "__exit__"]
		for method in special_methods:
			pattern = QRegExp("\\b" + method +"\\b")
			rule = HighlightingRule(pattern, special_methodF)
			self.highlighting_rules.append(rule)

		# constructors
		reserved_classesF.setForeground(QColor("#b06500"))
		# reserved_classesF.setFontWeight(QFont.Bold)
		predefined = ["class", "def"]

		for word in predefined:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern,reserved_classesF)
			self.highlighting_rules.append(rule)
		
		# func/class names
		after_constructF.setForeground(QColor("#cf1020"))
		after_constructF.setFontWeight(QFont.Bold)
		for word in predefined:
			pattern = QRegExp("([^"+ word +"\\s])+.*(")
			rule = HighlightingRule(pattern, after_constructF)
			self.highlighting_rules.append(rule)

		# any text between parens
		between_parensF.setFontItalic(True)
		for word in predefined:
			pattern = QRegExp("\(.*(?=\))\\b")
			rule = HighlightingRule(pattern, between_parensF)
			self.highlighting_rules.append(rule)

		# assignment operator
		# assignment_operatorF.setForeground(Qt.darkGreen)
		# assignment_operatorF.setFontWeight(QFont.Bold)
		# pattern = QRegExp("(<){1,2}-")
		# rule = HighlightingRule(pattern, assignment_operatorF)
		# self.highlighting_rules.append(rule)

		# digits
		numberF.setForeground(QColor("#dc143c"))
		pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
		pattern.setMinimal(True)
		rule = HighlightingRule(pattern, numberF)
		self.highlighting_rules.append(rule)

		# python builtin functions
		builtin_functionsF.setForeground(QColor("#ff4f00"))
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

		# double quotes string
		stringF.setBackground(QColor("#e25822"))
		pattern = QRegExp("\".*\"")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		# single quotes string
		stringF.setBackground(QColor("#e25822"))
		pattern = QRegExp("\'.*\'")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		# comments
		commentF = QTextCharFormat()
		commentF.setForeground(QColor("#986960"))
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
	"""Finds and Highlights all HTML related keywords"""
	
	def __init__(self, parent=None):
		super(HtmlSyntax, self).__init__(parent)

		self.highlighting_rules = []

		bracket_patternF = QTextCharFormat()
		between_bracket_patternF = QTextCharFormat()

		# highlights brackets
		bracket_patternF.setForeground(QColor("#f42c2c"))
		bracket_patternF.setFontWeight(QFont.Bold)
		pattern_list = ["<", ">", "</"]
		for regexp in pattern_list:
			pattern = QRegExp(regexp)
			rule = HighlightingRule(pattern, bracket_patternF)
			self.highlighting_rules.append(rule)

		# highlight words between brackets
		# currently broken
		# between_bracket_patternF.setForeground(QColor("#fe6f5e"))
		# pattern = QRegExp("(?<=<)[\w]*(?=>)")
		# rule = HighlightingRule(pattern, between_bracket_patternF)
		# self.highlighting_rules.append(rule)

	def highlightBlock(self, text):
		for rule in self.highlighting_rules:
			expression = QRegExp(rule.pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, rule.format)
				index = expression.indexIn(text, index+length)
		self.setCurrentBlockState(0)


class CSSSyntax(QSyntaxHighlighter):
	"""Highlights all CSS keywords
		CSS2 and CSS3 will inherit from this.
	"""
	def __init__(self, parent=None):
		super(CSSSyntax, self).__init__(parent)
		self.highlighting_rules = []

		# init all textformats here
		pseudo_classes_F = QTextCharFormat()
		pseudo_attributes_F = QTextCharFormat()
		commentsF = QTextCharFormat()
		keywordF = QTextCharFormat()
		id_keywordF = QTextCharFormat()
		valueF = QTextCharFormat()
		stringF = QTextCharFormat()
		url_keywordF = QTextCharFormat()

		# value color
		valueF.setForeground(QColor("#cc4e5c"))
		pattern = QRegExp(":.*(?=;)")
		rule = HighlightingRule(pattern, valueF)
		self.highlighting_rules.append(rule)

		# double quotes string
		stringF.setBackground(QColor("#e25822"))
		pattern = QRegExp("\".*\"")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		# single quotes string
		stringF.setBackground(QColor("#e25822"))
		pattern = QRegExp("\'.*\'")
		rule = HighlightingRule(pattern, stringF)
		self.highlighting_rules.append(rule)

		# id selector color
		id_keywordF.setForeground(QColor("#e25822"))
		pattern = QRegExp("[\.]\w+\\s+")
		rule = HighlightingRule(pattern, id_keywordF)
		self.highlighting_rules.append(rule)

		# comments multi/single
		commentsF.setBackground(QColor("#986960"))
		pattern = QRegExp("/\*.*\*/")
		rule = HighlightingRule(pattern, commentsF)
		self.highlighting_rules.append(rule)

		url_keywordF.setForeground(QColor("#e25822"))
		url_keywordF.setFontWeight(QFont.Bold)
		pattern = QRegExp("url(?=\()")
		rule = HighlightingRule(pattern, url_keywordF)
		self.highlighting_rules.append(rule)

		# pseudo classes
		pseudo_classes_F.setForeground(QColor("#dc143c"))
		pseudo_classes_F.setFontItalic(True)
		pattern_list = [":+\w*\(?\)?\\s", ":+\w*\(?\)?\\s", ":+\w*-*\w*\(?\)?\\s",
						":+\w*-*\w*-*\w*\(?\)?\\s", ":+\w*-*\w*-*\w*-*\w*\(?\)?\\s",
						":+\w*\(?\)?\.?", ":+\w*\(?\)?\.?", ":+\w*-*\w*\(?\)?\.?",
						":+\w*-*\w*-*\w*\(?\)?\.?", ":+\w*-*\w*-*\w*-*\w*\(?\)?\.?"]
		for pat in pattern_list:
			pattern = QRegExp(pat)
			rule = HighlightingRule(pattern, pseudo_classes_F)
			self.highlighting_rules.append(rule)

		# keywords
		keywordF.setForeground(QColor("#ffa812"))
		keywordF.setFontWeight(QFont.Bold)
		pattern_list = ["\\s\w+:", "\\s\w*-*\w+:", "\\s\w*-*\w*-*\w+:",
						"\\s\w*-*\w*-*\w*-*\w*-*\w+:"]
		for word in pattern_list:
			pattern = QRegExp(word)
			rule = HighlightingRule(pattern, keywordF)
			self.highlighting_rules.append(rule)

	def highlightBlock(self, text):
		for rule in self.highlighting_rules:
			expression = QRegExp(rule.pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, rule.format)
				index = expression.indexIn(text, index+length)
		self.setCurrentBlockState(0)


class PlainText(QSyntaxHighlighter):
	"""Sets Syntax to PlainText"""
	def __init__(self, parent=None):
		super(PlainText, self).__init__(parent)

	def highlightBlock(self, text):
		pass


#common keywords:
# #ffa812: Dark Tangerine;

# special methods/functions:
# #cc4e5c: DarkTerraCotta;

# common functions:
# #ffbcd9: cotton candy;

# single/multi comments :
# #986960: Dark Chestnut;

# numbers:=========
# #dc143c Crimson;

# assignment operators

# text strings:
# #e25822 Flame;

# class prefixes:
# #e48400 Ginger

class HighlightingRule():

  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format