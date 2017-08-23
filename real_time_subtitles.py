#!/usr/bin/env python
#
# Copyright (c) 2017 Jukka Ylitalo
# forked from pyqt examples: http://www.qtrac.eu/pyqtbook.html
# pyqtbook27\pyqt\chap11\counters.py
# Copyright (c) 2008-14 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.


from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

import re

from PyQt5.QtCore import (QRectF, QPoint,QSize, Qt,QRect)
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtGui import (QKeySequence,QFontMetrics)
from PyQt5.QtWidgets import (QApplication, QColorDialog, QErrorMessage, QSizePolicy, QWidget,QLabel,QVBoxLayout,QMainWindow,QAction,QDialog,QMessageBox,QCheckBox,QSpinBox,QDialogButtonBox,QGridLayout, QFileDialog)

from timelogging import logtime



logginfil = "loggingtimes_log"
labelStyle="QLabel {font-size: 40px;padding: 3px 5px 10px 30px;background-color: #ddd; color:black}"
previewlabelStyle="QLabel {font-size: 28px;padding: 2px 2px 2px 4px;background-color: #ddd; color:black}"


def saveAFileAppend(tnimi, contents):
    fo = open(tnimi  , "a")
    fo.write( contents);
    # Close opend file
    fo.close()

def lataa_tied(tiednimi):
    """ Load a file
    :param tiednimi:
    :return:
    """
    readfil = open(tiednimi, 'r')
    html_doc = readfil.read()
    readfil.close()
    return html_doc



previous_tail_len = 4
upcoming_len = 4
messagemaxlen=60

def splitMessageToLines(message2,messagemaxlen):
    message2list=[]
    #if len(message2) > 120:
    if len(message2) > messagemaxlen:
        while len(message2) > messagemaxlen:
            #for i in range(10):
            try:
                indx=message2[:messagemaxlen].rindex(" ")
            except ValueError:
                indx = messagemaxlen

            if indx < 2:
                indx = messagemaxlen

            message2[:indx]
            message2list.append(message2[:indx])
            message2=message2[indx:]

        message2list.append(message2)

        message2 = "<br>".join( message2list)
    return message2




class LineIndexDialog(QDialog):

    def __init__(self, lineIndx, parent=None):
        super(LineIndexDialog, self).__init__(parent)
        self.create_widgets(lineIndx)
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle(self.tr("Jump to line"))

    def create_widgets(self,lineIndx):
        self.lineIndxLabel = QLabel(self.tr("&lineIndx:"))
        self.lineIndxSpinBox = QSpinBox()
        self.lineIndxLabel.setBuddy(self.lineIndxSpinBox)
        self.lineIndxSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.lineIndxSpinBox.setRange(0, 20000)
        self.lineIndxSpinBox.setValue(lineIndx)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)


    def layout_widgets(self):
        layout = QGridLayout()
        layout.addWidget(self.lineIndxLabel, 0, 0)
        layout.addWidget(self.lineIndxSpinBox, 0, 1)
        layout.addWidget(self.buttonBox, 1, 0, 1, 2)
        self.setLayout(layout)

    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        #self.lineIndxSpinBox.valueChanged.connect(self.updateUi)

class SubtitleLabelSettings(QDialog):

    def __init__(self, xpos,ypos, width, height,fontsize, parent=None):
        super(SubtitleLabelSettings, self).__init__(parent)
        self.create_widgets(xpos,ypos,width, height, fontsize)
        self.layout_widgets()
        self.create_connections()
        self.setWindowTitle(self.tr("Subtitle size, position"))

    def registerSubtitleLabel(self,subtitleLabel):
        #self.mainwin = mainwin
        self.subtitleLabel = subtitleLabel

    def create_widgets(self,xpos,ypos, width, height,fontsize):
        self.widthLabel = QLabel(self.tr("&Width:"))
        self.widthSpinBox = QSpinBox()
        self.widthLabel.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.widthSpinBox.setRange(10, 2000)
        self.widthSpinBox.setValue(width)
        self.heightLabel = QLabel(self.tr("&Height:"))
        self.heightSpinBox = QSpinBox()
        self.heightLabel.setBuddy(self.heightSpinBox)
        self.heightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.heightSpinBox.setRange(10, 2000)
        self.heightSpinBox.setValue(height)

        self.xposLabel = QLabel(self.tr("&xPos:"))
        self.xposSpinBox = QSpinBox()
        self.xposLabel.setBuddy(self.xposSpinBox)
        self.xposSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.xposSpinBox.setRange(-2000, 2000)
        self.xposSpinBox.setValue(xpos)

        self.yposLabel = QLabel(self.tr("&yPos:"))
        self.yposSpinBox = QSpinBox()
        self.yposLabel.setBuddy(self.yposSpinBox)
        self.yposSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.yposSpinBox.setRange(-2000, 2000)
        self.yposSpinBox.setValue(ypos)

        self.fontSizeLabel = QLabel(self.tr("&Font Size:"))
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeLabel.setBuddy(self.fontSizeSpinBox)
        self.fontSizeSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.fontSizeSpinBox.setRange(-2000, 2000)
        self.fontSizeSpinBox.setValue(fontsize)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|
                                          QDialogButtonBox.Cancel)


    def layout_widgets(self):
        layout = QGridLayout()
        layout.addWidget(self.widthLabel, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(self.heightLabel, 1, 0)
        layout.addWidget(self.heightSpinBox, 1, 1)

        layout.addWidget(self.xposLabel, 2, 0)
        layout.addWidget(self.xposSpinBox, 2, 1)
        layout.addWidget(self.yposLabel, 3, 0)
        layout.addWidget(self.yposSpinBox, 3, 1)

        layout.addWidget(self.fontSizeLabel, 4, 0)
        layout.addWidget(self.fontSizeSpinBox, 4, 1)

        layout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.setLayout(layout)


    def create_connections(self):
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.xposSpinBox.valueChanged.connect(self.updateUi)
        self.yposSpinBox.valueChanged.connect(self.updateUi)
        self.widthSpinBox.valueChanged.connect(self.updateUi)
        self.heightSpinBox.valueChanged.connect(self.updateUi)


    def updateUi(self):
        labelxpos=self.xposSpinBox.value()
        #print(labelxpos), type(labelxpos)
        global label
        label.move(QPoint(labelxpos, self.yposSpinBox.value()))
        label.setFixedWidth( self.widthSpinBox.value())
        label.setFixedHeight( self.heightSpinBox.value())


    def result(self):
        return self.xposSpinBox.value(), self.yposSpinBox.value(), self.widthSpinBox.value(), self.heightSpinBox.value()


class MainWindow(QMainWindow):
    def __init__(self,):
        super(MainWindow, self).__init__()
        self.form = SubTitlePreviewWidget()
        self.setWindowTitle("Real Time Subtitles Preview View")
        self.setCentralWidget(self.form)
        self.createActions()
        self.createMenus()
        self.form.tekstiilist = []
        self.errorLabel = QLabel()
        self.errorMessageDialog = QErrorMessage(self)
        initialColor = Qt.gray
        self.paintColor = initialColor
        #form.move(QPoint(0, 10))

    def open(self):
        print ("open file")
        self.default_filespath = r"e:\sl\su"
        options = QFileDialog.Options()

        #fname = unicode(QFileDialog.getOpenFileName(self,
        fname = QFileDialog.getOpenFileName(self, "Select Subtitle File", self.default_filespath )
        print(fname)
        if type((1,2)) == type(fname) and len(fname) > 1:
            fname =fname[0]

        if fname == '':
            return

        try:
            texti = lataa_tied(  fname )
       # texti = lataa_tied('"' + fname + '"')

        except:
            self.errorMessageDialog.showMessage("File named " + fname + " could not be opened.")
            self.errorLabel.setText("If the box is unchecked, the message won't "
                                    "appear again.")
            return

        tekstii = texti.decode("utf8")

        if len(re.findall(r'\r[^\n]', tekstii)) > len(re.findall(r'\r\n', tekstii)):
            self.form.tekstiilist = tekstii.split("\r")

        elif len(re.findall(r'\r\n', tekstii)) > len(tekstii) / 70:
            self.form.tekstiilist = tekstii.split("\r\n")
        else:
            self.form.tekstiilist = tekstii.split("\n")

        self.form.lineindex = 0
        self.form.fileTitleText = [row for row in self.form.tekstiilist[:10] if row.strip() != ''][0]
        self.form.updateControlView("init")
        saveAFileAppend(logginfil, "Opening: " + fname[:15].decode("utf-8") + "\n")

    def jumpToIndex(self):
        print ("goto index")
        dlg = LineIndexDialog(self.form.lineindex)
        # dlg.registerSubtitleLabel(self.form.label)
        dlg.exec_()
        self.form.lineindex = dlg.lineIndxSpinBox.value()
        self.form.updateControlView("jump")

    def about(self):
        #self.infoLabel.setText("Invoked <b>Help|About</b>")
        QMessageBox.about(self, "About Menu",
                          "<b>Real Time Subtitles</b> is for subtitling a live event. "
                          "Choose file and start subtitling.")

    def aboutQt(self):
        self.infoLabel.setText("Invoked <b>Help|About Qt</b>")

    def openSettings(self):
        print("settings")
        global  messagemaxlen
        #self.subtitleLabelSize
        xpos,ypos,width, height = self.subtitleLabelPos[0], self.subtitleLabelPos[1], self.subtitleLabelSize[0], self.subtitleLabelSize[1]
        fontsize = self.subtitleFontSize
        dlg = SubtitleLabelSettings(xpos,ypos,width, height,fontsize)
        #dlg.registerSubtitleLabel(self.form.label)
        dlg.exec_()
        self.subtitleLabelPos = dlg.xposSpinBox.value() , dlg.yposSpinBox.value()
        self.subtitleLabelSize = dlg.widthSpinBox.value() , dlg.heightSpinBox.value()
        self.subtitleFontSize = dlg.fontSizeSpinBox.value()
        print ("SubtitleFontSize " + str( self.subtitleFontSize))
        #labelStyle="QLabel {font-size: 58px;padding: 0px 5px 10px 70px;background-color: #ddd; color:black}"

        labelStyle2= re.sub(r'font\-size: \d\dpx',"font-size: " + str(self.subtitleFontSize) + "px",labelStyle)
        self.form.outputLabel.setStyleSheet(labelStyle2)
        aveg_char_w =  self.form.outputLabel.fontMetrics().averageCharWidth()
        messagemaxlen=int(self.subtitleLabelSize[0] / aveg_char_w) -10
        #messagemaxlen3=messagemaxlen2
        #print("label pos, size ", x,y,w,h )

    def viewsubtitleLabelToggle(self):
        print ("toggle subtitles view")
        if self.subtitleLabelVisible:
            self.form.outputLabel.hide()
            self.subtitleLabelVisible = False
        else:
            self.form.outputLabel.show()
            self.subtitleLabelVisible = True

    def setlabelColor(self):
        global labelStyle
        self.paintColor
        self.paintColor = QColorDialog.getColor(self.paintColor)
        newColor2 = self.paintColor.name()
        #labelStyle = "QLabel {font-size: 40px;padding: 10px 5px 10px 40px;background-color: #ddd; color:black}"
        labelStyle = re.sub(r'background-color: #\w+;','background-color: ' + newColor2 + ';',labelStyle )
        self.form.outputLabel.setStyleSheet(labelStyle)


    def createActions(self):
        self.openAct = QAction("&Open subtitles", self,
                               shortcut=QKeySequence.Open,
                               statusTip="Open a taglisting", triggered=self.open)


        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application", triggered=self.close)

        self.jumpToIndexAct = QAction("&Jump To Index", self,
                                      shortcut=QKeySequence("Ctrl+J"),
                                      statusTip="Jump to index", triggered=self.jumpToIndex)

        self.viewsubtitleLabelToggleAct = QAction("&Toggle subtitle label", self,
                                      shortcut=QKeySequence("Ctrl+T"),
                                      statusTip="Toggle subtitle label", triggered=self.viewsubtitleLabelToggle)

        self.setlabelColorAct = QAction("&Subtitles Background Color", self,
                                      shortcut=QKeySequence("Ctrl+B"),
                                      statusTip="Subtitles Background Color", triggered=self.setlabelColor)


        self.settingsAct = QAction("&Settings", self,
                                   shortcut=QKeySequence("Ctrl+Alt+E"),
                                   statusTip="Settings", triggered=self.openSettings)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)



    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.settingsAct)
        self.editMenu.addAction(self.jumpToIndexAct)
        self.editMenu = self.menuBar().addMenu("&View")
        self.editMenu.addAction(self.viewsubtitleLabelToggleAct)
        self.editMenu.addAction(self.setlabelColorAct)


        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        # self.helpMenu.addAction(self.aboutQtAct)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.form.updateControlView("prev")
            #print("left")

        elif event.key() == Qt.Key_Right:
            #print("right")
            self.form.updateControlView("next")

class SubTitlePreviewWidget(QWidget):

    def __init__(self, parent=None):
        super(SubTitlePreviewWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))

        self.outputLabel = None
        self.infolabel = QLabel()
        self.infolabel.setMaximumHeight(20)
        self.lineindex = 0
        self.infolabel.setText("line " + str(self.lineindex))
        self.label = QLabel()
        self.label.setStyleSheet(previewlabelStyle);
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.infolabel)
        self.setLayout(vbox)
        #self.setMinimumSize(self.minimumSizeHint())

    def initialize(self):
        pass
        #self.updateControlView("init")

    def textScroll(self,linindx):
        linindx_tailstart = linindx - previous_tail_len
        linindx_upcoming_end = linindx + upcoming_len
        if linindx_tailstart < 0:
            linindx_tailstart = 0

        if linindx_upcoming_end > len(self.tekstiilist) - 1:
            linindx_upcoming_end = len(self.tekstiilist) - 1

        message1 = "<br>\n".join(self.tekstiilist[linindx_tailstart:linindx]) + "<br>\n"
        message2 = self.tekstiilist[linindx] + "<br>\n"
        message3 = "<br>\n".join(self.tekstiilist[linindx + 1:linindx_upcoming_end]) + "<br>\n"
        messagePreviewMaxlen = 110
        message1 = splitMessageToLines(message1, messagePreviewMaxlen )
        message2 = splitMessageToLines(message2,messagemaxlen)
        message3 = splitMessageToLines(message3,messagePreviewMaxlen)

        return message1, message2, message3
    def updateOutlabel(self,   labelmessage):
        self.outputLabel.setText("<p>{0}</p>".format(labelmessage))
        self.outputLabel.fontMetrics()

    def registerLabel(self,label):
        self.outputLabel = label
    #
    # def sizeHint(self):
    #     return QSize(1800, 900)
    #
    # def minimumSizeHint(self):
    #     return QSize(1800, 800)

    def updateControlView(self, direction):
        if direction == "prev":
            self.lineindex -=1
            if self.lineindex < 0:
                self.lineindex = 0
        elif direction == "next" :
            self.lineindex +=1
            if self.lineindex > len(self.tekstiilist)-1:
                self.lineindex = len(self.tekstiilist)-1
        #elif direction == "jump":

        message1, message2, message3 = self.textScroll(self.lineindex)
        self.label.setText(
            "<p>{0}</p><p><b>{1}</b></p><p>{2}</p>".format(
                message1, message2, message3))
        self.updateOutlabel( message2)
        self.infolabel.setText("line " + str(1+self.lineindex) +
                               " / " + str(len(self.tekstiilist)) + "    " + self.fileTitleText )

        logtime(logginfil, direction, self.lineindex)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        print("jee")

    #    fil = sys.argv[1]
    app = QApplication(sys.argv)
    subtitleLabelIntialPos= (20,800)
    subtitleLabelInitialSize= (1760,160)

    desktop=app.desktop()
    firstscreengeom=desktop.screenGeometry(0)
    firstscreengeom

    if desktop.screenCount() > 1:
        secondscreen_geom= desktop.availableGeometry(1)
        secondscreen_geom.getCoords()
        print(secondscreen_geom.getCoords())
        # subtitleLabelIntialPos= (20,secondscreen_geom.getCoords()[1]+180)
        subtitleLabelIntialPos= (secondscreen_geom.getCoords()[0]+20,secondscreen_geom.getCoords()[3]-180)
        subtitleLabelInitialSize= (desktop.screenGeometry(1).getCoords()[2]-20,160)
    else:
        subtitleLabelIntialPos= (desktop.screenGeometry().getCoords()[0]+20,desktop.screenGeometry().getCoords()[3]-180)
        subtitleLabelInitialSize=desktop.screenGeometry().getCoords()[2]-40,160
    global label
    label = QLabel()

    window = MainWindow()
    window.form.registerLabel(label)
    window.form.initialize()
    window.subtitleLabelPos = subtitleLabelIntialPos
    window.subtitleLabelSize = subtitleLabelInitialSize
    window.subtitleFontSize= 40

    label.setWindowFlags(label.windowFlags() |Qt.CustomizeWindowHint |
                         Qt.SplashScreen | Qt.WindowStaysOnTopHint)
    # label.setWindowFlags(Qt.WindowStaysOnTopHint)
    label.setFixedWidth(subtitleLabelInitialSize[0])
    label.setFixedHeight(subtitleLabelInitialSize[1])

    label.setStyleSheet(labelStyle)
    label.fontMetrics()
    label.move(QPoint(subtitleLabelIntialPos[0], subtitleLabelIntialPos[1]))
    #label.move(QPoint(-1360, 700))
    label.show()
    window.subtitleLabelVisible = True

    # window.setGeometry(20, 20, firstscreengeom.getCoords()[2]-40, firstscreengeom.getCoords()[3]-40)
    # window.setGeometry(20, 20, firstscreengeom.getCoords()[2]-40, firstscreengeom.getCoords()[3]-40)
    window.form.setMinimumSize(QSize(firstscreengeom.getCoords()[2]-40, firstscreengeom.getCoords()[3]-80))
    window.form.setMaximumHeight(  firstscreengeom.getCoords()[3]-110)
    window.show()
    app.exec_()

