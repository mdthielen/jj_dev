#!/usr/bin/python

import os
import tempfile

def main():
    # High level variables
    maya_prefs_path = '/Users/trender/Library/Preferences/Autodesk/maya/2017/'
    maya_plugin_prefs_file = 'prefs/pluginPrefs.mel'
    maya_env_file = 'Maya.env'
    vray_plugin_line = 'evalDeferred("autoLoadPlugin(\\\"\\\", \\\"vrayformaya\\\", \\\"vrayformaya\\\")");'


    replace_line(maya_prefs_path + maya_plugin_prefs_file, vray_plugin_line, vray_plugin_line)

# defensive programming style
# function to replace a line in a file
# and not destroy data in case of error

def replace_line(filepath, oldline, newline ):
    """
    replace a line in a temporary file,
    then copy it over into the
    original file if everything goes well

    """

    # quick parameter checks
    assert os.path.exists(filepath)          # !
    assert ( oldline and str(oldline) ) # is not empty and is a string
    assert ( newline and str(newline) )

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
                print('Added VRay plugin')
                written = True

                # if replaced:  # overwrite the original file
                #     f.seek(0)  # beginning of file
                #     f.truncate()  # empties out original file
                #     print('writing file')
                #     for tmplines in tmpfile:
                #         print tmplines
                #         f.write(tmplines)  # writes each line to original file
                #     written = True

            else:
                tmpfile = tempfile.NamedTemporaryFile(delete=True)  # temp file opened for writing

                for line in lines:           # process each line
                    if line == oldline:        # find the line we want
                        tmpfile.write(newline)   # replace it
                        replaced = True
                    else:
                        tmpfile.write(oldline)   # write old line unchanged

                if replaced:                   # overwrite the original file
                    f.seek(0)                    # beginning of file
                    f.truncate()                 # empties out original file

                    for tmplines in tmpfile:
                        f.write(tmplines)          # writes each line to original file
                    written = True

            # tmpfile.close()              # tmpfile auto deleted
            f.close()                          # we opened it , we close it

    except IOError, ioe:                 # if something bad happened.
        printf ("ERROR" , ioe)
        f.close()
        return False

    return replaced and written        # replacement happened with no errors = True

main()
