###########
# IMPORTS #
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QWidgetAction, QToolBar, QStyle, QFileDialog, QInputDialog, QLabel, QFrame, QDialog, QMessageBox, QTableWidget, QTableWidgetItem
from PySide6.QtGui import QIcon, QFont, QTextCursor, QBrush, QTextCharFormat, QColor, QDesktopServices
from PySide6.QtCore import QRegularExpression, Qt, QTimer, QUrl
from datetime import *
import platform
import locale
#---------------------------------------------------------------------------------------

#***************************************************************************************
#     _.._   .    .  ._   .   _.._   _____   _.._   _.._  .    .                       *
#    |´    )  \  /  |´ \  |  f    i | `|´ | |´     |´     |    |                       *
#    |___.´    y`   |  |  |  |    |    |    |__    |      |____|                       *
#    |´        |    |  |  |  |    |    |    |´     |      |´  `|                       *
#    i         i    i  L__J   \__/     i    L____  L____  i    i  by josrojrom1        *
#    ¡         :          !     :              ¡          .    :                       *
#              .          :                    .          !                            *
#    .                          .                         .                            *
#                                                                                      *
#                          .                    ¡                                      *
#                                                                                      *
#***************************************************************************************

#####################
# MAIN WINDOW CLASS #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ########################
        # MAIN WINDOW SETTINGS #
        self.resize(800, 500)
        self.initialTitle = "Untitled"
        self.setWindowTitle(self.initialTitle)
        self.current_path = None
        self.current_font_size = 14
        self.custom_font = QFont()
        self.custom_font.setPointSize(self.current_font_size)
        self.darkThemeStyle = '''QWidget{background-color: rgb(49,49,49);color: #FFFFFF;}QTextEdit{background-color: rgb(29,29,29);}QMenuBar::item:selected{color: #000000;}QMenu::item:selected{background-color: rgb(66,66,66);}'''
        self.recentlyOpen = False
        #---- ICONS, Uncoment and iterate for getting all posible icons
        #icons = sorted([attr for attr in dir(QStyle.StandardPixmap) if attr.startswith("SP_")])
        #------------------------- NEW ICON
        new_icon_path = getattr(QStyle, "SP_FileIcon")
        new_icon = self.style().standardIcon(new_icon_path)
        #------------------------- OPEN ICON
        open_icon_path = getattr(QStyle, "SP_DirClosedIcon")
        open_icon = self.style().standardIcon(open_icon_path)
        #------------------------- SAVE ICON
        save_icon_path = getattr(QStyle, "SP_DialogSaveButton")
        save_icon = self.style().standardIcon(save_icon_path)
        #------------------------- EXIT ICON
        exit_icon_path = getattr(QStyle, "SP_DialogCancelButton")
        exit_icon = self.style().standardIcon(exit_icon_path)
        #------------------------- APPEARANCE ICON
        appearance_icon_path = getattr(QStyle, "SP_DesktopIcon")
        appearance_icon = self.style().standardIcon(appearance_icon_path)
        #------------------------- UNDO ICON
        undo_icon_path = getattr(QStyle, "SP_MediaSeekBackward")
        self.undo_icon = self.style().standardIcon(undo_icon_path)    
        #------------------------- REDO ICON
        redo_icon_path = getattr(QStyle, "SP_MediaSeekForward")
        self.redo_icon = self.style().standardIcon(redo_icon_path)             
        #------------------------- UNDO WHITE ICON
        undo_icon_w_path = getattr(QStyle, "SP_ArrowBack")
        self.undo_icon_w = self.style().standardIcon(undo_icon_w_path)    
        #------------------------- REDO WHITE ICON
        redo_icon_w_path = getattr(QStyle, "SP_ArrowRight")
        self.redo_icon_w = self.style().standardIcon(redo_icon_w_path) 
        #------------------------- ABOUT ICON
        about_icon_path = getattr(QStyle, "SP_FileDialogInfoView")
        self.about_icon = self.style().standardIcon(about_icon_path) 
        #------------------------- SEARCH ICON
        search_icon_path = getattr(QStyle, "SP_FileDialogContentsView")
        search_icon = self.style().standardIcon(search_icon_path)
        #------------------------- SEARCH ICON
        selectAll_icon_path = getattr(QStyle, "SP_FileDialogDetailedView")
        selectAll_icon = self.style().standardIcon(selectAll_icon_path)
        #------------------------- CLEAN SEARCH ICON
        cleanSearch_icon_path = getattr(QStyle, "SP_DialogResetButton")
        cleanSearch_icon = self.style().standardIcon(cleanSearch_icon_path)   
        #------------------------- HELP ICON
        help_icon_path = getattr(QStyle, "SP_DialogHelpButton")
        help_icon = self.style().standardIcon(help_icon_path)  
        #---------------------------------------------------------------------------------------
        ##########################
        # MAIN WIDGET AND LAYOUT #
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        #---------------------------------------------------------------------------------------
        ########################
        # ADD WIDGETS FUNCTION #
        def add_widget(layout, widget):
            hbox = QHBoxLayout()
            hbox.addWidget(widget)
            layout.addLayout(hbox)
        #---------------------------------------------------------------------------------------
        ###############
        # TEXT EDITOR #
        self.text_edit = QTextEdit()
        self.text_edit.setViewportMargins(8, 6, 8, 8)
        self.text_edit.setFrameStyle(0)
        self.text_edit.setFont(self.custom_font)
        add_widget(main_layout, self.text_edit)
        self.text_edit.textChanged.connect(self.updateWindowTitle)
        #self.update_window_title
        #---------------------------------------------------------------------------------------
        ########################
        # BOTTON BAR WITH INFO #
        bottomLayout = QHBoxLayout()
        #---- DATE LABEL
        self.dateInfo = QLabel()
        #---- OS LABEL
        self.osTag = QLabel()
        #---- LANGUAJE LABEL
        self.langTag = QLabel()
        #---- UPDATE INFO CALL FUNCTION
        self.updateInfo()
        #---- ACTUAL HOVER INFO
        self.hoverInfo = QLabel()
        self.hoverInfo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        #---- SEPARATOR FOR TAGS
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.VLine)
        separator1.setFrameShadow(QFrame.Sunken)
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.VLine)
        separator2.setFrameShadow(QFrame.Sunken)
        #---- ADDING WIDGETS TO BOTTOM LAYOUT
        bottomLayout.addWidget(self.osTag)
        bottomLayout.addWidget(separator1)
        bottomLayout.addWidget(self.langTag)
        bottomLayout.addWidget(separator2)
        bottomLayout.addWidget(self.dateInfo)
        bottomLayout.addWidget(self.hoverInfo)
        bottomLayout.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottomLayout.setSpacing(15) 
        #---- ADDING BOTTOM LAYOUT TO MAIN LAYOUT
        main_layout.addLayout(bottomLayout)
        #---------------------------------------------------------------------------------------
        ###################################
        # DEFAULT MENU BAR OF QMainWindow #
        menuBar = self.menuBar()
        # ---------#
        # TOOL BAR #
        toolBar = QToolBar()
        toolBar.setMovable(False)
        self.addToolBar(toolBar)
        #---- TOOL BAR ACTIONS
        #------------------------- NEW ACTION
        self.new = QWidgetAction(self)  
        self.new.setIcon(new_icon)
        self.new.setShortcut("Ctrl+N")
        self.new.setIconText("New")
        #------------------------- OPEN ACTION
        self.open = QWidgetAction(self)
        self.open.setIcon(open_icon)
        self.open.setShortcut("Ctrl+O")
        self.open.setIconText("Open")
        #------------------------- SAVE ACTION
        self.save = QWidgetAction(self)
        self.save.setIcon(save_icon)
        self.save.setShortcut("Ctrl+S")
        self.save.setIconText("Save")
        #------------------------- SAVE AS ACTION
        self.saveAs = QWidgetAction(self)
        self.saveAs.setIcon(save_icon)
        self.saveAs.setShortcut("Ctrl+Shift+S")
        self.saveAs.setIconText("Save as...")
        #------------------------- EXIT ACTION
        self.exit = QWidgetAction(self)
        self.exit.setIcon(exit_icon)
        self.exit.setShortcut("Ctrl+Q")
        self.exit.setIconText("Exit")
        #------------------------- COPY ACTION
        self.copy = QWidgetAction(self)  
        self.copy.setIcon(QIcon("resources/icons/copy_icon.PNG"))
        self.copy.setShortcut("Ctrl+C")
        self.copy.setIconText("Copy")
        #------------------------- CUT ACTION
        self.cut = QWidgetAction(self)
        self.cut.setIcon(QIcon("resources/icons/cut_icon.PNG"))
        self.cut.setShortcut("Ctrl+X")
        self.cut.setIconText("Cut")
        #------------------------- PASTE ACTION
        self.paste = QWidgetAction(self)
        self.paste.setIcon(QIcon("resources/icons/paste_icon.PNG"))
        self.paste.setShortcut("Ctrl+V")
        self.paste.setIconText("Paste")
        #------------------------- SELECT ALL ACTION
        self.selectAll = QWidgetAction(self)
        self.selectAll.setIcon(selectAll_icon)
        self.selectAll.setShortcut("Ctrl+A")
        self.selectAll.setIconText("Select all")
        #------------------------- SEARCH ACTION
        self.search = QWidgetAction(self)
        self.search.setIcon(search_icon)
        self.search.setShortcut("Ctrl+F")
        self.search.setIconText("Search")
        #------------------------- CLEAN SEARCH ACTION
        self.cleanSearch = QWidgetAction(self)
        self.cleanSearch.setIcon(cleanSearch_icon)
        self.cleanSearch.setShortcut("Ctrl+B")
        self.cleanSearch.setIconText("Clean search")
        self.cleanSearch.setDisabled(True)
        #------------------------- UNDO ACTION
        self.undo = QWidgetAction(self)
        self.undo.setIcon(self.undo_icon)
        self.undo.setShortcut("Ctrl+Z")
        self.undo.setIconText("Undo")
        #------------------------- REDO ACTION
        self.redo = QWidgetAction(self)
        self.redo.setIcon(self.redo_icon)
        self.redo.setShortcut("Ctrl+Y")
        self.redo.setIconText("Redo")
        #------------------------- ZOOM IN ACTION
        self.zoomIn = QWidgetAction(self)
        self.zoomIn.setIcon(QIcon("resources/icons/zoomIn_icon.PNG"))
        self.zoomIn.setShortcut("Ctrl++")
        self.zoomIn.setIconText("Zoom In")
        #------------------------- ZOOM OUT ACTION
        self.zoomOut = QWidgetAction(self)
        self.zoomOut.setIcon(QIcon("resources/icons/zoomOut_icon.PNG"))
        self.zoomOut.setShortcut("Ctrl+-")
        self.zoomOut.setIconText("Zoom Out")
        #------------------------- APPEARANCE SELECT ACTION
        self.appearance = QWidgetAction(self)
        self.appearance.setIconText("Appearance")
        #------------------------- DARK THEME 
        self.darkTheme = QWidgetAction(self)
        self.darkTheme.setIconText("Dark mode")
        #------------------------- LIGHT THEME
        self.lightTheme = QWidgetAction(self)
        self.lightTheme.setIconText("Light mode")
        #------------------------- ABOUT ACTION
        self.about = QWidgetAction(self)
        self.about.setIcon(self.about_icon)
        self.about.setIconText("About")
        #------------------------- CONTRIBUTE ACTION
        self.contribute = QWidgetAction(self)
        self.contribute.setIcon(QIcon("resources/icons/github-mark.PNG"))
        self.contribute.setIconText("Contribute")
        #------------------------- MORE HELP ACTION
        self.moreHelp = QWidgetAction(self)
        self.moreHelp.setIcon(help_icon)
        self.moreHelp.setIconText("More help...")
        #---------------------------------------------------------------------------------------
        #---- TOOL BAR ADDED ACTIONS
        toolBar.addAction(self.new)
        toolBar.addAction(self.open)
        toolBar.addAction(self.save)
        toolBar.addSeparator()
        toolBar.addAction(self.search)
        toolBar.addAction(self.cleanSearch)
        #---- FILE MENU BAR OPTIONS  
        fileMenu = menuBar.addMenu('File')
        fileMenu.addAction(self.new)
        fileMenu.addAction(self.open)
        fileMenu.addAction(self.save)
        fileMenu.addAction(self.saveAs)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exit)
        #---- EDIT MENU BAR OPTIONS  
        editMenu = menuBar.addMenu('Edit')
        editMenu.addAction(self.copy)
        editMenu.addAction(self.cut)
        editMenu.addAction(self.paste)
        editMenu.addSeparator()
        editMenu.addAction(self.selectAll)
        editMenu.addAction(self.search)
        editMenu.addSeparator()
        editMenu.addAction(self.undo)
        editMenu.addAction(self.redo)
        #---- PREFERENCES MENU BAR OPTIONS  
        preferencesMenu = menuBar.addMenu('Preferences')
        preferencesMenu.addAction(self.zoomIn)
        preferencesMenu.addAction(self.zoomOut)
        #--------------- APPEARANCE SELECT OPTION
        self.appearance = preferencesMenu.addMenu('Appearance')
        self.appearance.setIcon(appearance_icon)
        self.appearance.addAction(self.darkTheme)
        self.appearance.addAction(self.lightTheme)
        #---- HELP MENU BAR OPTIONS  
        helpMenu = menuBar.addMenu('Help')
        helpMenu.addAction(self.about)
        helpMenu.addAction(self.contribute)
        helpMenu.addAction(self.moreHelp)
        #---------------------------------------------------------------------------------------
        ###############
        # CONNECTIONS #
        #---- File CONNECTIONS
        self.new.triggered.connect(self.newFile)
        self.open.triggered.connect(self.openFile)
        self.save.triggered.connect(self.saveFile)
        self.saveAs.triggered.connect(self.saveFileAs)
        self.exit.triggered.connect(self.checkUnsaveChanges)
        #---- Edit CONNECTIONS
        self.copy.triggered.connect(self.text_edit.copy)
        self.cut.triggered.connect(self.text_edit.cut)
        self.paste.triggered.connect(self.text_edit.paste)
        self.search.triggered.connect(self.searchAndHighlight)
        self.selectAll.triggered.connect(self.text_edit.selectAll)
        self.cleanSearch.triggered.connect(self.cleanSearchTerms)
        self.undo.triggered.connect(self.text_edit.undo)
        self.redo.triggered.connect(self.text_edit.redo)
        #---- Parameters CONNECTIONS
        self.zoomIn.triggered.connect(self.zoomInEditor)
        self.zoomOut.triggered.connect(self.zoomOutEditor)
        self.darkTheme.triggered.connect(self.setDarkTheme)
        self.lightTheme.triggered.connect(self.setLightTheme)
        #---- Help CONNECTIONS
        self.about.triggered.connect(self.showAbout)
        self.moreHelp.triggered.connect(self.showMoreHelp)
        self.contribute.triggered.connect(self.goGitRepo)
        #---------------------------------------------------------------------------------------
    #####################
    # NEW FILE FUNCTION #
    def newFile(self):
        self.text_edit.clear()
        self.setWindowTitle("Untitled")
        self.current_path = None
        self.text_edit.setFontPointSize(14)
    #---------------------------------------------------------------------------------------
    ######################
    # OPEN FILE FUNCTION #        
    def openFile(self):
        open_file = QFileDialog().getOpenFileName(self, 'Open file', 'Desktop','Text files (*.txt)')
        if open_file:
            self.recentlyOpen = True
            try:
                self.initialTitle = open_file[0]
                self.setWindowTitle(self.initialTitle)
                #self.setWindowTitle(open_file[0])
                with open(open_file[0], 'r') as f:
                    file_text = f.read()
                    self.text_edit.setPlainText(file_text)
                self.current_path = open_file[0]
                self.recentlyOpen = False
            except FileNotFoundError:
                print("File not found")
        else:
            print("No file selected")
    #---------------------------------------------------------------------------------------
    ######################
    # SAVE FILE FUNCTION #
    def saveFile(self):
        if self.current_path is not None:
            fileTextContent = self.text_edit.toPlainText()
            with open(self.current_path, 'w') as f:
                f.write(fileTextContent)
                self.initialTitle = str(self.current_path)
                self.setWindowTitle(self.initialTitle)
        else:
            self.saveFileAs()
    #---------------------------------------------------------------------------------------
    #########################
    # SAVE FILE AS FUNCTION #
    def saveFileAs(self):
        pathName = QFileDialog.getSaveFileName(self, 'Save file', '', 'Text files (*.txt)')
        fileTextContent = self.text_edit.toPlainText()
        with open(pathName[0], 'w') as f:
            f.write(fileTextContent)
        self.current_path = pathName[0]
        self.initialTitle = pathName[0]
        self.setWindowTitle(pathName[0])               
    #---------------------------------------------------------------------------------------
    ####################
    # ZOOM IN FUNCTION #
    def zoomInEditor(self):
        self.current_font_size += 1
        self.custom_font.setPointSize(self.current_font_size)
        self.text_edit.setFont(self.custom_font)
    #---------------------------------------------------------------------------------------
    #####################
    # ZOOM OUT FUNCTION #
    def zoomOutEditor(self):
        self.current_font_size -= 1
        self.custom_font.setPointSize(self.current_font_size)
        self.text_edit.setFont(self.custom_font)
    #---------------------------------------------------------------------------------------
    #####################
    # SEARCH FUNCTION #
    def searchAndHighlight(self):
        pattern, ok = QInputDialog.getText(self, "Search", "Enter your search term:")
        
        if ok:
            cursor = self.text_edit.textCursor()
            # FORMAT MATCHES COLORING #
            format = QTextCharFormat()
            format.setBackground(QBrush(QColor("yellow")))
            self.cleanSearch.setDisabled(False)
            # REGEX SETUP #
            re = QRegularExpression(pattern)
            # REGULAR EXPRESSION MATCH ITERATOR #
            i = re.globalMatch(self.text_edit.toPlainText())

            # ITERATE THROUGH ALL THE MATCHES AND HIGHLIGHT
            while i.hasNext():
                # REGULAR EXPRESSION MATCH
                match = i.next()

                # FORMATING OF MATCHED TEXT
                cursor.setPosition(match.capturedStart(), QTextCursor.MoveAnchor)
                cursor.setPosition(match.capturedEnd(), QTextCursor.KeepAnchor)
                cursor.mergeCharFormat(format)
    #---------------------------------------------------------------------------------------
    #################################
    # CLEAN MATCHES BEFORE SEARCHING#
    def cleanSearchTerms(self):
        cursor = self.text_edit.textCursor()
        cursor.select(QTextCursor.Document)
        format = QTextCharFormat()
        format.setFontUnderline(False)
        cursor.setCharFormat(format)
        self.text_edit.setFont(self.custom_font)
        self.cleanSearch.setDisabled(True)
    #---------------------------------------------------------------------------------------
    #######################
    # DARK THEME FUNCTION #
    def setDarkTheme(self):
        self.setStyleSheet(self.darkThemeStyle)
        self.zoomIn.setIcon(QIcon("resources/icons/zoomIn_icon_w.PNG"))
        self.zoomOut.setIcon(QIcon("resources/icons/zoomOut_icon_w.PNG"))
        self.copy.setIcon(QIcon("resources/icons/copy_icon_w.PNG"))
        self.cut.setIcon(QIcon("resources/icons/cut_icon_w.PNG"))
        self.paste.setIcon(QIcon("resources/icons/paste_icon_w.PNG"))
        self.contribute.setIcon(QIcon("resources/icons/github-mark-white.PNG"))
        self.undo.setIcon(self.undo_icon_w)
        self.redo.setIcon(self.redo_icon_w)
    #---------------------------------------------------------------------------------------
    ########################
    # LIGHT THEME FUNCTION #
    def setLightTheme(self):
        self.setStyleSheet("")
        self.zoomIn.setIcon(QIcon("resources/icons/zoomIn_icon.PNG"))
        self.zoomOut.setIcon(QIcon("resources/icons/zoomOut_icon.PNG"))
        self.copy.setIcon(QIcon("resources/icons/copy_icon.PNG"))
        self.cut.setIcon(QIcon("resources/icons/cut_icon.PNG"))
        self.paste.setIcon(QIcon("resources/icons/paste_icon.PNG"))
        self.contribute.setIcon(QIcon("resources/icons/github-mark.PNG"))
        self.undo.setIcon(self.undo_icon)
        self.redo.setIcon(self.redo_icon)
    #---------------------------------------------------------------------------------------
    ####################################
    # UPDATE BOTTOM LAYOUT DATA LABELS #
    def updateInfo(self):
            # DATE LABEL DATA
            self.dateInfo.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            self.timer = QTimer()
            self.timer.timeout.connect(self.updateInfo)
            self.timer.start(1000)
            # OS LABEL DATA
            system = platform.system()
            release = platform.release()
            self.osTag.setText(f"{system} {release}")
            # LANGUAJE LABEL DATA
            language, _ = locale.getlocale()
            self.langTag.setText(f"{language}")
    #---------------------------------------------------------------------------------------
    #################
    # ABOUT WINDOWN #
    def showAbout(self):
        dialog = QDialog()
        dialog.setWindowTitle("About")
        dialog.setWindowIcon(self.about_icon)
        dialog.setModal(True)
        dialog.setStyleSheet("background-color: rgb(175,210,255)")
        aboutFont = QFont()
        aboutFont.setPointSize(11)
        # ABOUT LABEL #
        label = QLabel("      pyNotech es un bloc de notas digital desarrollado como proyecto open source para\n"+
                        "el trabajo de fin de grado en Ingeniería Informática del Software por la Universidad de\n"+
                        "Sevilla (US). Utilizando PySide6 para Python, pyNotech es una aplicación de escritorio\n"+
                        "intuitiva y eficiente, desarrollada con el objetivo de aprender y establecer las bases del\n"+
                        "desarrollo de aplicaciones de escritorio.\n\n\n"
                        "Autor, José Joaquín Rojas Romero                                                 pyNotech v1.0.0-beta")
        # ABOUT LABEL STYLE #
        label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        label.setFont(aboutFont)
        label.setMargin(10)
        label.setStyleSheet("background-color: rgb(220,236,255);")#
        label.setFrameShape(QFrame.Panel)#
        label.setFrameShadow(QFrame.Sunken)#
        label.setLineWidth(2)#
        # LAYOUT #
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()
    #---------------------------------------------------------------------------------------
    ####################
    # MORE HELP WINDOW #
    def showMoreHelp(self):
        # MORE HELP DIALOG #
        dialog = QDialog()
        dialog.setWindowTitle("More help")
        dialog.setModal(True)
        dialog.setStyleSheet("background-color: rgb(175,210,255)")
        # TABLES CREATION #
        shortcutsTable1 = QTableWidget()
        shortcutsTable1.setColumnCount(2)    
        shortcutsTable1.setHorizontalHeaderLabels(["Shortcut", "Description"])
        shortcutsTable2 = QTableWidget()
        shortcutsTable2.setColumnCount(2)    
        shortcutsTable2.setHorizontalHeaderLabels(["Shortcut", "Description"])
        # DATA FOR TABLE 1 #
        shortcuts1 ={"New file": "Ctrl + N",
                    "Open file": "Ctrl + O",              
                    "Save file": "Ctrl + S",            
                    "Save file as": "Ctrl + Shift + S",     
                    "Exit": "Ctrl + Q",
                    "Zoom in": "Ctrl + +",             
                    "Zoom out": "Ctrl + -"}
        # DATA FOR TABLE 2 #
        shortcuts2 ={"Copy": "Ctrl + C",
                    "Cut": "Ctrl + X",
                    "Paste": "Ctrl + V",
                    "Search": "Ctrl + F",
                    "Select all": "Ctrl + A",
                    "Undo": "Ctrl + Z",
                    "Redo": "Ctrl + Y"}
        # SET ROWS #
        shortcutsTable1.setRowCount(len(shortcuts1))
        shortcutsTable2.setRowCount(len(shortcuts2))
        # TABLE 1 #
        for row, (description, shortcut) in enumerate(shortcuts1.items()):
            shortcutsTable1.setColumnWidth(1,154)
            shortcutsTable1.setItem(row, 0, QTableWidgetItem(description))
            shortcutsTable1.setItem(row, 1, QTableWidgetItem(shortcut))
        shortcutsTable1.verticalHeader().setVisible(False)  # Ocultar la cabecera vertical
        # TABLE 2 #
        for row, (description, shortcut) in enumerate(shortcuts2.items()):
            shortcutsTable2.setColumnWidth(1,154)
            shortcutsTable2.setItem(row, 0, QTableWidgetItem(description))
            shortcutsTable2.setItem(row, 1, QTableWidgetItem(shortcut))
        shortcutsTable2.verticalHeader().setVisible(False)  # Ocultar la cabecera vertical
        # TABLES STYLE #
        moreHelpFont = QFont()
        moreHelpFont.setPointSize(11)
        shortcutsTable1.setFont(moreHelpFont)
        shortcutsTable2.setFont(moreHelpFont)
        shortcutsTable1.setStyleSheet("background-color: rgb(220,236,255);")
        shortcutsTable2.setStyleSheet("background-color: rgb(220,236,255);")
        shortcutsTable1.setFrameShape(QFrame.Panel)
        shortcutsTable1.setFrameShadow(QFrame.Sunken)
        shortcutsTable1.setLineWidth(2)
        shortcutsTable2.setFrameShape(QFrame.Panel)
        shortcutsTable2.setFrameShadow(QFrame.Sunken)
        shortcutsTable2.setLineWidth(2)
        # CONTACT INFO LABEL #
        label = QLabel("Si usted encuentra algún problema con la aplicación puede ponerse en contacto\n"
                       "con nosotros mandando un email a la siguiente dirección de correo electrónico:\n\n\n"
                       "josrojrom1@alum.us.es")
        # CONTACT INFO STYLE #
        label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        label.setFont(moreHelpFont)
        label.setMargin(10)
        label.setStyleSheet("background-color: rgb(220,236,255);")
        label.setFrameShape(QFrame.Panel)
        label.setFrameShadow(QFrame.Sunken)
        label.setLineWidth(2)
        # LAYOUTS #
        layout = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutH.addWidget(shortcutsTable1)
        layoutH.addWidget(shortcutsTable2)
        layout.addLayout(layoutH)
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.exec()
    #---------------------------------------------------------------------------------------
    ################################################
    # CHECKING SAVE STATUS BEFORE EXITING FUNCTION #
    def checkUnsaveChanges(self):
        self.saved_changes = False
        if self.text_edit.toPlainText():
            reply = QMessageBox.question(self, 'Unsaved changes', '¿Do you want to save your changes before exiting?', QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            # WHEN SAVE IS PRESSED #
            if reply == QMessageBox.Save:
                self.saveFile()
                self.text_edit.setPlainText('')
                self.close()
            # WHEN DISCARD IS PRESSED #
            elif reply == QMessageBox.Discard:
                self.text_edit.setPlainText('')
                self.close()
            # WHEN CANCEL IS PRESSED #
            else:
                pass
        else:
            self.close()  
    #---------------------------------------------------------------------------------------
    ############################################
    # CHECKING "X" BUTTON FROM WINDOW FUNCTION #
    def closeEvent(self, event):
        if self.text_edit.toPlainText():
            self.checkUnsaveChanges()
            event.ignore()
        else:
            self.close
            event.accept()
    #---------------------------------------------------------------------------------------
    ##########################################
    # ADD MARK IN THE TITLE WHEN NEW CHANGES #
    def updateWindowTitle(self):
        if self.text_edit.textChanged and not self.recentlyOpen:
            self.setWindowTitle(f"{self.initialTitle} (*)")
        else:
            self.setWindowTitle(self.initialTitle)
    #---------------------------------------------------------------------------------------
    ############################
    # CONTRIBUTE LINK FUNCTION #
    def goGitRepo(self):
        url = QUrl("https://github.com/josrojrom1/pyNotech")
        QDesktopServices.openUrl(url)
    #---------------------------------------------------------------------------------------


########
# MAIN #
if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = MainWindow()
    notepad.show()
    sys.exit(app.exec())
