#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2011 Luca Beltrame <einar@heavensinferno.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License, under
#   version 2 of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the
#   Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import time

try:
    from numpy import linspace
except ImportError:
    def linspace(start, stop, num=50):
        L = [0.0] * num
        nm1 = num - 1
        nm1inv = 1.0 / nm1
        for i in range(num):
            L[i] = nm1inv * (start*(nm1 - i) + stop*i)
        return L

import PyQt4.QtGui as QtGui
import PyKDE4.kdeui as kdeui
from PyKDE4.kio import KFile

import vlc
from ui_capturewidget import Ui_VideoWidget

class CaptureWidget(QtGui.QWidget, Ui_VideoWidget):

    def __init__(self, parent=None):

        super(CaptureWidget, self).__init__(parent)
        self.setupUi(self)

        self.screencaps_no = None
        self.destination = None
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = None

        # Set parameters of the file requesters
        self.destinationRequester.setMode(KFile.Mode(KFile.Directory))
        self.sourceRequester.setMode(KFile.Mode(KFile.File))

        self.captureButton.clicked.connect(self.do_capture)

    def do_capture(self):

        source = self.sourceRequester.url().toLocalFile()
        destination = self.destinationRequester.url()

        if self.capsInput.value() == 0:
            return

        self.screencaps_no = self.capsInput.value()

        if source.isEmpty():
            return

        if destination.isEmpty():
            return

        self.destination = unicode(destination.toLocalFile())
        self.media = self.instance.media_new(unicode(source))
        self.player.set_media(self.media)
        self.media.parse()

        self.player.set_xwindow(self.videoFrame.winId())
        self.take_screenshots()

    def take_screenshots(self):

        self.player.play()
        time.sleep(1) # FIXME: Without it it doesn't work, why?

        self.player.pause()
        self.player.set_position(0)

        intervals = linspace(0, 1, num=self.screencaps_no)

        for position in intervals:

            self.player.set_position(position)
            self.player.video_take_snapshot(0, self.destination, 0, 0)

        self.player.stop()


class CaptureDialog(kdeui.KDialog):

    def __init__(self, parent=None):
        super(CaptureDialog, self).__init__(parent)

        self.capturewidget = CaptureWidget()
        self.setMainWidget(self.capturewidget)
        self.setButtons(kdeui.KDialog.None)
