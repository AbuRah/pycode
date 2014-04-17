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

"""


import sys
import os
import codecs
import re

from functools import partial
from PySide.QtCore import *
from PySide.QtGui import *
from SyntaxClasses import (PythonSyntax, HtmlSyntax, PlainText, CSSSyntax,
PyCodeIdentifier)

from PyCodeCore import (PyCodeTabInterface, PyCodePage, PyCodeDockWidget,
PyCodeStatusBar, PyCodeAction, PyCodeMenu, PyCodeSettings, PyCodeShortcuts)



# Do Note the following:
# at the moment, PyCodeMenuBar isn't decoupled from this module. It *may* not 
# run due to current code transformations occuring. Just a reminder to address 
# this issue.
# Also, due to tab constraints in emacs, i've mixed spaces and tabs in this
# module and the PyCodeCore module (GASP!)

# Need to test this...

class PyCodeMenuBar(QMenuBar):
    """Responsible for holding all menus and menu actions.
       This class does *not* fit in core, way too many dependencies.
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

# this class has been suspended until encoding features are implemented.
class PyCodeDialogWindow(QDialog):
    def __init__(self, parent=None):
        super(PyCodeDialogWindow, self).__init__(parent)
        self.setLayout(None)
        self.set_attributes()
        self.initUI()
        self.set_signal_slots()

    def set_attributes(self):
        self.setSizeGripEnabled(True)

    def initUI(self):
        """Constructs user interface"""

        self.main = QVBoxLayout(self)
        self.header_layout()
        self.view_window_layout()
        self.file_name_entry_layout()
        self.main_button_line()


        # hides file name entry line
        self.main.addWidget(self.dialog_header)
        self.main.addWidget(self.center)
        self.main.addWidget(self.file_name_line)
        self.main.addWidget(self.command_line_buttons)

        self.main.addSpacing(1)

        self.setLayout(self.main)

    def set_signal_slots(self):
        """sets up all necessary signals and slots."""
        self.default_button.triggered.connect(self.accept)
        self.cancel_button.triggered.connect(self.reject)

    
    def set_view_mode(self):
        """sets view mode between icons and icon/text"""
        if not tmp_counter:
            return self.file_list_view.setViewMode(True)
            tmp_counter = 0
        else:
            return self.file_list_view.setViewMode(False)

    def header_layout(self):
        """Sets the upper portion layout of the dialog window."""
        self.dialog_header = QHBoxLayout(self)
        self.file_header = QLineEdit(self)
        self.up_button = QToolButton(self)
        self.down_button = QToolButton(self)
        self.new_folder_buttom = QToolButton(self)

        self.dialog_header.addWidget(self.new_folder_buttom)
        self.dialog_header.addWidget(self.file_header)
        self.dialog_header.addWidget(self.up_button)
        self.dialog_header.addWidget(self.down_button)

    def file_name_entry_layout(self):
        """lays out the file entry bar..."""
        self.file_name_line = QHBoxLayout(self)
        self.file_name = QLineEdit(self)

        self.folder_search = QToolButton(self)

        self.file_name_line.addWidget(self.file_name)

    def view_window_layout(self):
        """sets up the layout for the file view area..."""
        self.center = QHBoxLayout(self)
        self.main_splitter = QSplitter(self)
        
        self.file_model = QFileSystemModel(self)
        self.testing_dir = QDir(os.getcwd())
        self.file_list_view = QListView(self)
        self.folder_tree_view = QTreeView(self)


        self.file_model.setRootPath(self.testing_dir.rootPath())
        self.file_list_view.setModel(self.file_model)
        self.folder_tree_view.setModel(self.file_model)
        

        self.main_splitter.addWidget(self.file_list_view)
        self.main_splitter.addWidget(self.folder_tree_view)

        self.file_list_view.setLayoutMode(QListView.Batched)
        self.file_list_view.setBatchSize(25)
        self.file_list_view.setSpacing(4)


    def main_button_line(self):
        """lays out the commonly expected buttons, such as 'save', 'open', 
            'cancel', etc...
            """

        self.command_line_buttons = QHBoxLayout(self)
        self.default_button = QPushButton("TESTING", self)
        self.cancel_button = QPushButton("CANCEL", self)
        self.default_button.setDefault(True)

        self.command_line_buttons.addWidget(self.default_button)
        self.command_line_buttons.addWidget(self.cancel_button)


class TabInterface(PyCodeTabInterface):
    """I've created theis class and the Page class so that
       the inter-dependency of the main program is clear. Nothing
       in the PyCodeCore module will directly affect any connections made
       here...once i'm finished...
    """
    def __init__(self, parent=None):
        super(TabInterface, self).__init__(parent)
        self.grab_sm_bars()
        self.IDENTIFIER = PyCodeIdentifier(self)
        

    def new_file(self):
        """Creates a new file"""
        page = Page(self)
        PlainText(page.document())
        return self.addTab(page, "Untitled")

    def open_folder(self):
        """Opens every file supported in a user-selected folder"""
        # TODO: open a tree-view into folder from which user can select files.
        pass

    def open_file_dialog(self):
        """opens file in new tab
           In the middle of testing at the moment.
        """

        # i think the encoding feature should come later...
        # does not pass arg if called from open w/ encoding menu...
        # I'm trying to create my own Dialog class in order to 
        # avoid dependence upon the PySide Framework.
        file_name,_ = QFileDialog.getOpenFileName(self,
            "Open File", os.getcwd())

        if file_name != '':

            with open(file_name, "r") as f:
                
                data = f.read()
                new_page = Page(self)
                new_page.setPlainText(data)
                f.close()
                
                # codense the following two lines of code
                nameHolder = QFileInfo(file_name)
                nameOfFile = nameHolder.fileName()
                
                set_syntax = self.get_syntax_highlighter(file_name)
                set_syntax(new_page.document())                 

                self.addTab(new_page, nameOfFile)
        else:
            print "open file failed"


    def grab_sm_bars(self):
        """grabs menus from mainwindow"""
        self.MENU = self.P.menuBar()
        self.STATUS = self.P.statusBar()

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

    def reopen_last_tab(self):
        """Opens the last tab closed"""

        if len(self._CLOSED_TABS) > 0:

            new_page = Page(self)
            last_file = self._CLOSED_TABS.pop()

            try:

                with open(last_file, "r") as f:
                    data = f.read()
                    new_page.setPlainText(data)
                    
                    set_syntax = self.get_syntax_highlighter(file_name)
                    set_syntax(new_page.document())                 
                    
                    self.addTab(new_page, last_file)
                    self.currentWidget().setFocus()
        
            except IOError:
                pass

        else:
            pass

            


class Page(PyCodePage):
    """As written above in TabInterface class, this is here only to condense 
       and make clear the inter-dependency of the program. Nothing in PyCodeCore
       *should* cause dependency issues as no code real manipulation takes place there.
    """
    def __init__(self, parent=None):
        super(Page, self).__init__(parent)
        self.grab_sm_bars()

    def grab_sm_bars(self):
        """Takes control of menu and status bars
            Should only run once as a part of initial set-up
        """
        self.STATUS = self.TI.STATUS
        self.MENU = self.TI.MENU
    
    def hide_statusbar(self):
        """Hides status bar"""
        if not self.tmp_counter:
            self.STATUS.hide()
            self.tmp_counter += 1
        else:
            self.STATUS.show()
            self.tmp_counter -= 1

    def find_text(self):
        """Find the indicated text within the current tab page"""
        # need to add auto-complete, find & replace
        # i can make this called from the DockWidget instance
        Dock_widget = self.TI.parent().DOCKW
        Dock_widget.show()
        Dock_widget.user_input.setFocus()
        Dock_widget.set_slot_connections()

        update = self.TI.currentWidget().document().find(Dock_widget.user_input.text())
        self.TI.currentWidget().setTextCursor(update)
        self.TI.currentWidget().textCursor().select(QTextCursor.WordUnderCursor)
            

    def find_regexp(self):
        """Find the indicated text within the current tab page"""
        # need to add auto-complete, find & replace
        # i can make this called from the DockWidget instance
        Dock_widget = self.TI.parent().DOCKW
        Dock_widget.show()
        Dock_widget.user_input.setFocus()
        Dock_widget.set_slot_connections_regexp()

        user_regexp = QRegExp(Dock_widget.user_input.text())
        update = self.TI.currentWidget().document().find(user_regexp, Qt.MatchRegExp)
        self.TI.currentWidget().setTextCursor(update)
        self.TI.currentWidget().textCursor().select(QTextCursor.WordUnderCursor)
    


    # i'm going to have to find a better way to set syntax highlighting,
    # this class should *not* depend upon the SyntaxClasses module
    def css_syntax(self):
        """sets CSS syntax highlighting"""
        CSSSyntax(self.document())
        self.TI._SYNTAX_DICT[self.TI.currentIndex()] = self.css_syntax
        self.STATUS.current_syntax.setText("CSS")

    def python_syntax(self):
        """sets python syntax highlighting for textdocument in focus"""
        PythonSyntax(self.document())
        self.TI._SYNTAX_DICT[self.TI.currentIndex()] = self.python_syntax
        self.STATUS.current_syntax.setText("Python")

    def plain_text(self):
        """Sets plain text syntax highlighting for textdocument in focus"""
        PlainText(self.document())
        self.TI._SYNTAX_DICT[self.TI.currentIndex()] = self.plain_text
        self.STATUS.current_syntax.setText("PlainText")

    def html_syntax(self):
        """sets syntax highlighting to HTML"""
        HtmlSyntax(self.document())
        self.TI._SYNTAX_DICT[self.TI.currentIndex()] = self.html_syntax
        self.STATUS.current_syntax.setText("HTML") 

    def clone_doc(self):
        """clones current document in focus"""
        cloned_doc = self.document().clone(self)
        new_page = Page(self.TI)
        new_page.setDocument(cloned_doc)
        self.TI.addTab(new_page, "Untitled")

# MENU CLASSES=================

    
# i belive these should remain here instead of being moved to the CORE module

class FileMenu(PyCodeMenu):
    """Responsible for all FileMenu specific actions, signal/slot connections 
        are NOT to be made here.
        I've choosen to separate action creation and signal/slot connections 
        to offer more flexibility and have one core responsibility for each
        respective class.
        The most common selections in a file menu will be added by default,
        however, if you desire to add more menu options, use the 
        create_action method-function. More detail will be written later...
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
        self.create_action("OpenFolder_act", "Open Folder", "Open Folder")
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
        self.create_action("kill_line", "Kill Line", "Ctrl+k")
        self.create_action("delete_line", "Delete Line", "Ctrl+Shift+K")
        self.create_action("line_up", "Move line up", "Ctrl+Shift+Up")
        self.create_action("line_down", "Move line down", "Ctrl+Shift+Down")
        self.create_action("clone_line", "Clone current line", "Ctrl+Shift+D")
        self.create_action("line_select", "Select current line", "Ctrl+L")
        self.create_action("indent_paste", "Paste and indent", "Shift+Ctrl+V")


class ViewMenu(PyCodeMenu):
    """Defines and Holds all view menu specific actions
        If there are any sub-menus for the view menu, be sure to update
        the main self.VIEW_ACTIONS dictionary appropriately using the
        *update_dict* method inherited from PyCodeMenu.
    """
    def __init__(self, name="Default", parent=None):
        super(ViewMenu, self).__init__(name, parent)
        self.VIEW_ACTIONS = self.ALL_ACTIONS
        # these two may be redundant
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


class IDEMenu(PyCodeMenu):
    def __init__(self, parent=None):
        super(IDEMenu, self).__init__(parent)


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

# the encoding menu classes need to be changed. Windows specific encoding along with a menu for just
# European languages is not the most intuitive. The menu should display language options with the avaliable
# encoding number next to it...
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
        
        self.ENC_MAIN = self.ALL_ACTIONS
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
        
        self.create_action("gbk_act", "Chinese Simplified(GBK)", status="GBK")
        self.create_action("gb18030_act", "Chinese Simplified(GB18030)", status="GB18030")
        self.create_action("big5_act", "Chinese Traditional(Big5)", status="Big-5")
        self.create_action("big5hkscs_act", "Chinese Traditional(Big5-HKSCS)", status="Big5-HKSCS")
        self.update_dict(self.ENC_MAIN, self.win_menu.ALL_ACTIONS)
        self.update_dict(self.ENC_MAIN, self.iso_menu.ALL_ACTIONS)      


        # check if python supports any of these languages...
        # self.create_action("gb2312_act", "Chinese", "GB2312") may not use
        # self.create_action("ksx1001_act", "UTF-8") may not use
        # self.create_action("euc-kr_act", "UTF-8") may not use
        # self.create_action("jis_x_0208_act", "Japenese", ) may not use
        # self.create_action("euc_jis_act", "UTF-8") python supports this
        # self.create_action("iso-2022_act", "UTF-8") python supports this
        # self.create_action("iscii_act", "Indian(ISCII)", status="ISCII") # not supported

    # i may be able to make this an inherited method in pycodemenu core.
    def make_menus(self):
        """Constructs submenu constants."""
        self.win_menu = WindowsEncodingMenu("Windows", self)
        self.iso_menu = EuropeanEncodingMenu("European", self)


# TRIGGER CLASSES ============
"""These trigger classes are where a LOT of the inter-dependent connections occur.
   I will attempt to make this as much as will allow an easy time with debugging
   OR to the degree that will allow easy assimilation of how this
   all works...

"""
class OpenEncMenuTriggers(MainEncodingMenu):
    """defines all encoding Menu signal/slot connections
       specific to the OpenEncMenu sub-menu.
       This is constructed in the Filemenu class. Watch for 
       dependencies.
       As I've mentioned elsewhere, the *reset_all* method is inherited from
       PyCodeMenu core class. If there are any issues with it, check there...
    """
    def __init__(self, name=None, parent=None):
        super(OpenEncMenuTriggers, self).__init__(name, parent)
        self.ENC_GET = self.ENC_MAIN.get
        # this isn't init'd in the base class
        self.PP_C = parent.parent()


    def update_connections(self):
        """Calls the relevant update functions"""
        self.reset_all(self.ENC_MAIN.values(), self.PP_C)
        self.update_triggers()

    def update_triggers(self):
        """This method sets all Edit menu actions' connections
           All of the available actions will be connected to the same slot, that is
           the PyCodeTabInterface method open_file_dialog.
           I'm trying to avoid having to create all of these functions
           with the proper argument passed individually, i.e. the same function
           only with a different name.
        """

        # testing...  broken; Here is the issue i'm currently
        # having, this calls open_file_dialog multiple times
        # when used with partial().  when partial is left out
        # of the equation, one only call is made for each
        # signal emission. That means i cannot, with my current
        # set-up, pass an argument to the slot...
        for key, action in self.ENC_MAIN.items():
            action.triggered.connect(self.PP_C.open_file_dialog)



class SaveEncMenuTriggers(MainEncodingMenu):
    """The layout here is identical to the OpenEncMenuTriggers class
       95% of what applies there also applies here.
    """
    def __init__(self, name=None, parent=None):
        super(SaveEncMenuTriggers, self).__init__(name, parent)
        self.ENC_S_GET = self.ENC_MAIN.get
        self.PP_C = parent.parent()


    def update_connections(self):
        self.reset_all(self.ENC_MAIN.values(), self.PP_C)
        self.update_triggers()

    def update_triggers(self):

        for action in self.ENC_MAIN.values():
            action.triggered.connect(self.PP_C.save_event)



# i think i may create a module specifically for all menu related classes...
class FileMenuTriggers(FileMenu):
    """ This class holds all file menu action signals and slots.
        The signal/slot connections related to the file menu are 
        to go in this class.
    """
    def __init__(self, name=None, parent=None):
        super(FileMenuTriggers, self).__init__(name, parent)
        self.F_DICT = self.FILE_ACTIONS.get
        # self.P_C = parent.CHILD this may not work...
        self.P = parent
        self.F_DICT("exit_act").triggered.connect(self.exit_event)
        self.F_DICT("newW_act").triggered.connect(self.new_window)
        self.F_DICT("closeW_act").triggered.connect(self.close_window)


    def update_triggers(self):
        """updates pertinent triggers to respective slots"""
        # these need to be set after init due to coupling issues....
        self.F_DICT("save_act").triggered.connect(self.P_C.save_event)
        self.F_DICT("openF_act").triggered.connect(self.P_C.open_file_dialog)
        self.F_DICT("save_as_act").triggered.connect(self.P_C.save_file_as)
        self.F_DICT("newF_act").triggered.connect(self.P_C.new_file)
        self.F_DICT("save_all_act").triggered.connect(self.P_C.save_all)
        self.F_DICT("close_all_act").triggered.connect(self.P_C.close_all)
        self.F_DICT("reopenF_act").triggered.connect(self.P_C.reopen_last_tab)
        self.F_DICT("closeF_act").triggered.connect(self.P_C.close_tab)
        # self.F_DICT("OpenFolder_act").triggered.connect(self.P_C.open_folder)

    # to me, these feel out of place. They should be encapsulated elsewhere...
    def new_window(self):
        """opens a completely new window."""
        self.new_window_instance = PyCodeTop()
        return self.new_window_instance.show()

    def close_window(self):
        """Close active window"""
        return self.parent().close()
    
    def exit_event(self):
        """Exits without prompting"""
        if self.P.SETTINGS:
                    self.P.SETTINGS.write_settings()
        sys.exit()


class EditMenuTriggers(EditMenu):
    """Responsible for all edit menu specific triggers.
         be wary of this....
          testing, these should still work appropriately, causing no
          bugs. I've moved this init to the base PyCodeMenu class...
          between this init and the ancestor base pycode class, there
          are no parent assignments
         self.P_C, self.P_C_T = parent, parent
    """
    def __init__(self, name=None, parent=None):
        super(EditMenuTriggers, self).__init__(name, parent)
        self.E_DICT = self.EDIT_ACTIONS.get
        # self.P_C should be set to parent.CHILD in PyCodeTop
        # class.  if there are any issues, it's because a
        # trigger menu method is being called before self.P_C
        # is switched from parent to parent.CHILD
        

    def update_connections(self):
        """Calls both the inherited *reset_all* method and then
            follows up with *update_triggers*
                """
        self.reset_all(self.EDIT_ACTIONS.values(), self.P_C_T)
        self.update_triggers()


    def update_triggers(self):
        """This method sets all Edit menu actions' connections"""
        self.P_C_T = self.P_C.currentWidget()

        if self.P_C_T:
            # Not yet implemented
            self.E_DICT("find_act").triggered.connect(self.P_C_T.find_text)
            self.E_DICT("find_regexp_act").triggered.connect(self.P_C_T.find_regexp)
            self.E_DICT("redo_act").triggered.connect(self.P_C_T.redo_last)
            self.E_DICT("undo_act").triggered.connect(self.P_C_T.undo_last)
            self.E_DICT("cut_act").triggered.connect(self.P_C_T.cut_selection)
            self.E_DICT("paste_act").triggered.connect(self.P_C_T.paste_selection)
            self.E_DICT("copy_act").triggered.connect(self.P_C_T.copy_selection)
            self.E_DICT("clone_act").triggered.connect(self.P_C_T.clone_doc)
            self.E_DICT("kill_line").triggered.connect(self.P_C_T.kill_to_end_of_line)
            self.E_DICT("delete_line").triggered.connect(self.P_C_T.delete_line)
            self.E_DICT("line_up").triggered.connect(self.P_C_T.line_up)
            self.E_DICT("line_down").triggered.connect(self.P_C_T.line_down)
            self.E_DICT("clone_line").triggered.connect(self.P_C_T.clone_line)
            self.E_DICT("line_select").triggered.connect(self.P_C_T.current_line_select)
            self.E_DICT("indent_paste").triggered.connect(self.P_C_T.paste_and_indent)


class ViewMenuTriggers(ViewMenu):
    """This class holds all view action connections. i.e. signals and slots 
        for the view menu
    """
    def __init__(self, name=None, parent=None):
        super(ViewMenuTriggers, self).__init__(name, parent)
        self.V_GET = self.VIEW_ACTIONS.get



    def update_connections(self):
        """Updates all signal/slot connections"""
        self.reset_all(self.VIEW_ACTIONS.values(), self.P_C_T)
        self.update_triggers()

    def update_triggers(self):
        self.P_C_T = self.P_C.currentWidget()

        if self.P_C_T:
            self.V_GET("hide_status_act").triggered.connect(self.P_C_T.hide_statusbar)
            self.V_GET("python_syn").triggered.connect(self.P_C_T.python_syntax)
            self.V_GET("plain_syn").triggered.connect(self.P_C_T.plain_text)
            self.V_GET("html_syn").triggered.connect(self.P_C_T.html_syntax)
            self.V_GET("css_syn").triggered.connect(self.P_C_T.css_syntax)
            self.V_GET("zoom_in").triggered.connect(self.P_C_T.zoom_in)
            self.V_GET("zoom_out").triggered.connect(self.P_C_T.zoom_out)
            self.V_GET("word_wrap_act").triggered.connect(self.P_C_T.set_word_wrap)

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
        

    def update_connections(self):
        self.reset_all(self.TOOL_ACTIONS.values(), self.P_C_T)
        self.update_triggers()

    def update_triggers(self):
        
        self.P_C_T = self.P_C.currentWidget()
        
        if self.P_C_T:
            
            for action in self.TOOL_ACTIONS.values():
                # partial also causes this to connect multiple times after the 
                # signal connects to the initial connection...
                # to/do find a way to pass arg without multiple function calls...
                action.triggered.connect(self.P_C_T.set_tab_width)
            


class PrefMenuTriggers(PrefMenu):
    """This class is responsible for all preference specific
       action triggers.  As mentioned earlier above, this class
       *depends* upon a connection with an instantiation of
       TabInterface at *some* point. If not, this will not
       function properly
    """
    def __init__(self, name=None, parent=None):
        super(PrefMenuTriggers, self).__init__(name, parent)
        self.P_GET = self.PREF_ACTIONS.get
        

    def update_connections(self):
        self.reset_all(self.PREF_ACTIONS.values(), self.P_C_T)
        self.update_triggers()

    def update_triggers(self):
        self.P_C_T = self.P_C.currentWidget()
        if self.P_C_T:
            self.P_GET("font_inc_act").triggered.connect(self.P_C_T.increase_font_size)
            self.P_GET("font_dec_act").triggered.connect(self.P_C_T.decrease_font_size)
            self.P_GET("serif_font_act").triggered.connect(self.P_C_T.set_serif)
            self.P_GET("monospace_font_act").triggered.connect(self.P_C_T.set_monospace)
            self.P_GET("sans_serif_font_act").triggered.connect(self.P_C_T.set_sansserif)

class PyCodeShortcutTriggers(PyCodeShortcuts):
    """This class is Responsible for holding all *shortcut* signals and their 
       respective slots. P_C is a naming convention. Wherever this appears, 
       it refers to parent.child.
       Debugging Note: there aren't any parent assignments between this and it's ancestor class
       QObject...
       
    """
    def __init__(self, parent=None):
        super(PyCodeShortcutTriggers, self).__init__(parent)
        self.SHORT_GET = self._ALL_SHORTCUTS.get
        self.P_C = parent


    def set_shortcut_slots(self):
        # should think about connecting to Qactions instead....
        self.SHORT_GET("move_right").activated.connect(self.P_C.tab_seek_right)
        self.SHORT_GET("move_right2").activated.connect(self.P_C.tab_seek_right)
        self.SHORT_GET("move_left").activated.connect(self.P_C.tab_seek_left)
        self.SHORT_GET("move_left2").activated.connect(self.P_C.tab_seek_left)
        self.SHORT_GET("close_focused_win").activated.connect
        self.SHORT_GET("close_dock").activated.connect
        # self.SHORT_GET("cut_act").activated.connect(self.P_C.cut_selection)



# MISC CLASSES================
class SettingsTmp(PyCodeSettings):
    """ The only reason this is here is due to it's class dependency, the core
        class in located in PyCodeCore module.
    """
    def __init__(self, parent=None):
        super(SettingsTmp, self).__init__(parent)
    
    def read_settings(self):
        """Loads the saved settings from a previous session
           How ever many file names are save in the array, they will
           be initiated with the appropriate syntax highlighter set.
        """
        # self.settings = QSettings("AD Engineering", 
        #               "PyCode Text Editor")
        # that ^^^ is only for reference purposes, ignore...

        
        # re-open any files left open from last session
        self.settings.beginGroup("Main Window")
        size = self.settings.beginReadArray("files")
        for i in xrange(size):
            self.settings.setArrayIndex(i)
            file_name = self.settings.value("filename")
            try:
                with open(file_name, "r") as f:
                    data = f.read()
                    f.close()
                    new_page = Page(self.P_C)
                    new_page.setPlainText(data)
                    
                    set_syntax = self.P_C.get_syntax_highlighter(file_name)
                    set_syntax(new_page.document())
                    
                    self.P_C.addTab(new_page, file_name)
                    
            except IOError:
                pass

        self.settings.endArray()

        self.P.move(self.settings.value("Position"))
        self.P.resize(self.settings.value("Size"))
        self.settings.endGroup()

# dock widget testing....
class DockWidget(PyCodeDockWidget):
    """This dockWidget will serve as the bottom line bar for searches, find operations
        and other simple tasks.
    """
    def __init__(self, parent=None):
        super(DockWidget, self).__init__(parent)
        self.P_C = parent

    def set_slot_connections(self):
        """This method will update the current method and page DockWidget
            is connected to.
        """
        self.P_C_T = self.P_C.currentWidget()
        
        try:
            self.user_input.disconnect(self.P_C_T)
            self.user_input.textChanged.connect(self.P_C_T.find_text)
        
        except AttributeError:
            print "error processed"

    def set_slot_connections_regexp(self):
        """This method will update the current method and page DockWidget
            is connected to.
        """
        self.P_C_T = self.P_C.currentWidget()
        
        try:
            self.user_input.disconnect(self.P_C_T)
            self.user_input.textChanged.connect(self.P_C_T.find_regexp)
        
        except AttributeError:
            print "error processed"




class PyCodeTop(QMainWindow):
    """This will bring all classes together to make up the final application.
        All children after PyCodeTabInterface DEPEND upon the self.CHILD constant.
    """
    def __init__(self, parent=None):
        super(PyCodeTop, self).__init__(parent)
        self.initUI()
        self.set_child_connections()
        self.SETTINGS.read_settings()
        # this checks if there are any opened tabs from the last session...
        if not self.CHILD.currentWidget():
            self.CHILD.new_file()
        self.set_stylesheet()

    def set_child_connections(self):
        """Here most of the interdependent connections take place.
                   If there's a bug, this would be THE place to check...
           I've attempted to condense all signal/slot connection coupling in this
           ONE function. Everything that needs to be coupled occurs here.
        """
        self.CHILD = self.findChild(TabInterface)
        self.SETTINGS.P_C = self.CHILD
        self.DOCKW.P_C = self.CHILD
        self.SHORT.P_C = self.CHILD
        self.SHORT.set_shortcut_slots()
        self.CHILD.grab_sm_bars()
        self.CHILD.set_signal_slots()
        self.menuBar().set_CHILD_constant()

    def initUI(self):
        """Here, the main instantance creation takes place. The order
           *does* matter. Code in the *set_child_connections* depends upon this
           order, So be wary of how you order the instance creation.
        """
        self.setWindowTitle("PyCode Text Editor")
        status = PyCodeStatusBar(self)
        menu = PyCodeMenuBar(self)
        self.setMenuBar(menu)
        self.setStatusBar(status)
        main = TabInterface(self)
        self.setCentralWidget(main)
        
        self.SETTINGS = SettingsTmp(self)
        self.SHORT = PyCodeShortcutTriggers(self)
        self.DOCKW = DockWidget(self)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.DOCKW)

    def set_stylesheet(self):
        """sets PyCode Stylesheet"""
        # todo: make this customizable.i.e. load user settings.
        try:
            with open("../PyCodeThemes/PyCodeDeepViolet.qss") as f:
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
