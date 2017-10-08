import os
import sys
from .constants import CMD_FOLDER, PRIVATE_CMD_FOLDER

cmd_map = {}


def list_commands():
    rv = []
    global cmd_map
    cmd_map = {}

    for filename in os.listdir(CMD_FOLDER):
        if filename.endswith('.py') and filename.startswith('cmd_'):
            mod = __import__('torrench.modules.' + filename[:-3], 
                    None, None, ['CMD_NAME'])
            rv.append(mod.CMD_NAME)
            cmd_map[mod.CMD_NAME] = filename[:-3]
    rv.sort()
    return rv

def get_command(name):
    list_commands()
    mod = None
    try:
        if sys.version_info[0] == 2:
            name = name.encode('ascii', 'replace')
        try:
            mod = __import__('torrench.modules.' + cmd_map[name],
                            None, None, ['cli'])
        except FileNotFoundError:
            mod = __import__('torrench.modules.privates.' + cmd_map[name],
                None, None, ['cli'])
    except ImportError as ex:
        return
    return mod.cli