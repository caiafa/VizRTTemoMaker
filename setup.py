import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

exe = [Executable(
    script='temoMaker.py',
    base=base,
    icon="Temo1.ico",
    compress=True,
    copyDependentFiles=True,
    appendScriptToExe=False,
    appendScriptToLibrary=False,
)]

setup(name='TEMO Maker',
      version='0.3',
      description='TEMO Maker',
      options=options,
      executables=exe,
      requires=['PIL', 'PyQt5', 'cx_Freeze']
      )
