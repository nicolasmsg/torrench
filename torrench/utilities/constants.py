import os


TORRENCH_SETTINGS = dict(auto_envvar_prefix='TORRENCH')

CMD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                          'modules'))
PRIVATE_CMD_FOLDER = os.path.join(CMD_FOLDER, 'privates') 