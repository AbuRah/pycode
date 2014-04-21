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
#--coding:utf-8---
import re
import os

from PySide.QtGui import *
from PySide.QtCore import *



# NOTE: the classes are *not* organized...

class PyCodeTabInterface(QTabWidget):
    """This class and the PyCodePage class are where most of the relevant slots and
        modifications will be. i.e. if you want to find where cursor manipulation takes
        place, it would be in one of these classes.
        
        Whenever the actor changes tabs, the menubar and statusbar will both be automatically
        updated to reflect the pycodepage instance's menubar and statusbar. It will then
        set PyCodeTop to hold these updated status/menubars.
        The _SYNTAX_DICT constant holds the syntax highlighting class applied to it's
        respective document. e.g. if PythonSyntax is set for the first tab page, 
        HTML for the second, their respective entries will look like this::
    
        >> self._SYNTAX_DICT[0]
        "Python"

        >> self._SYNTAX_DICT[1]
        "HTML"

        etc....
                The closed tabs list holds the file-names of recently closed tabs...
                In order to continue with composition, this class will be coupled with the 
                PyCodeIdentifier class...


    """


    _CLOSED_TABS = []
    _SYNTAX_DICT = {}

    def __init__(self, parent=None):
        super(PyCodeTabInterface, self).__init__(parent)
        self.init_setup()
        self.P = parent
        # the need to wrap the document in a class causes a
        # class dependency to arise. I may have to move this
        # to the main module

        

    def init_setup(self):
        """Sets up all options pertinent to QTabWidget"""
        self.setFocusPolicy(Qt.NoFocus)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setElideMode(Qt.ElideRight)


    def set_signal_slots(self):
        """Sets the signal connections to their appropriate slots."""
        #self.currentChanged.connect(self.grab_sm_bars)
        self.currentChanged.connect(self.set_syntax)
        self.tabCloseRequested.connect(self.close_tab)


    def set_syntax(self):
        """sets appropriate syntax highlighting whenever a tab page is switched
                   First we check to ensure there are tabs and there are entries in the 
                   *_SYNTAX_DICT* constant...
                   The value stored there is the syntax_setting specific method which only needs
                   to be called, hence the empty parens at the end...
                """

        if self.count() and self._SYNTAX_DICT:
                    
                        self._SYNTAX_DICT.get(self.currentIndex())()
            #set_syn = self._SYNTAX_DICT.get(self.currentIndex())
            #set_syn()


    # # practice/testing
    # def testing(self, enc):
    #   # when opening file use decode(encoding specified)
    #   data = f.read()
    #   data.decode(enc)
    #   # when writing to file, use encode(encoding specified)

    def auto_save_event(self):
        """When toggled, this method will automate file saving.
            In order to prevent unwanted saving for modifications,
            this method will save file name as, then save the newly
            named file. e.g. some_file.txt, would be saved as,
            some_file~.txt. 
        """
        # TODO: make this method run at intervals.
        file_name = self.tabText(self.currentIndex())
        
        if file_name[0] != "~":
            file_name = "~" + file_name

        save_file = QFile(file_name)

        f = open(file_name, "w")

        with f:
            data = self.currentWidget().toPlainText()
            try:
                # codecs.encode(data, enc)
                f.write(data)

            except ValueError:
                print "error processing goes here"

            finally:
                f.close()
            
            self.P.statusBar().showMessage(
                                    "Saved %s" % file_name, 4000)






    def save_event(self, enc="utf-8"):
        """Saves current file, except if "Untitled"; it will prompt user
            to save.
        """
        file_name = self.tabText(self.currentIndex())       

        save_file = QFile(file_name)

        if file_name != "Untitled":
            f = open(file_name, "w")

            with f:
                data = self.currentWidget().toPlainText()
                try:
                    # codecs.encode(data, enc)
                    f.write(data)

                except ValueError:
                    print "error processing goes here"

                finally:
                    f.close()
                
                self.P.statusBar().showMessage(
                                        "Saved %s" % file_name, 4000)

        else:
            return self.save_file_as()
    
    def save_all(self):
        """Save all opened files, prompt if "Untitled" page exists"""
        for i in xrange(self.count()):
            
            file_name = self.tabText(i)
            if file_name != "Untitled":
                # not sure why this is here...
                save_file = QFile(file_name)

                with open(file_name, "w") as f:
                    data = self.widget(i).toPlainText()
                    f.write(data)
                    f.close()
            else:
                self.save_file_as()

        return self.P.statusBar().showMessage(
                                    "Saved All Opened Files", 4000)

    def save_file_as(self):
        """Save current file as"""

        file_name, _ = QFileDialog.getSaveFileName(self,
            "Save File", os.getcwd())

        # could use RegExp search to catch more complicated errors here
        if file_name != '':

            f = open(file_name, "w")

            with f:

                data = self.currentWidget().toPlainText()
                
                f.write(data)
                f.close()

                nameHolder = QFileInfo(file_name)
                nameOfFile = nameHolder.fileName()
                self.setTabText(self.currentIndex(), nameOfFile)
        
        else:
            pass


    def close_tab(self):
        """Closes focused tab"""
        # need to take the file either using the os module or
                # PySide's QFile, QDir etc....
        file_name = self.tabText(self.currentIndex())
        # TODO: ask user if they would like to save IF file is untitled
        # if file_name == "Untitled":

        self._CLOSED_TABS.append(file_name)
        self.removeTab(self.currentIndex())


        try:
            return self.currentWidget().setFocus()
        
        except AttributeError:
            pass

    def close_all(self):
        """Closes all open files"""
        for i in xrange(self.count()):
            self.close_tab()

    def tab_seek_right(self):
        """Moves focus one tab to the right, back to start if at the end"""

        if self.currentIndex() == self.count() - 1:
            return self.setCurrentWidget(self.widget(0))

        else:
            widget_at_index = self.widget(self.currentIndex() + 1)
            return self.setCurrentWidget(widget_at_index)

    def tab_seek_left(self):
        """Moves focus one tab to the left, moves to end if at the start"""

        if self.currentIndex() == 0:
            return self.setCurrentWidget(self.widget(self.count() - 1))

        else:
            widget_at_index = self.widget(self.currentIndex() - 1)
            return self.setCurrentWidget(widget_at_index)

    def __repr__(self):
        return "PyCodeTabInterface"


class PyCodePage(QTextEdit):
    """Responsible for all signals and method-functions related ONLY to QTextEdit.
        I may make a class specifically for all QTextEdit related signal connections.
        Use the PyCodePage.Doc in order to access the current QTextDocument.
        

    """
    # TODO implement find, find_regexp, Open_folder
    def __init__(self, parent=None):
        super(PyCodePage, self).__init__(parent)
        self.TI = parent
        self.init_setup()
        self.textChanged.connect(self.modified_since_save)
        self.cursorPositionChanged.connect(self.column_line_update)


    def init_setup(self):
        """This defines the cursor color and width"""
        self.tmp_counter = 0
        self.setCursorWidth(5)
        self.setTabStopWidth(40)

    def modified_since_save(self):
        """Causes tab text to change if modified since last save"""
        #todo: find a better way to implement this...
        return self.TI.tabBar().setTabTextColor(
            self.TI.currentIndex(), QColor("#fff5ee"))

    # the tab width should be set elsewhere with a different, higher level method
    def set_tab_width(self, num):
        return self.setTabStopWidth(num)

    def column_line_update(self):
        """updates current cursor position in document"""
        return self.STATUS.line_count.setText("Line: %d, Column: %d" % (
            self.textCursor().blockNumber()+1, 
            self.textCursor().columnNumber()+1))

    def clone_line(self):
        """Clones current line cursor is found in"""
        self.copy_selection()
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.insertBlock()
        cursor.insertText(self.paste())
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    # TODO: have line_up/down SWAP block above/below respectively
    def line_up(self):
        """Moves current line block up one block level"""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.movePosition(QTextCursor.Up)
        cursor.insertText(cursor.selectedText())
        self.setTextCursor(cursor)
        cursor.removeSelectedText()
        # cursor.setKeepPositionOnInsert(True)
        self.setTextCursor(cursor)
        cursor.endEditBlock()
    
    def line_down(self):
        """Moves current line block down one level"""
        # need to make this a block swapping operation
        cursor = self.textCursor()

    def current_line_select(self):
        """Selects current line cursor is found in"""
        # shortcut for this will be Ctrl+L
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def delete_next_word(self):
        """deletes next word from cursor current position"""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.NoMove)
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def delete_previous_word(self):
        """deletes previous word from cursor current position"""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.PreviousWord)
        cursor.select(QTextCursor.WordUnderCursor)
        cursor.removeSelectedText()
        self.setTextCursor(cursor)
        cursor.endEditBlock()

    def delete_line(self):
        """Deletes current line cursor is found in"""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        
        if cursor.hasSelection():
            cursor.removeSelectedText()
        else:
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        cursor.endEditBlock()

    def kill_to_end_of_line(self):
        """kills text from cursor position to end of line"""
        cursor = self.textCursor()

        if not self.textCursor().atBlockEnd():
            cursor.movePosition(QTextCursor.NoMove)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
            self.cut()

    def delete_to_beginning(self):
        """Deletes text from current cursor position to start of current line"""
        cursor = self.textCursor()
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.NoMove)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.setTextCursor(cursor)
        cursor.endEditBlock()


    def paste_and_indent(self):
        """Paste from clipboard with indent"""
        # this is a temp fix
        self.insertPlainText("    ")
        self.paste()

    def paste_selection(self):
        """paste text from clipboard to tab page"""
        return self.paste()

    def undo_last(self):
        """Steps back in operation history"""
        return self.undo()

    def redo_last(self):
        """Steps forward in operation history"""
        return self.redo()

    def increase_font_size(self):
        """Incrementally increases font point size"""
        self.selectAll()
        currentF = self.currentCharFormat()
        currentF.setFontPointSize(currentF.fontPointSize()+ 1)
        self.setCurrentCharFormat(currentF)
        # this gets rid of the highlighting when increaseing font size
        # cursor = self.textCursor()
        # cursor.clearSelection()
        # self.setTextCursor(cursor)

    def decrease_font_size(self):
        """Incrementally decreases font point size"""
        self.selectAll()
        currentF = self.currentCharFormat()
        currentF.setFontPointSize(currentF.fontPointSize()- 1)
        if currentF.fontPointSize() > 0:
            return self.setCurrentCharFormat(currentF)
        else:
            pass

    def set_word_wrap(self):
        # does not work. After toggling
        # back on, it will not auto-wrap off-screen text
        off = QTextOption.NoWrap

        if self.wordWrapMode() != QTextOption.NoWrap:
            self.setWordWrapMode(QTextOption.NoWrap)
        else:
            self.setWordWrapMode(QTextOption.WordWrap)


    #testing zoom functions
    def zoom_in(self):
        return self.zoomIn()

    def zoom_out(self):
        return self.zoomOut()

    def set_serif(self):
        """Set all text to serif font family"""
        self.selectAll()
        currentF = self.currentCharFormat()
        currentF.setFontFamily("serif")
        self.setCurrentCharFormat(currentF)

    def set_monospace(self):
        """Set all text to monospace font family"""
        self.selectAll()
        currentF = self.currentCharFormat()
        currentF.setFontFamily("monospace")
        self.setCurrentCharFormat(currentF)

    def set_sansserif(self):
        """Set all text to sans-serif font family"""
        self.selectAll()
        currentF = self.currentCharFormat()
        currentF.setFontFamily("sans-serif")
        self.setCurrentCharFormat(currentF)

    def copy_selection(self):
        """Copies current text selection"""
        if self.textCursor().hasSelection():
            return self.copy()
        else:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
            self.copy()
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def cut_selection(self):
        """copy/cut selected text"""
        if self.textCursor().hasSelection():
            return self.cut()
        else:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            self.setTextCursor(cursor)
            return self.cut()



class PyCodeAction(QAction):
    """Reimplemented in order to override __repr__ special method. Besides that,
        there is no difference between this and the original QAction.
    """
    def __init__(self, name=None, text="default", parent=None):
        super(PyCodeAction, self).__init__(text, parent)
        self.name = name

    def __repr__(self):
        return self.name



class PyCodeStatusBar(QStatusBar):
    """ Responsible for individual statusbars' slots and signals"""
    def __init__(self, parent=None):
        super(PyCodeStatusBar, self).__init__(parent)
        self.showMessage("Ready", 4000)
        
        self.line_count = QLabel()
        self.current_syntax = QLabel()
        self.addPermanentWidget(self.line_count)
        self.addPermanentWidget(self.current_syntax)

    def __repr__(self):
        return "PyCodeStatusBar Instance"


class PyCodeMenu(QMenu):
    """ This Menu will hold all of the common functionality between 
        the pycode menus
        """
    def __init__(self, name="Default", parent=None):
        super(PyCodeMenu, self).__init__(parent)
        self.name = name
        self.ALL_ACTIONS = {}
        self.ACTION_GROUPS = {}
        self.setTitle(str(name))
        # this is here for testing purposes
        # these are used to establish connections between the triggermenu classes and 
        # the main tabinterface class methods...
        self.P_C, self.P_C_T = parent, parent
        
    def create_action(self, name=None, menutext=None, short=None, status=None):
        """Creates a new action and automatically adds it to itself"""
        self.ALL_ACTIONS[str(name)] = PyCodeAction(name, menutext, self)
        if short:
            self.ALL_ACTIONS.get(name).setShortcut(short)
        if status:
            self.ALL_ACTIONS.get(name).setStatusTip(status)
        self.addAction(self.ALL_ACTIONS.get(name))

    def create_action_group(self, name=None):
        self.ACTION_GROUPS[name] = QActionGroup(self)

    def add_to_action_group(self, name=None, actionname=None):
        actionname = self.ALL_ACTIONS.get(actionname)
        return self.ACTION_GROUPS.get(name).addAction(actionname)

    def update_dict(self, dict_name=None, dict_to_add=None):
        """Adds all actions to main dictionary
                   *dict_name* from the supplied *dict_to_add* arg.
                """
        if dict_name:
            dict_name = self.ALL_ACTIONS
            return dict_name.update(dict_to_add)

    def reset_all(self, dict_name=None, slot_name=None):
        """NOTE: this indentation begins with a tab, and then 4 spaces!
           This method is called in order to disconnect all *dict_name* actions
           from the *slot_name* arg.
        """
        for action in dict_name:
            try:
                action.disconnect(slot_name)
            except TypeError, AttributeError:
                # NOTE this errors occur in the trigger menu classes.
                # this is due to the signal *currentChange* of the PyCodeTabInterface class
                # being emitted when there are no open tabs; the act of opening a new tab in such 
                # a state raises another error that this is meant to catch...
                print "Error processed..."

    def __repr__(self):
        return self.name


class PyCodeDockWidget(QDockWidget):
    """This class holds the main window dock widget for pop-ups, i.e. search & replace, find
        etc.
    """
    
    def __init__(self, parent=None):
        super(PyCodeDockWidget, self).__init__(parent)

        self.user_input = QLineEdit(self)
        self.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.setFloating(False)
        self.setObjectName('Main Dock')
        self.setWidget(self.user_input)
        self.hide()

        self.user_input.returnPressed.connect(self.select_current_text)

    def select_current_text(self):
        """Selects text in find bar when enter is pressed"""
        self.user_input.setSelection(0, len(self.user_input.text()))


class PyCodeSettings(QSettings):
    """ Here the user specific settings are written and kept.
        These methods, and the methods defined in other classes *expect* to 
        see a tab interface class at **some** point. This is important to remember.
        The *read_settings* method has been moved to the OOPEdit module
        due to class dependency. 
    """

    def __init__(self, parent=None):
        super(PyCodeSettings, self).__init__(parent)
        self.settings = QSettings(QSettings.UserScope, 
                      "AD Engineering", "PyCode Text Editor")
        self.P = parent
        self.P_C = self.P

    def write_settings(self):
        """Writes the current user settings"""

        files = [self.P_C.tabText(i) for i in xrange(self.P_C.count())]
        
        self.settings.beginGroup("Main Window")
        
        # save opened tabs
        self.settings.beginWriteArray("files")
        for i in xrange(len(files)):
            self.settings.setArrayIndex(i)
            self.settings.setValue("filename", files[i] )
        self.settings.endArray()

        self.settings.setValue("Position", self.P.pos())
        self.settings.setValue("Size", self.P.size())
        self.settings.endGroup()




class PyCodeShortcuts(QObject):
    """Responsible for creating/holding all pycode Shortcuts
        Shortcut context needs to be set for instantiated objects.
       Also, do note that the Qt.Page_Down key does *not* register
       when pressed, this leaves tab switching broken.
       I used the QObject as placeholder without any real reason other than
       to inherit some basic QObject methods. e.g. parent.
    """

    def __init__(self, parent=None):
        super(PyCodeShortcuts, self).__init__(parent)
        self._ALL_SHORTCUTS = {}
        self.create_shortcut("move_right", "Ctrl+pgup", parent, True)
        self.create_shortcut("move_right2", "Ctrl+Tab", parent, True)
        self.create_shortcut("move_left", "Ctrl+pgdn", parent, True)
        self.create_shortcut("move_left2", "Ctrl+Shift+Tab", parent, True)
        self.create_shortcut("close_focused_win", "Ctrl+Shift+W", parent)
        self.create_shortcut("close_dock", "Esc", parent)
        self.create_shortcut("cut_act", "Ctrl+X", parent)
        # self.create_shortcut("delete_line", "Ctrl+K", parent, True)
        # self.create_shortcut("clone_line", "Ctrl+Shift+D", parent, True)
        


    def create_shortcut(self, name=None, short=None, parent=None, auto=False, ctxt=None):
        """Creates Shortcut
           For convience, the most likely to be used aspects of QShortcut
           are placed as optional args.
        """
        self._ALL_SHORTCUTS[str(name)] = QShortcut(short, parent)
        if auto:
            self._ALL_SHORTCUTS.get(name).setAutoRepeat(auto)
        if ctxt:
            self._ALL_SHORTCUTS.get(name).setContext(ctxt)
