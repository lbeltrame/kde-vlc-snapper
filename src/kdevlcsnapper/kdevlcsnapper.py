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


import sys

from PyKDE4.kdecore import KAboutData, ki18n, KCmdLineArgs
from PyKDE4.kdeui import KApplication

import capturewidget

def main():

    app_name="vlc_snapper"
    catalog = "danbooru_client"
    program_name = ki18n("KDE VLC Snapper")
    version = "0.1"
    description = ki18n("A screenshot taker for video clips.")
    license = KAboutData.License_GPL
    copyright = ki18n("(C) 2011 Luca Beltrame")
    text = ki18n("")
    home_page = "http://www.dennogumi.org"
    bug_email = "einar@heavensinferno.net"

    about_data = KAboutData(app_name, catalog, program_name, version,
                            description, license, copyright, text, home_page,
                            bug_email)

    about_data.setProgramIconName("internet-web-browser")

    KCmdLineArgs.init(sys.argv, about_data)
    app = KApplication()
    dialog = capturewidget.CaptureDialog()
    dialog.show()

    app.lastWindowClosed.connect (dialog.deleteLater)
    app.exec_()

