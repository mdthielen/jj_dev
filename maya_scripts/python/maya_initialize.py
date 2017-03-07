#!/usr/bin/python
"""Maya initialization for Maya.env, userSetup.py, and pluginPrefs.mel for a new machine setup.

Used as a first step for a user to setup the Maya.env with python and mel script folders.
Setup the userSetup.py to be consistent on all machines.
Setup VRay plugin to be loaded.

Run from desktop:
    initialize_maya

Attributes:

Todo:
    * setup Maya.env
    * setup userSetup.py
    * setup pluginPrefs.mel

"""

import os
import tempfile


def main():
    # High level variables
    maya_prefs_path = os.path.expanduser('~/Library/Preferences/Autodesk/maya/2017/')
    maya_plugin_prefs_file = 'prefs/pluginPrefs.mel'
    maya_env_file = 'Maya.env'

    # VRay plugin
    vray_plugin_line = 'evalDeferred("autoLoadPlugin(\\\"\\\", \\\"vrayformaya\\\", \\\"vrayformaya\\\")");'
    replaced_vray = replace_line(maya_prefs_path + maya_plugin_prefs_file, vray_plugin_line, vray_plugin_line)
    if replaced_vray:
        print('Added VRay plugin')

    # Maya.env
    pythonpath = ''
    maya_scripts_path = ''
    replaced_maya_env = replace_line(maya_prefs_path + maya_env_file, 'PYTHONPATH', pythonpath)


def maya_env(maya_env_file):
    """Edits the Maya.env file to have the latest PYTHONPATH, MAYA_SCRIPTS_PATH, and MAYA_SHELF_PATH

    Attributes:
        MAYA_SHELF_PATH = /Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/maya_shelves/lighting/
        SBTVTOOLS = /Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/
        PYTHONPATH = $SBTVTOOLS/jj_dev/maya_scripts/python:$SBTVTOOLS/jj_dev/maya_scripts/python/RnD
        MAYA_SCRIPT_PATH = $SBTVTOOLS/jj_dev/maya_scripts/mel

    Returns:

    Todo:

    """
    # quick parameter checks
    assert os.path.exists(filepath)

    replaced = False
    written  = False

    maya_shelf_path = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/maya_shelves/lighting/'
    sbtvtools = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/'
    pythonpath = '$SBTVTOOLS/jj_dev/maya_scripts/python:$SBTVTOOLS/jj_dev/maya_scripts/python/RnD'
    maya_scripts_path = '$SBTVTOOLS/jj_dev/maya_scripts/mel'

    try:
        with open(filepath, 'r+') as f:    # open for read/write -- alias to f
            lines = f.readlines()            # get all lines in file
            # TODO - check for existing variables in Maya.env
            # TODO - check if existing path matches correct path
            # TODO - leave any paths that are user defined and don't overlap studio paths
            # TODO - put in a dev flag

    except IOError, ioe:                 # if something bad happened.
        printf ("ERROR" , ioe)
        f.close()
        return False


def replace_line(filepath, oldline, newline ):
    """replace a line in a temporary file, then copy it over into the original file if everything goes well
    Attributes:
        filepath file to change
        oldline old line to replace
        newline new line to replace
    """

    # quick parameter checks
    assert os.path.exists(filepath)
    assert (oldline and str(oldline)) # is not empty and is a string
    assert (newline and str(newline))

    replaced = False
    written  = False

    try:

        with open(filepath, 'r+') as f:    # open for read/write -- alias to f

            lines = f.readlines()            # get all lines in file

            if oldline not in lines:
                # tmpfile = tempfile.NamedTemporaryFile(delete=True)  # temp file opened for writing
                #
                # for line in lines:  # process each line
                #     tmpfile.write(oldline)  # write old line unchanged
                # tmpfile.write(newline)  # replace it
                # replaced = True
                f.writelines(newline)
                written = True

                # if replaced:  # overwrite the original file
                #     f.seek(0)  # beginning of file
                #     f.truncate()  # empties out original file
                #     print('writing file')
                #     for tmplines in tmpfile:
                #         print tmplines
                #         f.write(tmplines)  # writes each line to original file
                #     written = True

            # else:
            #     tmpfile = tempfile.NamedTemporaryFile(delete=True)  # temp file opened for writing
            #
            #     for line in lines:           # process each line
            #         if line == oldline:        # find the line we want
            #             tmpfile.write(newline)   # replace it
            #             replaced = True
            #         else:
            #             tmpfile.write(oldline)   # write old line unchanged
            #
            #     if replaced:                   # overwrite the original file
            #         f.seek(0)                    # beginning of file
            #         f.truncate()                 # empties out original file
            #
            #         for tmplines in tmpfile:
            #             f.write(tmplines)          # writes each line to original file
            #         written = True
            #
            #     tmpfile.close()              # tmpfile auto deleted
            f.close()                          # we opened it , we close it

    except IOError, ioe:                 # if something bad happened.
        printf ("ERROR" , ioe)
        f.close()
        return False

    return replaced and written        # replacement happened with no errors = True

if __name__ == '__main__':
    main()

__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
