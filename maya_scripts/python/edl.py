#!/usr/bin/python
"""
EDL file fixer

Attributes:


Todo:


"""


import os
from sys import argv


def rvEdl():
    """Modify RV edl.py
    Copies modified jj_mod_rv_edl.py to the rv app contents: /Applications/RV64.app/Contents/src/python/sgtk/bundle_cache/manual/tk-framework-editorial/v1.0.41/python/edl/edl.py
    Attributes:

    Returns:

    Todo:

    """
    
    import shutil
    import filecmp
    rv_edl = '/Applications/RV64.app/Contents/src/python/sgtk/bundle_cache/manual/tk-framework-editorial/v1.0.41/python/edl/edl.py'
    jj_mod_rv_edl = '/Volumes/public/StoryBots/production/series/ask_the_storybots/03_shared_assets/01_cg/05_maya_tools/jj_dev/maya_scripts/python/resources/jj_mod_rv_edl.py'

    try:
        assert os.path.exists(rv_edl)
    except IOError, ioe:
        print('ERROR: edl.py does not exist', ioe)
        print('Check if RV is installed')

    try:
        assert os.path.exists(jj_mod_rv_edl)
    except IOError, ioe:
        print('ERROR: jj_mod_rv_edl.py does not exist', ioe)

    if not filecmp.cmp(rv_edl, jj_mod_rv_edl):
        try:
            backups = [f for f in os.listdir(os.path.dirname(rv_edl)) if 'backup' in f]
            shutil.move(rv_edl, '{}.backup{:02d}'.format(rv_edl, len(backups)))
            shutil.copy(jj_mod_rv_edl, rv_edl)
            print('Modified RV edl.py successfully')
        except Exception, e:
            print('Exception: {}'.format(e))
            print('Error when copying modified edl.py file. Check file permissions.')


def edl(edl_file):
    """modify edl file
    takes edl file and adds a label
    Attributes:

    Returns:

    Todo:

    """

    # quick parameter checks
    try:
        assert os.path.exists(edl_file)
    except IOError, ioe:  # if something bad happened.
        print("ERROR", ioe)
        with open(edl_file, 'w') as f:
            f.close()

    try:
        with open(edl_file, 'r') as f:  # open for read/write -- alias to f
            lines = f.readlines()  # get all lines in file
            f.close()  # we opened it , we close it
            lines_replaced = []
            search_clip_name = '* FROM CLIP NAME: '
            search_bl = ' BL '

            for line in lines:
                if line.startswith(search_clip_name):
                    lines_replaced.append(line)
                    lines_replaced.append('* {}'.format(line.split(search_clip_name)[1]))
                elif search_bl in line:
                    lines_replaced.append(line.replace(search_bl, 'AX'))
                else:
                    lines_replaced.append(line)
        with open(edl_file, 'w') as f:  # open for read/write -- alias to f
            f.writelines(lines_replaced)
            f.close()

    except Exception, e:
        print('Error exception: {}'.format(e))


if __name__ == '__main__':
    if '-rv' == argv[1]:
        rvEdl()

    # edl_file = argv[1]
    # edl(edl_file)


__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "4/21/17"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
