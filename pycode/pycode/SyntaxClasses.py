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

from PySide.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, QFont)
from PySide.QtCore import QRegExp, Qt


class PyCodeSyntaxHighlighter(QSyntaxHighlighter):
	"""Base class for all PyCode syntax highlighters
		I may implement a method that parses pycode specific
		styles and automatically sets the formatting rules.
		As i add more lexers, i will also add more formatting options.
		If there is no need for specifying particular sub-types (e.g. float, int)
		use the generic formatting constant defined i.e. number, instead of
		number_integer.
	"""

	# need to be able to extract theme colors from css stylesheet and
	# set theme_dict values to corresponding key.
	def __init__(self, parent=None):
		super(PyCodeSyntaxHighlighter, self).__init__(parent)
		self.highlighting_rules = []

		self.commentF = QTextCharFormat()
		self.comment_singleF = QTextCharFormat()
		self.comment_multiF = QTextCharFormat()
		self.comment_specialF = QTextCharFormat()
		self.comment_otherF = QTextCharFormat()
		self.keywordF = QTextCharFormat()
		self.keyword_pseudoF = QTextCharFormat()
		self.keyword_builtinF = QTextCharFormat()
		self.keyword_constantF = QTextCharFormat()
		self.keyword_functionF = QTextCharFormat()
		self.keyword_classF = QTextCharFormat()
		self.keyword_namespaceF = QTextCharFormat()
		self.keyword_reservedF = QTextCharFormat()
		self.keyword_typeF = QTextCharFormat()
		self.nameF = QTextCharFormat()
		self.name_attribute = QTextCharFormat()
		self.name_tagF = QTextCharFormat()
		self.name_builtinF = QTextCharFormat()
		self.name_decoratorF = QTextCharFormat()
		self.name_classF = QTextCharFormat()
		self.name_entityF = QTextCharFormat()
		self.name_exceptionF = QTextCharFormat()
		self.name_functionF = QTextCharFormat()
		self.name_namespaceF = QTextCharFormat()
		self.name_variableF = QTextCharFormat()
		self.name_otherF = QTextCharFormat()
		self.literalF = QTextCharFormat()
		self.stringF = QTextCharFormat()
		self.string_singleF = QTextCharFormat()
		self.string_doubleF = QTextCharFormat()
		self.string_docF = QTextCharFormat()
		self.string_escapeF = QTextCharFormat()
		self.string_regexF = QTextCharFormat()
		self.string_symbolF = QTextCharFormat()
		self.string_otherF = QTextCharFormat()
		self.numberF = QTextCharFormat()
		self.number_integerF = QTextCharFormat()
		self.number_int_longF = QTextCharFormat()
		self.number_floatF = QTextCharFormat()
		self.number_hexF = QTextCharFormat()
		self.number_octF = QTextCharFormat()
		self.number_otherF = QTextCharFormat()
		self.operatorF = QTextCharFormat()
		self.operator_wordF = QTextCharFormat()
		self.operator_otherF = QTextCharFormat()
		self.punctuationF = QTextCharFormat()

		self.THEME_DICT = {"comment": QColor("#b94e48"),
						"comment_short": QColor("#b94e48"),
						"comment_long": QColor("#b94e48"), 
						"comment_special": QColor("#b94e48"),
						"comment_other": QColor("#b94e48"),
						"keyword": QColor("#fdee00"), 
						"keyword_pseudo": QColor("#fe6f5e"),
						"keyword_builtin": QColor("#ffa812"),
						"keyword_constant": QColor("#ffa812"),
						"keyword_function": QColor("#e48400"),
						"keyword_class": QColor("#e48400"),
						"keyword_namespace": QColor("#e48400"),
						"keyword_reserved": QColor("#e48400"), 
						"keyword_type": QColor("#e48400"),
						"name": QColor("#cc5500"), 
						"name_attribute": QColor("#933d41"),
						"name_tag": QColor("#cd5700"),
						"name_builtin": QColor("#e08d3c"),
						"name_decorator": QColor("#e08d3c"),
						"name_class": QColor("#cc5500"), 
						"name_entity": QColor("#933d41"),
						"name_exception": QColor("#933d41"),
						"name_function": QColor("#cc5500"),
						"name_namespace": QColor("#933d41"), 
						"name_variable": QColor("#cc5500"), 
						"name_other": QColor("#cc5500"), 
						"literal": QColor("#e25822"), 
						"string": QColor("#e25822"), 
						"string_single": QColor("#e25822"),
						"string_double": QColor("#e25822"),
						"string_doc": QColor("#e30b5d"),
						"string_escape": QColor("#ab4e52"), 
						"string_regex": QColor("#de3163"),
						"string_symbol": QColor("#e25822"), 
						"number": QColor("#dc143c"), 
						"number_integer": QColor("#dc143c"), 
						"number_float": QColor("#dc143c"), 
						"number_hex": QColor("#de3163"), 
						"number_oct": QColor("#b31b1b"),
						"number_other": QColor("#dc143c"),
						"operator": QColor("#d2691e"), 
						"operator_word": QColor("#cf1020"), 
						"operator_other": QColor("#cf1020"),
						"punctuation": QColor("#a40000"),
						}

		self.TM_GET = self.THEME_DICT.get


class PythonSyntax(PyCodeSyntaxHighlighter):
	""" Highlights regular python syntax"""

	def __init__(self, parent=None):
		super(PythonSyntax, self).__init__(parent)
		
		# common statement words
		self.keywordF.setForeground(self.TM_GET("keyword"))
		self.keywordF.setFontWeight(QFont.Bold)
		
		keyword_list = ["for", "in", "while", "print", "from", 
				"import", "not", "None", "self", "return", "pass", 
				"True", "False", "if", "elif", "else"]

		for word in keyword_list:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern, self.keywordF)
			self.highlighting_rules.append(rule)

		# special methods
		self.keyword_reservedF.setForeground(self.TM_GET("keyword_reserved"))
		self.keyword_reservedF.setFontWeight(QFont.Bold)
		keywords_reserved = ["__init__", "__name__",
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
		for method in keywords_reserved:
			pattern = QRegExp("\\b" + method +"\\b")
			rule = HighlightingRule(pattern, self.keyword_reservedF)
			self.highlighting_rules.append(rule)

		# function keywords
		self.keyword_functionF.setForeground(self.TM_GET("keyword_function"))
		keywords_functions = ["class", "def"]

		for word in keywords_functions:
			pattern = QRegExp("\\b"+ word +"\\b")
			rule = HighlightingRule(pattern, self.keyword_functionF)
			self.highlighting_rules.append(rule)
		
		# func/class names
		self.name_functionF.setForeground(self.TM_GET("name_function"))
		self.name_functionF.setFontWeight(QFont.Bold)
		for word in keywords_functions:
			pattern = QRegExp("([^"+ word +"\\s])+.*(")
			rule = HighlightingRule(pattern, self.name_functionF)
			self.highlighting_rules.append(rule)

		# text between parens after name
		self.name_otherF.setFontItalic(True)
		for word in keywords_functions:
			pattern = QRegExp("\(.*(?=\))\\b")
			rule = HighlightingRule(pattern, self.name_otherF)
			self.highlighting_rules.append(rule)

		# number
		self.numberF.setForeground(self.TM_GET("number"))
		pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
		pattern.setMinimal(True)
		rule = HighlightingRule(pattern, self.numberF)
		self.highlighting_rules.append(rule)

		# builtin functions
		self.keyword_builtinF.setForeground(self.TM_GET("keyword_builtin"))
		keywords_builtin_list = ["abs",	"divmod", "input", "open",
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
		
		for word in keywords_builtin_list:
			pattern = QRegExp("\\b"+word+"\\b")
			rule = HighlightingRule(pattern, self.keyword_builtinF)
			self.highlighting_rules.append(rule)

		# double quotes string
		self.string_doubleF.setBackground(self.TM_GET("string_double"))
		pattern = QRegExp("\".*\"")
		rule = HighlightingRule(pattern, self.string_doubleF)
		self.highlighting_rules.append(rule)

		# single quotes string
		self.string_singleF.setBackground(self.TM_GET("string_single"))
		pattern = QRegExp("\'.*\'")
		rule = HighlightingRule(pattern, self.string_singleF)
		self.highlighting_rules.append(rule)

		# comments
		self.commentF.setForeground(self.TM_GET("comment"))
		pattern = QRegExp("#[^\n]*")
		rule = HighlightingRule(pattern, self.commentF)
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


class HtmlSyntax(PyCodeSyntaxHighlighter):
	"""Finds and Highlights all HTML related keywords"""
	
	def __init__(self, parent=None):
		super(HtmlSyntax, self).__init__(parent)


		# brackets
		self.keywordF.setForeground(self.TM_GET("keyword"))
		self.keywordF.setFontWeight(QFont.Bold)
		pattern_list = ["<", ">", "</"]
		for regexp in pattern_list:
			pattern = QRegExp(regexp)
			rule = HighlightingRule(pattern, self.keywordF)
			self.highlighting_rules.append(rule)

		# name between brackets
		# name_tagF.setForeground("name_tag")
		# pattern = QRegExp("(?<=<)[\w]*(?=>)")
		# rule = HighlightingRule(pattern, name_tagF)
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


class CSSSyntax(PyCodeSyntaxHighlighter):
	"""Highlights all CSS keywords
		CSS2 and CSS3 will inherit from this.
	"""
	def __init__(self, parent=None):
		super(CSSSyntax, self).__init__(parent)

		# value color
		self.name_variableF.setForeground(self.TM_GET("name_variable"))
		pattern = QRegExp(":.*(?=;)")
		rule = HighlightingRule(pattern, self.name_variableF)
		self.highlighting_rules.append(rule)

		# double quotes string
		self.string_doubleF.setBackground(self.TM_GET("string_double"))
		pattern = QRegExp("\".*\"")
		rule = HighlightingRule(pattern, self.string_doubleF)
		self.highlighting_rules.append(rule)

		# single quotes string
		self.string_singleF.setBackground(self.TM_GET("string_single"))
		pattern = QRegExp("\'.*\'")
		rule = HighlightingRule(pattern, self.string_singleF)
		self.highlighting_rules.append(rule)

		# id selector color
		self.keyword_reservedF.setForeground(self.TM_GET("keyword_reserved"))
		pattern = QRegExp("[\.]\w+\\s+")
		rule = HighlightingRule(pattern, self.keyword_reservedF)
		self.highlighting_rules.append(rule)

		# comments multi/single
		self.comment_multiF.setBackground(self.TM_GET("comment"))
		pattern = QRegExp("/\*.*\*/")
		rule = HighlightingRule(pattern, self.comment_multiF)
		self.highlighting_rules.append(rule)

		# pseudo classes
		self.keyword_pseudoF.setForeground(self.TM_GET("keyword_pseudo"))
		self.keyword_pseudoF.setFontItalic(True)
		keyword_pseudo_list = [":+\w*\(?\)?\\s", ":+\w*\(?\)?\\s", ":+\w*-*\w*\(?\)?\\s",
						":+\w*-*\w*-*\w*\(?\)?\\s", ":+\w*-*\w*-*\w*-*\w*\(?\)?\\s",
						":+\w*\(?\)?\.?", ":+\w*\(?\)?\.?", ":+\w*-*\w*\(?\)?\.?",
						":+\w*-*\w*-*\w*\(?\)?\.?", ":+\w*-*\w*-*\w*-*\w*\(?\)?\.?"]
		for key in keyword_pseudo_list:
			pattern = QRegExp(key)
			rule = HighlightingRule(pattern, self.keyword_pseudoF)
			self.highlighting_rules.append(rule)

		# keywords
		self.keywordF.setForeground(self.TM_GET("keyword"))
		self.keywordF.setFontWeight(QFont.Bold)
		# need to name all CSS keywords
		keyword_list = ["\\s+\w+:", "\\s+\w*-*\w+:", "\\s+\w*-*\w*-*\w+:",
						"\\s+\w*-*\w*-*\w*-*\w*-*\w+:"]
		for word in keyword_list:
			pattern = QRegExp(word)
			rule = HighlightingRule(pattern, self.keywordF)
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


class PlainText(PyCodeSyntaxHighlighter):
	"""Sets Syntax to PlainText"""
	def __init__(self, parent=None):
		super(PlainText, self).__init__(parent)

	def highlightBlock(self, text):
		pass


class HighlightingRule(object):

  def __init__( self, pattern, format ):
    self.pattern = pattern
    self.format = format