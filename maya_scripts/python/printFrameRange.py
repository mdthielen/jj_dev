#!/usr/bin/python
"""
Print frame range
Print the frame range of a specified mayaAscii file.

Attributes:
    printFrameRange.py <mayaAscii_file>.ma
    
Todo:
    
    
"""

import sys

text = 'playbackOptions'


def readFile(ma_file):
    """
    Read in mayaAscii file lines
    :param ma_file: mayaAscii file
    :return: ma_contents of mayaAscii file
    """
    f = open(ma_file, 'r')
    ma_contents = f.readlines()
    f.close()

    return ma_contents


def findContents(fileContents, search_text):
    """
    Find given text (playbackOptions) in mayaAscii file
    :param fileContents: mayaAscii file contents
    :param search_text: 'playbackOptions'
    :return: line  --> playbackOptions line
    """
    for line in fileContents:
        if search_text in line:
            return line


if __name__ == '__main__':
    file_contents = readFile(sys.argv[1])
    line = findContents(file_contents, text)
    # print line
    index = 0
    print sys.argv[1]
    if line:
        for element in line.split(' '):
            if 'ast' in element:
                start = line.split(' ')[index + 1]
                print('Start frame: {}'.format(start))
            if 'aet' in element:
                end = line.split(' ')[index + 1]
                print('End frame:   {}'.format(end))
            index += 1


__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
