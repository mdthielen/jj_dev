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

# todo-mark repath textures
# todo-mark add fuctionality to run from within Maya


def processMaya(mafile):
    """
    Process mayaAscii files removing PRMan, Turtle renderers.
    
    :param mafile: file
    """

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

        rman_found = False
        turtle_found = False
        createnode_found = False

        for line in lines:
            if re.search(requires_rman, line):
                rman_found = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            elif rman_found and ';' not in line:
                rman_found = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            elif rman_found and ';' in line:
                rman_found = False
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.split(' ')[0].strip('"').strip('\n'))
            elif re.search(requires_turtle, line) and ';' not in line:
                turtle_found = True
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.strip('"').strip('\n'))
            elif turtle_found and ';' in line:
                turtle_found = False
                for node in line.split(' -nodeType '):
                    if '"' in node:
                        del_types.append(node.split(' ')[0].strip('"').strip('\n'))
            elif 'requires "stereoCamera"' in line:
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
        with open('{}_edit.ma'.format(mafile.split('.ma')[0]), 'w') as o:
            o.writelines(keep_lines)


def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        processMaya(filename)

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
