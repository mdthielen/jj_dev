#!/usr/bin/python
"""Maya initialization for Maya.env, userSetup.py, and pluginPrefs.mel for a new machine setup.

Used as a first step for a user to setup the Maya.env with python and mel script folders.
Setup the userSetup.py to be consistent on all machines.
Setup VRay plugin to be loaded.

Run from desktop:
    initialize_maya

Attributes:

Todo:

"""

import os


def main():
    # High level variables
    maya_prefs_path = os.path.expanduser('~/Library/Preferences/Autodesk/maya/2017/')
    maya_plugin_prefs_file = 'prefs/pluginPrefs.mel'
    maya_env_file = 'Maya.env'

    # VRay plugin
    vray_plugin_line = '\nevalDeferred("autoLoadPlugin(\\\"\\\", \\\"vrayformaya\\\", \\\"vrayformaya.bundle\\\")");'
    replaced_vray = fixLineInFile(maya_prefs_path + maya_plugin_prefs_file, 'vrayformaya', vray_plugin_line)
    if replaced_vray:
        print('Added VRay plugin')

    # Maya.env
    replaced_maya_env = maya_env(maya_prefs_path + maya_env_file, dev=True)
    if replaced_maya_env:
        print('Updated Maya.env')

    # userSetup.py
    replaced_usersetup_py = fixLineInFile(maya_prefs_path + 'scripts/userSetup.py', 'import maya.cmds as mc', 'import maya.cmds as mc')
    if replaced_usersetup_py:
        print('Updated userSetup.py')

    # userPrefs.mel
    replaced_userPrefs_mel = fixLineInFile(maya_prefs_path + 'prefs/userPrefs.mel', '"mayaBinary"', '"mayaAscii"', True)
    if replaced_userPrefs_mel:
        print('Updated userPrefs.mel  --> default mayaAscii save')
    replaced_userPrefs_mel = fixLineInFile(maya_prefs_path + 'prefs/userPrefs.mel', ' -sv "preferredRenderer" "', ' -sv "preferredRenderer" "vray"\n')
    if replaced_userPrefs_mel:
        print('Updated userPrefs.mel  --> default VRay renderer')


def maya_env(filepath, dev=False):
    """Edits the Maya.env file to have the latest PYTHONPATH, MAYA_SCRIPTS_PATH, and MAYA_SHELF_PATH

    Attributes:
        MAYA_SHELF_PATH = /Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/maya_shelves/lighting/
        SBTVTOOLS = /Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/
        PYTHONPATH = $SBTVTOOLS//maya_scripts/python:$SBTVTOOLS/maya_scripts/python/RnD
        MAYA_SCRIPT_PATH = $SBTVTOOLS/maya_scripts/mel

    Returns:
        True if file written
        False if error opening file

    Todo:

    """
    # quick parameter checks
    try:
        assert os.path.exists(filepath)
    except IOError, ioe:  # if something bad happened.
        print("ERROR", ioe)
        with open(filepath, 'w') as f:
            f.close()

    sbtvtools_var = 'SBTVTOOLS = '
    maya_script_path_var = 'MAYA_SCRIPT_PATH = '
    pythonpath_var = 'PYTHONPATH = '
    maya_shelf_path_var = 'MAYA_SHELF_PATH = '

    sbtvtools_path = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/'
    if not os.path.exists(sbtvtools_path):
        sbtvtools_path = os.path.expanduser('~/Documents/maya/scripts/JibJab/')
    if dev:
        sbtvtools_path = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/jj_dev/'
        if not os.path.exists(sbtvtools_path):
            sbtvtools_path = os.path.expanduser('~/Documents/maya/scripts/JibJab/jj_dev')
    if not os.path.exists(sbtvtools_path):
        os.makedirs(sbtvtools_path)
    maya_scripts_path = '$SBTVTOOLS/maya_scripts/mel'
    maya_shelf_path = '$SBTVTOOLS/maya_shelves/lighting/'
    pythonpath = '$SBTVTOOLS/maya_scripts/python:$SBTVTOOLS/maya_scripts/python/RnD'

    sbtvtools_replaced = False
    maya_script_path_replaced = False
    maya_shelf_path_replaced = False
    pythonpath_replaced = False

    try:
        with open(filepath, 'r') as f:    # open for read/write -- alias to f
            lines = f.readlines()            # get all lines in file
            f.close()  # we opened it , we close it
            lines_replaced = []

            for line in lines:
                # sbtvtools
                if line.startswith(sbtvtools_var):
                    lines_replaced.append(sbtvtools_var + sbtvtools_path + '\n')
                    sbtvtools_replaced = True
                # maya_script_path
                elif line.startswith(maya_script_path_var):
                    maya_script_path_old = line.split('=')[1].lstrip()
                    if ':' in maya_script_path_old:
                        paths_replaced = []
                        for path in maya_script_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                paths_replaced.append(maya_scripts_path)
                            else:
                                paths_replaced.append(path)
                        lines_replaced.append(maya_script_path_var + ':'.join(paths_replaced) + '\n')
                        maya_script_path_replaced = True
                    elif '$SBTVTOOLS' in maya_script_path_old:
                        lines_replaced.append(maya_script_path_var + maya_scripts_path + '\n')
                        maya_script_path_replaced = True
                    else:
                        lines_replaced.append(maya_script_path_var + maya_scripts_path + ':' +
                                              maya_script_path_old + '\n')
                        maya_script_path_replaced = True

                # maya_shelf_path
                elif line.startswith(maya_shelf_path_var):
                    maya_shelf_path_old = line.split('=')[1].lstrip()
                    if ':' in maya_shelf_path_old:
                        paths_replaced = []
                        for path in maya_shelf_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                paths_replaced.append(maya_shelf_path)
                            else:
                                paths_replaced.append(path)
                        lines_replaced.append(maya_shelf_path_var + ':'.join(paths_replaced))
                        maya_shelf_path_replaced = True
                    elif '$SBTVTOOLS' in maya_shelf_path_old:
                        lines_replaced.append(maya_shelf_path_var + maya_shelf_path + '\n')
                        maya_shelf_path_replaced = True
                    else:
                        lines_replaced.append(maya_shelf_path_var + maya_shelf_path + ':' +
                                              maya_shelf_path_old.rstrip() + '\n')
                        maya_shelf_path_replaced = True

                # pythonpath
                elif line.startswith(pythonpath_var):
                    pythonpath_old = line.split('=')[1].lstrip()
                    python_sbtvtools_replaced = False
                    if ':' in pythonpath_old:
                        paths_replaced = []

                        for path in pythonpath_old.split(':'):
                            if '$SBTVTOOLS' in path and not python_sbtvtools_replaced:
                                paths_replaced.append(pythonpath)
                                python_sbtvtools_replaced = True
                            elif '$SBTVTOOLS' not in path:
                                paths_replaced.append(path)
                            elif not python_sbtvtools_replaced:
                                paths_replaced.append(path)
                        lines_replaced.append(pythonpath_var + ':'.join(paths_replaced) + '\n')
                        pythonpath_replaced = True
                    elif '$SBTVTOOLS' in pythonpath_old:
                        lines_replaced.append(pythonpath_var + pythonpath + '\n')
                        pythonpath_replaced = True
                    else:
                        lines_replaced.append(pythonpath_var + pythonpath + ':' + pythonpath_old + '\n')
                        pythonpath_replaced = True

                # any other lines
                else:
                    lines_replaced.append(line)
            if not sbtvtools_replaced:
                lines_replaced.insert(0, sbtvtools_var + sbtvtools_path + '\n')
            if not maya_script_path_replaced:
                lines_replaced.insert(1, maya_script_path_var + maya_scripts_path + '\n')

            if not maya_shelf_path_replaced:
                lines_replaced.insert(2, maya_shelf_path_var + maya_shelf_path + '\n')

            if not pythonpath_replaced:
                lines_replaced.insert(3, pythonpath_var + pythonpath + '\n')

            with open(filepath, 'w') as f2:
                f2.writelines(lines_replaced)
                f2.close()
                return True

    except IOError, ioe:
        print("ERROR", ioe)
        return False


def fixLineInFile(filepath, line_keyword, newline, search_replace=False):
    """replace a line in a temporary file, then copy it over into the original file if everything goes well
    Attributes:
        filepath file to change
        line_keyword keyword to search
        newline new line to replace
    """

    # quick parameter checks
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.close()
    assert (line_keyword and str(line_keyword))  # is not empty and is a string
    assert (newline and str(newline))

    found_plugin = False
    written = False

    try:
        with open(filepath, 'r') as f:    # open for read/write -- alias to f
            lines = f.readlines()            # get all lines in file
            f.close()                          # we opened it , we close it
            lines_replaced = []
            for line in lines:
                if line_keyword in line:
                    if search_replace:
                        lines_replaced.append(line.replace(line_keyword, newline))
                        written = True
                    elif 'plugin' not in line_keyword:
                        lines_replaced.append(newline)
                        written = True
                        found_plugin = True
                    else:
                        found_plugin = True
                elif line.startswith('#'):
                    lines_replaced.append(line.rstrip() + '\n')
                else:
                    lines_replaced.append(line.rstrip() + '\n')
            if not found_plugin and not search_replace:
                lines_replaced.append(newline)
                written = True
            if written:
                with open(filepath, 'w') as f2:
                    f2.writelines(lines_replaced)
                    f2.close()
                return written

    except IOError, ioe:                 # if something bad happened.
        print("ERROR", ioe)
        return False

    return written        # replacement happened with no errors = True

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
