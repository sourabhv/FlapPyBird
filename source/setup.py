import os
import sys
from distutils.core import setup

import py2exe

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
    dlls = ("libfreetype-6.dll", "libogg-0.dll", "sdl_ttf.dll")
    if os.path.basename(pathname).lower() in dlls:
        return 0
    return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

sys.argv.append('py2exe')

setup(
    name =    'Flappy Bird',
    version = '1.0',
    author =  'Sourabh Verma',
    options = {
        'py2exe': {
            'bundle_files': 1, # doesn't work on win64
            'compressed': True,
        }
    },

    windows = [{
        'script': "flappy.py",
        'icon_resources': [
            (1, 'flappy.ico')
        ]
    }],

    zipfile=None,
)
