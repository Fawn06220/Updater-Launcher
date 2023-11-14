from distutils.core import setup
import sys, py2exe, os

sys.argv.append('py2exe')

setup(
    windows = [{'script': "Updater_Launcher_ENG.py",
               "icon_resources": [(1, "logo_g.ico")]
               }
              ],
    )
