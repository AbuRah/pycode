#-*-coding:utf-8-*-
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
    See COPYING for complete licensing information...

"""

from PySide.QtGui import (QSyntaxHighlighter, QTextCharFormat, QColor, QFont)
from PySide.QtCore import QRegExp, Qt, QObject


class PyCodeSyntaxHighlighter(QSyntaxHighlighter):
    """Base class for all PyCode syntax highlighters
        I may implement a method that parses pycode specific
        styles and automatically sets the formatting rules.
        As i add more lexers, i will also add more formatting options.
        If there is no desire for specifying particular sub-type styling (e.g. float, int)
        use the same color set for numbers for all number sub-types
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
        self.number_longF = QTextCharFormat()
        self.number_floatF = QTextCharFormat()
        self.number_hexF = QTextCharFormat()
        self.number_octF = QTextCharFormat()
        self.number_otherF = QTextCharFormat()
        self.operatorF = QTextCharFormat()
        self.operator_wordF = QTextCharFormat()
        self.operator_otherF = QTextCharFormat()
        self.punctuationF = QTextCharFormat()

        # monokai
        self.THEME_DICT = {"comment": QColor("#75715E"),
                    "comment_short": QColor("#75715E"),
                    "comment_long": QColor("#75715E"), 
                    "comment_special": QColor("#75715E"),
                    "comment_other": QColor("#75715E"),
                    "keyword": QColor("#EFB571"), 
                    "keyword_pseudo": QColor("#fe6f5e"),
                    "keyword_builtin": QColor("#A6E22E"),
                    "keyword_constant": QColor("#A6E22E"),
                    "keyword_function": QColor("#BED6FF"),
                    "keyword_class": QColor("#FFFFFF"),
                    "keyword_namespace": QColor("#e48400"),
                    "keyword_reserved": QColor("#e48400"), 
                    "keyword_type": QColor("#e48400"),
                    "name": QColor("#F92672"), 
                    "name_attribute": QColor("#933d41"),
                    "name_tag": QColor("#cd5700"),
                    "name_builtin": QColor("#F92672"),
                    "name_decorator": QColor("#F92672"),
                    "name_class": QColor("#F92672"), 
                    "name_entity": QColor("#933d41"),
                    "name_exception": QColor("#933d41"),
                    "name_function": QColor("#F92672"),
                    "name_namespace": QColor("#933d41"), 
                    "name_variable": QColor("#F92672"), 
                    "name_other": QColor("#cc5500"), 
                    "literal": QColor("#A6E22E"), 
                    "string": QColor("#A6E22E"), 
                    "string_single": QColor("#A6E22E"),
                    "string_double": QColor("#A6E22E"),
                    "string_doc": QColor("#e30b5d"),
                    "string_escape": QColor("#ab4e52"), 
                    "string_regex": QColor("#de3163"),
                    "string_symbol": QColor("#A6E22E"), 
                    "number": QColor("#F92672"), 
                    "number_long": QColor("#F92672"), 
                    "number_integer": QColor("#F92672"), 
                    "number_float": QColor("#F92672"), 
                    "number_hex": QColor("#de3163"), 
                    "number_oct": QColor("#b31b1b"),
                    "number_other": QColor("#F92672"),
                    "operator": QColor("#d2691e"), 
                    "operator_word": QColor("#cf1020"), 
                    "operator_other": QColor("#cf1020"),
                    "punctuation": QColor("#a40000"),
                    }

        self.TM_GET = self.THEME_DICT.get

    def add_list_of_rules(self, lst=None, format=None, prefix="", suffix=""):
        """adds predefined lists to highlighting rules
            The prefix denotes any regexp syntax that is to come BEFORE the actual
            word in the list. 
            The suffix denotes the regexp syntax to come AFTER the 
            word. Both default to no string...
            Use the *prefix* and *suffix* args only if they will occur for EVERY word in
            the list. If not, include the ENTIRE regex as a single element in the list.
            lst is the list of hightlighting syntax rules to append.
            Format is the user defined format to utilize for highlighting.
        """
        if lst:
            for word in lst:
                # needs to be tested
                pattern = QRegExp(prefix + word + suffix)
                new_rule = HighlightingRule(pattern, format)
                self.highlighting_rules.append(new_rule)

# don't think this will work well in the long run...need to find an alternative
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
        """Checks for extension in dictionary of supported syntaxs,
           Automatically defaults to PlainText syntax highlighting (i.e. None)
           if anything other than supported file types are found...
        """

        lst = [i for i in self.EXT.keys()]
        if ext in lst:
            return self.EXT[ext]
        else:
            return PlainText



class PythonSyntax(PyCodeSyntaxHighlighter):
    """ Highlights regular python syntax"""

    def __init__(self, parent=None):
        super(PythonSyntax, self).__init__(parent)
        
        # common statement words
        self.keywordF.setForeground(self.TM_GET("keyword"))
        self.keywordF.setFontWeight(QFont.Bold)
        keyword_list  = (r"False|class|finally|is|return", 
                        r"None|continue|for|lambda|try",
                        r"True|def|from|nonlocal|while",
                        r"and|del|global|not|with|as",
                        r"elif|if|or|yield|assert|else",
                        r"import|pass|break|except|in|raise")

        for word in keyword_list:
            pattern = QRegExp("\\b" + word +"\\b")
            rule = HighlightingRule(pattern, self.keywordF)
            self.highlighting_rules.append(rule)

        # special methods
        self.keyword_reservedF.setForeground(self.TM_GET("keyword_reserved"))
        self.keyword_reservedF.setFontWeight(QFont.Bold)
        keywords_reserved = (r"__\w*__ | _\w* | __\w*",)

        for method in keywords_reserved:
            pattern = QRegExp("\\b" + method +"\\b")
            rule = HighlightingRule(pattern, self.keyword_reservedF)
            self.highlighting_rules.append(rule)

        # number
        self.numberF.setForeground(self.TM_GET("number"))
        pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")

        pattern.setMinimal(True)
        rule = HighlightingRule(pattern, self.numberF)
        self.highlighting_rules.append(rule)

        #number long
        self.number_longF.setForeground(self.TM_GET("number_long"))
        pattern = QRegExp(r"\d+L")
        rule = HighlightingRule(pattern, self.number_longF)
        self.highlighting_rules.append(rule)

        # builtin functions
        self.keyword_builtinF.setForeground(self.TM_GET("keyword_builtin"))
        keywords_builtin_list = (r"abs|divmod|input|open|staticmethod|all",
                                 r"enumerate|int|ord",  
                                 r"str|any|eval|isinstance|pow|sum", 
                                 r"basestring|execfile|issubclass|print", 
                                 r"super|bin|file|iter|property", 
                                 r"tuple|bool|filter|len|range|type", 
                                 r"bytearray|float|list|raw_input|unichr",
                                 r"callable|format|locals|reduce|unicode",
                                 r"chr|frozenset|long|reload|vars",
                                 r"classmethod|getattr|map|repr|xrange",
                                 r"cmp|globals|max|reversed|zip",
                                 r"compile|hasattr|memoryview|round", 
                                 r"complex|hash|min|set", 
                                 r"apply|delattr|help|next|setattr", 
                                 r"buffer|dict|hex|object|slice|coerce",
                                 r"dir|id|oct|sorted|intern",)
        
        # this (?<!\.) belongs in the following list
        keywords_exceptions_list = (r"ArithmeticError|AssertionError|AttributeError|"
                                    r"BaseException|DeprecationWarning|EOFError|EnvironmentError|"
                                    r"Exception|FloatingPointError|FutureWarning|GeneratorExit|IOError|"
                                    r"ImportError|ImportWarning|IndentationError|IndexError|KeyError|"
                                    r"KeyboardInterrupt|LookupError|MemoryError|NameError|"
                                    r"NotImplemented|NotImplementedError|OSError|OverflowError|"
                                    r"OverflowWarning|PendingDeprecationWarning|ReferenceError|"
                                    r"RuntimeError|RuntimeWarning|StandardError|StopIteration|"
                                    r"SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|"
                                    r"TypeError|UnboundLocalError|UnicodeDecodeError|"
                                    r"UnicodeEncodeError|UnicodeError|UnicodeTranslateError|"
                                    r"UnicodeWarning|UserWarning|ValueError|VMSError|Warning|"
                                    r"WindowsError|ZeroDivisionError",)
        
        for word in keywords_builtin_list:
            pattern = QRegExp(r"\b"+word+"(?=[(])+")
            rule = HighlightingRule(pattern, self.keyword_builtinF)
            self.highlighting_rules.append(rule)

        for word in keywords_exceptions_list:
            pattern = QRegExp("\b"+word+"\\b")
            rule = HighlightingRule(pattern, self.keyword_builtinF)
            self.highlighting_rules.append(rule)

        # names
        self.name_builtinF.setForeground(self.TM_GET("name_builtin"))
        name_pattern_list = ["(def)((\s)+)(?:.*)(?=[(])",
                             "(class)((\s)+)(?:.*)(?=[(])",
                             ]
        for word in name_pattern_list:
            pattern = QRegExp(word)
            rule = HighlightingRule(pattern, self.name_builtinF)
            self.highlighting_rules.append(rule)

        # function keywords
        self.keyword_functionF.setForeground(self.TM_GET("keyword_function"))
        keywords_functions = (r"class|def",)

        for word in keywords_functions:
            pattern = QRegExp("\\b"+ word +"\\b")
            rule = HighlightingRule(pattern, self.keyword_functionF)
            self.highlighting_rules.append(rule)

        # decorator's
        self.name_decoratorF.setForeground(self.TM_GET("name_decorator"))
        pattern = (r"@[A-z0-9_.]+")
        rule = HighlightingRule(pattern, self.name_decoratorF)
        self.highlighting_rules.append(rule)

        # string
        self.string_doubleF.setForeground(self.TM_GET("string_double"))
        pattern = QRegExp("[rR]?[uU]?\".*\"")
        rule = HighlightingRule(pattern, self.string_doubleF)
        self.highlighting_rules.append(rule)

        # single-quote string
        self.string_singleF.setForeground(self.TM_GET("string_single"))
        pattern = QRegExp( "[rR]?[uU]?\'.*\'")
        rule = HighlightingRule(pattern, self.string_singleF)
        self.highlighting_rules.append(rule)
        
        # multi-line comment
        self.string_docF.setForeground(self.TM_GET("string_doc"))
        pattern = QRegExp(r'^(\s*)("""(?:.|\n)*?""")',)
        rule = HighlightingRule(pattern, self.string_docF)
        self.highlighting_rules.append(rule)

        # multi-line single quote
        self.string_docF.setForeground(self.TM_GET("string_doc"))
        pattern = QRegExp(r"^(\s*)('''(?:.|\n)*?''')",)
        rule = HighlightingRule(pattern, self.string_docF)
        self.highlighting_rules.append(rule)

        # comments
        self.commentF.setForeground(self.TM_GET("comment"))
        pattern = QRegExp("#.*$")
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



class PerlSyntax(PyCodeSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PerlSyntax, self).__init__(parent)

    def highlightBlock(self, text):
        pass


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
        self.string_doubleF.setForeground(self.TM_GET("string_double"))
        pattern = QRegExp("\".*\"")
        rule = HighlightingRule(pattern, self.string_doubleF)
        self.highlighting_rules.append(rule)

        # single quotes string
        self.string_singleF.setForeground(self.TM_GET("string_single"))
        pattern = QRegExp("\'.*\'")
        rule = HighlightingRule(pattern, self.string_singleF)
        self.highlighting_rules.append(rule)

        # id selector color
        self.keyword_reservedF.setForeground(self.TM_GET("keyword_reserved"))
        pattern = QRegExp("[\.]\w+\\s+")
        rule = HighlightingRule(pattern, self.keyword_reservedF)
        self.highlighting_rules.append(rule)

        # comments multi/single
        self.comment_multiF.setForeground(self.TM_GET("comment"))
        pattern = QRegExp("/\*.*\*/")
        rule = HighlightingRule(pattern, self.comment_multiF)
        self.highlighting_rules.append(rule)

        # pseudo classes
        self.keyword_pseudoF.setForeground(self.TM_GET("keyword_pseudo"))
        self.keyword_pseudoF.setFontItalic(True)
        keyword_pseudo_list = (":+\w*\(?\)?\\s", ":+\w*\(?\)?\\s", ":+\w*-*\w*\(?\)?\\s",
                        ":+\w*-*\w*-*\w*\(?\)?\\s", ":+\w*-*\w*-*\w*-*\w*\(?\)?\\s",
                        ":+\w*\(?\)?\.?", ":+\w*\(?\)?\.?", ":+\w*-*\w*\(?\)?\.?",
                        ":+\w*-*\w*-*\w*\(?\)?\.?", ":+\w*-*\w*-*\w*-*\w*\(?\)?\.?")
        for key in keyword_pseudo_list:
            pattern = QRegExp(key)
            rule = HighlightingRule(pattern, self.keyword_pseudoF)
            self.highlighting_rules.append(rule)

        # keywords
        self.keywordF.setForeground(self.TM_GET("keyword"))
        self.keywordF.setFontWeight(QFont.Bold)
        # need to name all CSS keywords
        keyword_list = ("\\s+\w+:", "\\s+\w*-*\w+:", "\\s+\w*-*\w*-*\w+:",
                        "\\s+\w*-*\w*-*\w*-*\w*-*\w+:")
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

# incomplete
class JavaScriptSyntax(PyCodeSyntaxHighlighter):
    def __init__(self, parent=None):
        super(JavaScriptSyntax, self).__init__(parent)

    def highlightBlock(self, text):
        pass


class LuaSyntax(PyCodeSyntaxHighlighter):
    def __init__(self, parent=None):
        super(LuaSyntax, self).__init__(parent)

    
        """
            For `Lua <http://www.lua.org>`_ source code.
        """
        # filenames = ['*.lua', '*.wlua']
        # mimetypes = ['text/x-lua', 'application/x-lua']

    
        # keyword
        self.keywordF.setForeground(self.TM_GET("keyword"))
        keyword_list = (r"and|break|do|else|elseif|end", 
                        r"false|for|function|goto|if|in|local",
                        r"nil|not|or|repeat|return",
                        r"then|true|until|while")
        
        self.add_list_of_rules(lst=keyword_list, format=self.keywordF)
        

        # keyword reserved
        self.keyword_reservedF.setForeground(self.TM_GET("keyword_reserved"))
        keyword_reserved_list = ("_+[A-Z]+")

        self.add_list_of_rules(lst=keyword_reserved_list, format=keyword_reservedF)


        # operators
        self.operatorF.setForeground(self.TM_GET("operator"))
        operator_list = (r"+|-|*|[/]|%|[^]|#",
                         r"==|~=|<=|>=|<|>|=",
                         r"\(|\)|\{|\}|\[|\] |::",
                         r";|:|,|\.|\.\.|\.\.\.")
        self.add_list_of_rules(lst=operator_list, format=self.operatorF) 


        #comment
        self.commentF.setForeground(self.TM_GET("comment"))
        comment_list = (r'#!(.*?)$',"--.*$")    
        

            # (r'', Text, 'base'),

        # number float
        self.number_floatF.setForeground(self.TM_GET("number_float"))
        float_list = (r'(?i)(\d*\.\d+|\d+\.\d*)(e[+-]?\d+)?', 
                      r'(?i)\d+e[+-]?\d+')
        self.add_list_of_rules(lst=float_list, format=self.number_floatF)
        
        
        # hex
        self.number_hexF.setForeground(self.TM_GET("number_hex"))
        hex_list = ('(?i)0x[0-9a-f]*')
        self.add_list_of_rules(hex_list, self.number_hexF)

        # integer
        self.number_integerF.setForeground(self.TM_GET("number_integer"))
        int_list =  (r'\d+')
        self.add_list_of_rules(int_list, self.number_integerF)

        # string
        self.string_singleF.setForeground(self.TM_GET("string_single"))
        single_string_list = (r"\n", r"[^\S\n]")
        self.add_list_of_rules(single_string_list, self.string_singleF)            
        
        # multiline strings
        self.string_doubleF.setForeground(self.TM_GET("string_double"))
        double_string_list = (r"(?s)\[(=*)\[.*?\]\1\]", r"(?s)--\[(=*)\[.*?\]\1\]")
        self.add_list_of_rules(double_string_list, self.string_doubleF)

        # operator
        self.punctuationF.setForeground(self.TM_GET("punctuation"))
        punctuation_list = (r"[\[\]\{\}\(\)\.,:;]",)
        self.add_list_of_rules(punctuation_list, self.punctuationF)


    # (r'(function)\b', Keyword, 'funcname'),

    # (r'[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?', Name),

    # ("'", String.Single, combined('stringescape', 'sqs')),
    # ('"', String.Double, combined('stringescape', 'dqs'))

    #     'funcname': [
    # (r'\s+', Text),
    # ('(?:([A-Za-z_][A-Za-z0-9_]*)(\.))?([A-Za-z_][A-Za-z0-9_]*)',
    #         # inline function
    # ('\(', Punctuation, '#pop'),
    #     ],

    #     # if I understand correctly, every character is valid in a lua string,
    #     # so this state is only for later corrections
    #     'string': [
    #         ('.', String)
    #     ],

    #     'stringescape': [
    #         (r'''\\([abfnrtv\\"']|\d{1,3})''', String.Escape)
    #     ],

    #     'sqs': [
    #         ("'", String, '#pop'),
    #         include('string')
    #     ],

    #     'dqs': [
    #         ('"', String, '#pop'),
    #         include('string')
    #     ]
    # }

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

