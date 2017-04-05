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
    vray_plugin_line = 'evalDeferred("autoLoadPlugin(\\\"\\\", \\\"vrayformaya\\\", \\\"vrayformaya\\\")");'
    replaced_vray = fixLineInFile(maya_prefs_path + maya_plugin_prefs_file, 'vrayformaya', vray_plugin_line)
    if replaced_vray:
        print('Added VRay plugin')

    # dynamicShelf plugin
    dynamicShelf_plugin_line = 'evalDeferred("autoLoadPlugin(\\\"\\\", \\\"dynamicShelf.py\\\", \\\"dynamicShelf\\\")");'
    replaced_dynamicShelf = fixLineInFile(maya_prefs_path + maya_plugin_prefs_file, 'dynamicShelf', dynamicShelf_plugin_line)
    if replaced_dynamicShelf:
        print('Added dynamicShelf plugin')

    # Maya.env
    replaced_maya_env = maya_env(maya_prefs_path + maya_env_file, dev=True)
    if replaced_maya_env:
        print('Updated Maya.env')

    # userSetup.py
    replaced_usersetup_py = fixLineInFile(maya_prefs_path + 'scripts/userSetup.py', 'import maya.cmds as cmds', 'import maya.cmds as cmds')
    if replaced_usersetup_py:
        print('Updated userSetup.py')

    # userPrefs.mel
    replaced_userPrefs_mel = fixLineInFile(maya_prefs_path + 'prefs/userPrefs.mel', '"mayaBinary"', '"mayaAscii"', search_replace=True)
    if replaced_userPrefs_mel:
        print('Updated userPrefs.mel  --> default mayaAscii save')

    replaced_userPrefs_mel_vray = fixLineInFile(maya_prefs_path + 'prefs/userPrefs.mel', ' -sv "preferredRenderer" "', ' -sv "preferredRenderer" "vray"\n')
    if replaced_userPrefs_mel_vray:
        print('Updated userPrefs.mel  --> default VRay renderer')

    replaced_userPrefs_mel_quicktime = addAppPrefs(maya_prefs_path + 'prefs/userPrefs.mel', 'rvpush')
    if replaced_userPrefs_mel_quicktime:
        print('Updated userPrefs.mel  --> Quicktime player is RV and image editor is Photoshop')


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

    # REVIEW[mark] Test at studio
    # todo-mark add MAYA_RENDER_SETUP_GLOBAL_PRESETS_PATH to Maya.env

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
    dynamic_shelf_path_var = 'DYNAMIC_SHELF_PATH = '
    maya_shelf_path_var = 'MAYA_SHELF_PATH = '
    maya_plug_in_path_var = 'MAYA_PLUG_IN_PATH = '
    icons_path_var = 'ICONS_PATH = '

    sbtvtools_path = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools'
    if not os.path.exists(sbtvtools_path):
        sbtvtools_path = os.path.expanduser('~/Documents/maya/scripts/JibJab/')
    if dev:
        sbtvtools_path = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/jj_dev'
        if not os.path.exists(sbtvtools_path):
            if os.path.exists(os.path.expanduser('~/Documents/creating/projects/JibJab/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/jj_dev')):
                sbtvtools_path = os.path.expanduser('~/Documents/creating/projects/JibJab/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/jj_dev')
            elif os.path.exists(os.path.expanduser('~/Documents/maya/scripts/JibJab/jj_dev')):
                sbtvtools_path = os.path.expanduser('~/Documents/maya/scripts/JibJab/jj_dev')
    if not os.path.exists(sbtvtools_path):
        os.makedirs(sbtvtools_path)
    maya_scripts_path = '$SBTVTOOLS/maya_scripts/mel'
    dynamic_shelf_path = '$SBTVTOOLS/maya_shelves/dynamicShelves'
    python_path = '$SBTVTOOLS/maya_scripts/python'
    icons_path = '$SBTVTOOLS/maya_shelves/icons'
    maya_plug_in_path = '$SBTVTOOLS/maya_scripts/python/plug-ins'
    maya_shelf_path = ''

    sbtvtools_replaced = False
    maya_script_path_replaced = False
    dynamic_shelf_path_replaced = False
    maya_shelf_path_replaced = False
    icons_path_replaced = False
    maya_plug_in_path_replaced = False
    pythonpath_replaced = False

    try:
        with open(filepath, 'r') as f:  # open for read/write -- alias to f
            lines = f.readlines()  # get all lines in file
            f.close()  # we opened it , we close it
            lines_replaced = []
            sbtv_lines = []
            maya_lines = []
            python_lines = []
            jibjab_block_found = 0

            for line in lines:
                # sbtvtools
                if line.startswith(sbtvtools_var):
                    sbtv_lines.append(sbtvtools_var + sbtvtools_path + '\n')
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
                        maya_lines.append(maya_script_path_var + ':'.join(paths_replaced) + '\n')
                        maya_script_path_replaced = True
                    elif '$SBTVTOOLS' in maya_script_path_old:
                        maya_lines.append(maya_script_path_var + maya_scripts_path + '\n')
                        maya_script_path_replaced = True
                    else:
                        maya_lines.append(maya_script_path_var + maya_scripts_path + ':' +
                                          maya_script_path_old + '\n')
                        maya_script_path_replaced = True

                # dynamic_shelf_path_var
                elif line.startswith(dynamic_shelf_path_var):
                    dynamic_shelf_path_old = line.split('=')[1].lstrip()
                    if ':' in dynamic_shelf_path_old:
                        paths_replaced = []
                        for path in dynamic_shelf_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                paths_replaced.append(dynamic_shelf_path)
                            else:
                                paths_replaced.append(path)
                        maya_lines.append(dynamic_shelf_path_var + ':'.join(paths_replaced))
                        dynamic_shelf_path_replaced = True
                    elif '$SBTVTOOLS' in dynamic_shelf_path_old:
                        maya_lines.append(dynamic_shelf_path_var + dynamic_shelf_path + '\n')
                        dynamic_shelf_path_replaced = True
                    else:
                        maya_lines.append(dynamic_shelf_path_var + dynamic_shelf_path + ':' +
                                          dynamic_shelf_path_old.rstrip() + '\n')
                        dynamic_shelf_path_replaced = True

                # maya_shelf_path_var
                elif line.startswith(maya_shelf_path_var):
                    maya_shelf_path_old = line.split('=')[1].lstrip()
                    if ':' in maya_shelf_path_old:
                        paths_replaced = []
                        for path in maya_shelf_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                pass
                                # paths_replaced.append(dynamic_shelf_path)
                            else:
                                paths_replaced.append(path)
                        if paths_replaced:
                            maya_lines.append(maya_shelf_path_old + ':'.join(paths_replaced))
                        maya_shelf_path_replaced = True

                    elif '$SBTVTOOLS' in maya_shelf_path_old:
                        pass
                        # maya_lines.append(maya_shelf_path_var + maya_shelf_path_old + '\n')
                        maya_shelf_path_replaced = True
                    else:
                        maya_lines.append(maya_shelf_path_var + maya_shelf_path_old + ':' +
                                          maya_shelf_path_old.rstrip() + '\n')
                        maya_shelf_path_replaced = True

                # icons_path_var
                elif line.startswith(icons_path_var):
                    icons_path_old = line.split('=')[1].lstrip()
                    if ':' in icons_path_old:
                        paths_replaced = []
                        for path in icons_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                paths_replaced.append(icons_path)
                            else:
                                paths_replaced.append(path)
                        maya_lines.append(icons_path_var + ':'.join(paths_replaced))
                        icons_path_replaced = True
                    elif '$SBTVTOOLS' in icons_path_old:
                        maya_lines.append(icons_path_var + icons_path + '\n')
                        icons_path_replaced = True
                    else:
                        maya_lines.append(icons_path_var + icons_path + ':' +
                                          icons_path_old.rstrip() + '\n')
                        icons_path_replaced = True

                # maya_plug_in_path_var
                elif line.startswith(maya_plug_in_path_var):
                    maya_plug_in_path_old = line.split('=')[1].lstrip()
                    if ':' in maya_plug_in_path_old:
                        paths_replaced = []
                        for path in maya_plug_in_path_old.split(':'):
                            if '$SBTVTOOLS' in path:
                                paths_replaced.append(maya_plug_in_path)
                            else:
                                paths_replaced.append(path)
                        maya_lines.append(maya_plug_in_path_var + ':'.join(paths_replaced))
                        maya_plug_in_path_replaced = True
                    elif '$SBTVTOOLS' in maya_plug_in_path_old:
                        maya_lines.append(maya_plug_in_path_var + maya_plug_in_path + '\n')
                        maya_plug_in_path_replaced = True
                    else:
                        maya_lines.append(maya_plug_in_path_var + maya_plug_in_path + ':' +
                                          maya_plug_in_path_old.rstrip() + '\n')
                        maya_plug_in_path_replaced = True

                # python_path
                elif line.startswith(pythonpath_var):
                    pythonpath_old = line.split('=')[1].lstrip()
                    python_sbtvtools_replaced = False
                    if ':' in pythonpath_old:
                        paths_replaced = []

                        for path in pythonpath_old.split(':'):
                            if '$SBTVTOOLS' in path and not python_sbtvtools_replaced:
                                paths_replaced.append(python_path)
                                python_sbtvtools_replaced = True
                            elif '$SBTVTOOLS' not in path:
                                paths_replaced.append(path)
                            elif not python_sbtvtools_replaced:
                                paths_replaced.append(path)
                        python_lines.append(pythonpath_var + ':'.join(paths_replaced) + '\n')
                        pythonpath_replaced = True
                    elif '$SBTVTOOLS' in pythonpath_old:
                        python_lines.append(pythonpath_var + python_path + '\n')
                        pythonpath_replaced = True
                    else:
                        python_lines.append(pythonpath_var + python_path + ':' + pythonpath_old + '\n')
                        pythonpath_replaced = True
                elif line != '\n' and '=' not in line and not line.startswith('#'):
                    lines_replaced.append('# removed by maya_initialize --> {}'.format(line))
                elif line.startswith('#') and 'Jib Jab' in line:
                    jibjab_block_found += 1
                elif line == '\n' and jibjab_block_found <= 1:
                    pass

                # any other lines
                else:
                    lines_replaced.append(line)
            if not sbtvtools_replaced:
                if not sbtvtools_path.endswith('\n'):
                    sbtvtools_path += '\n'
                sbtv_lines.insert(0, sbtvtools_var + sbtvtools_path)
            if not maya_script_path_replaced:
                if not maya_scripts_path.endswith('\n'):
                    maya_scripts_path += '\n'
                maya_lines.insert(1, maya_script_path_var + maya_scripts_path)
            if not dynamic_shelf_path_replaced:
                if not dynamic_shelf_path.endswith('\n'):
                    dynamic_shelf_path += '\n'
                maya_lines.insert(2, dynamic_shelf_path_var + dynamic_shelf_path)
            if not icons_path_replaced:
                if not icons_path.endswith('\n'):
                    icons_path += '\n'
                maya_lines.insert(3, icons_path_var + icons_path + '')
            if not maya_plug_in_path_replaced:
                if not maya_plug_in_path.endswith('\n'):
                    maya_plug_in_path += '\n'
                maya_lines.insert(3, maya_plug_in_path_var + maya_plug_in_path + '')
            if not pythonpath_replaced:
                if not python_path.endswith('\n'):
                    python_path += '\n'
                python_lines.insert(5, pythonpath_var + python_path + '')
            if not maya_shelf_path_replaced and maya_shelf_path != '':
                if not maya_shelf_path.endswith('\n'):
                    maya_shelf_path += '\n'
                maya_lines.insert(6, maya_shelf_path_var + maya_shelf_path + '')

            with open(filepath, 'w') as f2:
                f2.writelines('## Jib Jab Studios - settings start\n\n')
                f2.writelines(sbtv_lines)
                # f2.writelines('\n')
                f2.writelines(maya_lines)
                # f2.writelines('\n')
                f2.writelines(python_lines)
                f2.writelines('\n## Jib Jab Studios - settings end\n')
                f2.writelines(lines_replaced)
                f2.close()

                with open(filepath, 'r') as f3:
                    lines_from_new_file = f3.readlines()
                    f3.close()
                    if lines == lines_from_new_file:
                        return False
                    else:
                        return True

    except IOError, ioe:
        print("ERROR", ioe)
        return False


def addAppPrefs(filepath, line_keyword):
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

    try:
        with open(filepath, 'r') as f:  # open for read/write -- alias to f
            lines = f.readlines()  # get all lines in file
            f.close()  # we opened it , we close it
            for line in lines:
                if line_keyword in line:
                    return False

            lines.append('optionVar\n')
            lines.append(' -sv "PhotoshopDir" "/Applications/Adobe Photoshop CC 2017/Adobe Photoshop CC 2017.app/Contents/MacOS/Adobe Photoshop CC 2017"\n')
            lines.append(' -sv "PlayblastCmdAvi" "/Applications/RV64.app/Contents/MacOS/rvpush"\n')
            lines.append(' -sv "PlayblastCmdFormatAvi" "-tag playblast merge [ %f.mov -fps %r ]"\n')
            lines.append(' -sv "PlayblastCmdQuicktime" "/Applications/RV64.app/Contents/MacOS/rvpush"\n')
            lines.append(' -sv "PlayblastCmdFormatQuicktime" "-tag playblast merge [ %f.mov -fps %r ]"\n')
            lines.append(' -sv "ViewSequenceDir" "/Applications/RV64.app/Contents/MacOS/rvpush"\n')
            lines.append(' -sv "ViewSequenceCmdFormat" "-tag playblast merge [ %f.mov -fps %r ]"\n')
            lines.append(' -sv "ViewImageDir" "/Applications/RV64.app/Contents/MacOS/rvpush"\n')
            lines.append(' -sv "ViewImageCmdFormat" "%f";\n')

            with open(filepath, 'w') as f2:
                f2.writelines(lines)
                f2.close()
            return True

    except IOError:
        pass


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
        with open(filepath, 'r') as f:  # open for read/write -- alias to f
            lines = f.readlines()  # get all lines in file
            f.close()  # we opened it , we close it
            lines_replaced = []
            for line in lines:
                if line_keyword in line:
                    if search_replace:
                        lines_replaced.append(line.replace(line_keyword, newline))
                        written = True
                    elif 'Plugin' in line:
                        if newline != line.rstrip('\n'):
                            lines_replaced.append(newline)
                            written = True
                        found_plugin = True
                    elif line == newline:
                        found_plugin = True
                elif line.startswith('#'):
                    lines_replaced.append(line.rstrip() + '\n')
                else:
                    lines_replaced.append(line.rstrip() + '\n')
            if not found_plugin and not search_replace:
                if lines_replaced:
                    if newline.startswith(' -sv '):
                        lines_replaced.append('optionVar\n')
                        lines_replaced.append('{};\n'.format(newline))
                        written = True
                    else:
                        lines_replaced.append(newline)
                        written = True
                else:
                    lines_replaced.append(newline)
                    written = True

            if written:
                with open(filepath, 'w') as f2:
                    f2.writelines(lines_replaced)
                    f2.close()
                return written

    except IOError, ioe:  # if something bad happened.
        print("ERROR", ioe)
        return False

    return written  # replacement happened with no errors = True


if __name__ == '__main__':
    main()

__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/6/2017"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
