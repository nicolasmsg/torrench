#! /usr/bin/env python3

import platform
import os
import sys
import logging
import logging.config
import torrench.Torrench as Torrench
import torrench.utilities.logger as logger

logging.config.dictConfig(logger.LOG_SETTINGS)
mylogger = logging.getLogger('log1')

if platform.system() == 'Windows':
    from multiprocessing import Queue
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 3)
    # Expand windows console window so output does not overlap (font==default).
    os.system("mode 800")

system = platform.platform()
pyversion = sys.version
arch = platform.machine()

def main():
    """Execution begins here."""
    mylogger.debug(system)
    mylogger.debug(arch)
    mylogger.debug(pyversion)
    mylogger.debug("Torrench started.")
    Torrench.main()


if __name__ == "__main__":
    main()
