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

import subprocess
import time

try:
    from numpy import linspace
except ImportError:
    def linspace(start, stop, num=50):
        L = [0.0] * num
        nm1 = num - 1
        nm1inv = 1.0 / nm1
        for i in range(num):
            L[i] = nm1inv * (start * (nm1 - i) + stop * i)
        return L

try:
    import lxml.etree as etree
except ImportError:
    from xml.etree import ElementTree as etree

import PyQt4.QtCore as QtCore
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
        self._is_dvd = False
        self._tracks = dict()

        # Set parameters of the file requesters
        self.destinationRequester.setMode(KFile.Mode(KFile.Directory))
        self.sourceRequester.setMode(KFile.Mode(KFile.File))

        self.captureButton.clicked.connect(self.do_capture)
        self.sourceComboBox.currentIndexChanged[QtCore.QString].connect(
            self.toggle_boxes)
        self.titleComboBox.currentIndexChanged[int].connect(self.scan_tracks)

    def toggle_boxes(self, text):

        if text == "File":
            self.titleComboBox.setEnabled(False)
            self.chapterComboBox.setEnabled(False)
            self._is_dvd = False
        elif text == "DVD":
            self.titleComboBox.setEnabled(True)
            self.chapterComboBox.setEnabled(True)
            self.sourceRequester.setEnabled(False)
            self._is_dvd = True
            self.scan_disc()

    def scan_disc(self):

        self.titleComboBox.clear()

        try:
            args = ["lsdvd", "-Ox", "-c"]
            command = subprocess.Popen(args, stdout=subprocess.PIPE)
        except OSError:
            self.chapterComboBox.addItem("N/A")
            self.titleComboBox.addItem("N/A")

        returncode = command.poll()

        if returncode == 2:
            self.chapterComboBox.addItem("N/A")
            self.titleComboBox.addItem("N/A")
            return

        data = etree.parse(command.stdout)
        data = data.getroot()

        template = "Title {0}"

        for element in data.iter("track"):
            track_id = element.xpath("ix")[0]
            self._tracks[int(track_id.text)] = list()

            name = template.forma(track_id.text)
            self.titleComboBox.addItem(name)

        for track in sorted(self._tracks):
            chapters = data.xpath("//track[ix=%d]/chapter"
                                        % track)
            for chapter in chapters:
                chapter_id = chapter[0].text
                self._tracks[track].append(chapter_id)

        self.scan_tracks(self.chapterComboBox.currentIndex())

    def scan_tracks(self, index):

        self.chapterComboBox.clear()

        if index == -1:
            index = 0

        index += 1

        template = "Chapter {0}"
        chapters = self._tracks[index]

        for chapter in chapters:
            name = template.format(chapter)
            self.chapterComboBox.addItem(name)

    def do_capture(self):

        if self._is_dvd:
            source_url = "dvd://@{0}:{1}"
            current_title = unicode(self.titleComboBox.currentText())
            current_title = current_title.split(" ")[1]

            current_track = unicode(self.chapterComboBox.currentText())
            current_track = current_track.split(" ")[1]
            source_url = source_url.format(current_title, current_track)
        else:
            source_url = self.sourceRequester.url()

            if not source_url.isLocalFile():
                source_url = source_url.toString()
            else:
                source_url = source_url.toLocalFile()

            if source_url.isEmpty():
                return

        destination = self.destinationRequester.url()

        if self.capsInput.value() == 0:
            return

        self.screencaps_no = self.capsInput.value()

        if destination.isEmpty():
            return

        self.destination = unicode(destination.toLocalFile())
        self.media = self.instance.media_new(unicode(source_url))
        self.player.set_media(self.media)
        #self.media.parse()

        self.player.set_xwindow(self.videoFrame.winId())
        self.take_screenshots()


    def take_screenshots(self):

        self.player.play()
        time.sleep(1)  # FIXME: Port to VLC event handling

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
