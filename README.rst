KDE VLC Snapper
===============

KDE VLC Snapper is a small PyKDE4 based program to perform automated screencapping of DVD chapters or movie files.
It is based on the VLC Python bindings.

Requirements
------------

* Python (2.6 and 2.7 should work reliably)
* PyKDE4
* VLC 1.1.x
* ``dvdread`` and ``lsdvd`` (used for DVD chapter screencapping)
* numpy (optional)

Installation
------------

Untar the archive, and run::

    python setup.py install

as root. Supply the ``--prefix`` option if you want to install to a specific prefix (default ``/usr/local``).

Usage
-----

Simply select your media file or DVD chapter, set the number of required screencaps and the destination directory and click on *Capture*.

Known issues
------------

* Some media files make the program crash (hard to debug)

License
-------

This program is licensed under the GNU General Public License (GPL) version 2, or at your option, any later version.