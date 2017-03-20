#!/usr/bin/python
"""
Ingest maya files from external sources such as contractors and remove any plugins or fix paths.
Read in maya file.
Search for RenderMan or Turtle "requires" statements. (multiple lines - ends with ;)
If any exist:   search for createNode with those renderers and remove. (multiple lines)
                search for connectAttr with those renderers and remove. (single line)

Attributes:
    
    
Todo:
    * repath textures
    * add fuctionality to run from within Maya
    
"""

import sys

# REVIEW[mark] Test at studio
# todo-mark repath textures
# todo-mark add fuctionality to run from within Maya


def fileDialogRemoveRenderers():
    """
    Launch maya filebrowser within a Maya session to run removeRenderers(mafile) on.
    
    """
    import maya.cmds as cmds
    mafile = cmds.fileDialog2(fileMode=1, fileFilter='*.ma')[0]
    print('Search for renderers to remove in:\n{}'.format(mafile))
    removeRenderers(mafile)


def removeRenderers(mafile):
    """
    Process mayaAscii files removing PRMan, Turtle, mentalray renderers.
    
    :param mafile: file
    """

    print('\nJib Jab - removeRenderers:')
    with open(mafile, 'r') as f:
        lines = f.readlines()
        f.close()
    if lines:
        import re

        keep_lines = []
        del_types = []
        createnode_names = []

        requires_rman = r"requires.*RenderMan"
        requires_turtle = r"ilr"
        requires_mentalray = r"mentalray"

        rman_found = False
        turtle_found = False
        mentalray_found = False
        createnode_found = False
        file_edit = False

        for line in lines:
            # PRMan
            if re.search(requires_rman, line):
                rman_found = True
                file_edit = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            # PRMan
            elif rman_found and ';' not in line:
                rman_found = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            # PRMan
            elif rman_found and ';' in line:
                rman_found = False
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.split(' ')[0].strip('"').strip('\n'))
            # Turtle
            elif re.search(requires_turtle, line) and ';' not in line:
                turtle_found = True
                file_edit = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            # Turtle
            elif turtle_found and ';' in line:
                turtle_found = False
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.split(' ')[0].strip('"').strip('\n'))
            # mentalray
            elif re.search(requires_mentalray, line) and ';' not in line:
                mentalray_found = True
                file_edit = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            # mentalray
            elif mentalray_found and ';' not in line:
                mentalray_found = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            # mentalray
            elif mentalray_found and ';' in line:
                mentalray_found = False
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.split(' ')[0].strip('"').strip('\n'))
            elif 'requires "stereoCamera"' in line:
                file_edit = True
                continue
            elif line.startswith('createNode') and [node for node in del_types if node in line]:
                createnode_found = True
                createnode_names.append(line.split('"')[1])
            elif createnode_found and line.startswith('	'):
                continue
            elif createnode_found and line.startswith('lockNode'):
                createnode_found = False
            elif createnode_found and line.startswith('createNode'):
                createnode_found = False
                keep_lines.append(line)
            elif line.startswith('connectAttr') and [name for name in createnode_names if name in line]:
                continue
            else:
                keep_lines.append(line)
        if file_edit:
            import shutil
            import os

            if os.path.exists('{}.ingestBackup000'.format(mafile)):
                ingest_backup_files = [f for f in os.listdir(os.path.dirname(mafile)) if 'ingestBackup' in f]
                shutil.copy(mafile, '{}.ingestBackup{:03d}'.format(mafile, len(ingest_backup_files)))
                print('Backup made to:\n{}.ingestBackup{:03d}'.format(mafile, len(ingest_backup_files)))
            else:
                shutil.copy(mafile, '{}.ingestBackup000'.format(mafile))
                print('Backup made to:\n{}.ingestBackup000'.format(mafile))
            with open('{}.ma'.format(mafile.split('.ma')[0]), 'w') as o:
                o.writelines(keep_lines)
                o.close()
                print('Original file is fixed:\n{}'.format(mafile))
        else:
            print('No changes made.')

    print('\nJib Jab - removeRenderers COMPLETE')


def main():
    if len(sys.argv) > 1:
        import os
        filename = sys.argv[1]
        removeRenderers(os.path.abspath(filename))

if __name__ == '__main__':
    main()

__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/13/17"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
