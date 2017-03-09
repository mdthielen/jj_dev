#!/usr/bin/python
"""
Publish file
Publish animation or lighting file for shot.

Attributes:
    
    
Todo:
    * Document more
    
"""

# todo-mark test and clean

import os
import re
import maya.cmds as cmds


def pubName(currentFile):  # = cmds.file(q=1, l=1)[0] ):
    """
    Publish Name
        :param currentFile: mayaAscii file of currently opened file even if the file is not saved
        :return: pubFile    currentfilePUBLISH.ma  --> current file name, stripped of version and append PUBLISH.ma

    """
    ver = '_?\d+.ma$'  # version syntax, in this case, to search for '###.ma'
    pubFile = re.split(ver, currentFile)[0]  # remove version suffix
    pubFile += r'PUBLISH.ma'  # add PUBLISH suffix
    return pubFile


def publish(currentFile, exportOnly=False):  # = cmds.file(q=1, l=1)[0]:
    """
    publish current file
    :param currentFile: currently opened file, even new untitled file
    :param exportOnly: export only, no saving of current file
    :return: pubFile  --> name of published file
    """
    pubFile = pubName(currentFile)
    # export all as a .ma file, overwrite if existing.
    # cmds.file( rename = pubFile)
    if not exportOnly:
        # save the current file
        cmds.file(save=True, force=True)
        print('Saved %s' % currentFile)
    try:
        cmds.file(pubFile, force=1, options="v=0;", type="mayaAscii", pr=1, ea=1)
    except IOError:
        print('FAILED TO EXPORT\n%s' % pubFile)
        return
    print('\n*Exported: \n    %s \n\n' % pubFile.split('\\')[-1])  # only works on windows, returns long name on others
    return pubFile


def replaceCharRigs(currentFile):  # = cmds.file(q=1, l=1)[0]):
    """
    ** Deprecated **
    replace mental ray rigs with vray rigs
    :param currentFile: currently open file
    """
    pubFile = pubName(currentFile)
    print('Replacing rigs... \n    %s' % pubFile.split('/')[-1])
    characters = ['Bing', 'Bing', 'Bang', 'Beep', 'Bo', 'Boop']
    molephiusRig = 'Molepheus.ma'
    if '_animation' in pubFile:
        fileContents = readMA(pubFile)
        for i in range(len(fileContents)):
            if '_Rig.ma' in fileContents[i]:
                if len(fileContents[i]) < 250:
                    print('%s' % fileContents[i])
                for char in characters:
                    fileContents[i] = fileContents[i].replace(char + '_Rig.ma', char + '_Rig_Vray.ma')
                if len(fileContents[i]) < 255:
                    print('%s\n' % fileContents[i])
            elif molephiusRig in fileContents[i]:
                if len(fileContents[i]) < 250:
                    print('%s' % fileContents[i])
                fileContents[i] = fileContents[i].replace(molephiusRig, 'Molepheus_Vray.ma')
                if len(fileContents[i]) < 255:
                    print('%s\n' % fileContents[i])
        mayaFile = open(pubFile, 'w')
        mayaFile.writelines(fileContents)
        mayaFile.close()
    else:
        print 'please run from a versioned animation file'


def readMA(maFile):
    """
    Read all lines of mayaAscii file
    :param maFile: mayaAscii file
    :return: fileContents of the mayaAscii file read in as lines
    """
    mayaFile = open(maFile, 'r')
    fileContents = mayaFile.readlines()  # .splitlines()
    mayaFile.close()
    return fileContents


def writeMA(maFile, fileContents):
    """
    Write lines to a specified mayaAscii file
    :param maFile: mayaAscii file to write
    :param fileContents: lines to write
    """
    mayaFile = open(maFile, 'w')
    mayaFile.writelines(fileContents)
    mayaFile.close()


def findPUBLISH(sourcePath):
    """
    Find publish file that ends with PUBLISH.ma in sourcePath
    :param sourcePath: path to search for publish file
    :return: srcPub[0] is the publish file name
    """
    srcPub = [f for f in os.listdir(sourcePath) if 'PUBLISH.ma' in f]
    if len(srcPub) < 1:
        import sys
        sys.exit('No publish file present. \n  Check for a \'PUBLISH\' file in:\n  %s' % sourcePath)
    elif len(srcPub) > 1:
        import sys
        sys.exit('More than one publish file present. \n  Clean up directory:\n  %s' % sourcePath)
    else:
        return srcPub[0]


def importRef(sourcePath):
    """
    Import references in publish file of a given sourcePath
    :param sourcePath: path of publish file to import references
    """
    # REVIEW[mark] This method is not being used.
    srcPub = findPUBLISH(sourcePath)
    # print 'srcPub:\n  ', srcPub
    srcPubFP = os.path.join(sourcePath, srcPub)
    # print 'srcPubFP:\n  ', srcPubFP
    # return
    if os.path.isfile(srcPubFP):
        print '\nImporting reference from...\n    ', srcPubFP
        cmds.file(srcPubFP, mergeNamespacesOnClash=1, reference=1, namespace=':')  # todo-maek this is not the correct import command
    else:
        raise NameError('could not find:\n    ' + srcPubFP)

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
