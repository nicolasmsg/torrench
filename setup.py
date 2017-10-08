#! /usr/bin/python3

import sys

try:
    from setuptools import setup
except ImportError:
        print("Missing package setuptools. Please install to continue\n(https://pypi.python.org/pypi/setuptools)")
        sys.exit('Exiting now!!')

DESCRIPTION = 'Command-line torrent search program for Windows, Linux and  MacOS'
LONG_DESCRIPTION = 'Please visit https://github.com/kryptxy/torrench for docs.'
VERSION = '1.0.54'

setup(
    name="torrench",
    version=VERSION,
    author="kryptxy",
    author_email="kryptxy@protonmail.com",
    description=(DESCRIPTION),
    license="GPL",
    url="https://github.com/kryptxy/torrench",
    packages=['torrench', 'torrench.modules','torrench.utilities', 'torrench.core'],
    install_requires=['beautifulsoup4','lxml','requests','tabulate','colorama', 'pyperclip'],
    long_description=(LONG_DESCRIPTION),
    entry_points={'console_scripts': ['torrench = torrench.__main__:main']},
    zip_safe=False,
    keywords=['torrents', 'thepiratebay', 'kickasstorrents', 'CLI', 'linuxtracker', 'distrowatch', 'skytorrents'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
)
