#!/usr/bin/python
"""
Publish file
Publish animation or lighting file for shot.

Attributes:
    
    
Todo:
    
"""

import os
import re
import maya.cmds as cmds
import maya.mel
# from xml.dom import minidom


def pubName(currentFile):  # = cmds.file(q=1, l=1)[0] ):
    """
    Publish Name
        :param currentFile: mayaAscii file of currently opened file even if the file is not saved
        :return: pubFile    currentfilePUBLISH.ma  --> current file name, stripped of version and append PUBLISH.ma

    """
    ver = '_?\d+.ma$'  # version syntax, in this case, to search for '###.ma'
    pubFile = re.split(ver, currentFile)[0]  # remove version suffix
    pubFile += r'_PUBLISH.ma'  # add PUBLISH suffix
    return pubFile


def publish(currentFile=None, saveCurrentFile=False):
    """
    publish current file
    used on lightingTools shelf, labeled as pub  --> pipelineTools.publish()
    :param currentFile: currently opened file, even new untitled file
    :param saveCurrentFile: export only, no saving of current file
    :return: pubFile  --> name of published file
    """
    if not currentFile:
        if cmds.file(q=1, sn=1):
            currentFile = cmds.file(q=1, l=1)[0]
        else:
            cmds.warning('Save current file before publishing.')
            return

    pubFile = pubName(currentFile)

    if saveCurrentFile:
        # save the current file
        cmds.file(save=True, force=True)
        print('Saved %s' % currentFile)

    try:
        if os.path.exists(os.path.dirname(pubFile)):
            if os.path.exists(pubFile):
                if os.access(pubFile, os.W_OK):
                    cmds.file(pubFile, force=1, options="v=0;", type="mayaAscii", pr=1, ea=1)
                else:
                    print('FAILED TO EXPORT\n%s' % pubFile)
                    print('Check user permissions\n')
                    return
            else:
                cmds.file(pubFile, force=1, options="v=0;", type="mayaAscii", pr=1, ea=1)
        else:
            print('FAILED TO EXPORT\n%s' % pubFile)
            print('Check path exists\n')
            return
    except IOError:
        print('FAILED TO EXPORT\n%s' % pubFile)
        return
    message_out = ('JJ Exported:   {}'.format(pubFile))
    cmds.headsUpMessage(message_out, time=2.0)
    print(message_out)
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
    srcPub = [f for f in os.listdir(sourcePath) if f.endswith('PUBLISH.ma')]
    if len(srcPub) < 1:
        import sys
        sys.exit('No publish file present. \n  Check for a \'PUBLISH\' file in:\n  %s' % sourcePath)
    elif len(srcPub) > 1:
        import sys
        sys.exit('More than one publish file present. \n  Clean up directory:\n  %s' % sourcePath)
    else:
        return srcPub[0]


def loadRef(sourcePath):
    """
    Import references in publish file of a given sourcePath
    :param sourcePath: path of publish file to import references
    
    Used in:
        lightingSetup.buildMA()
    """
    # Find PUBLISH file in sourcePath and return filename only.
    srcPub = findPUBLISH(sourcePath)
    # Join sourcePath with PUBLISH filename
    srcPubFP = os.path.join(sourcePath, srcPub)

    # Check if PUBLISH is a file and load as a reference
    if os.path.isfile(srcPubFP):
        print '\nImporting reference from...\n    ', srcPubFP
        cmds.file(srcPubFP, mergeNamespacesOnClash=1, reference=1, namespace=':')
    else:
        raise NameError('could not find:\n    ' + srcPubFP)


# noinspection PyUnresolvedReferences
def loadDynamicShelf(shelfname):
    try:
        import yaml

        # Get icons path from the Maya.env ICONS_PATH variable
        iconsPath = os.environ.get('ICONS_PATH', None)

        # Get the CONFIGS_PATH from the Maya.env file and get the configuration files for the specified project
        configsPath = os.environ.get('DYNAMIC_SHELF_PATH', None)

        print('Loading shelf: {}'.format(shelfname))
        shelfConfFile = os.path.join(configsPath, '{}_dynamicShelfConf.yml'.format(shelfname))
        # shelfConfFile = os.path.join(dynamicShelfPath, '{}_dynamicShelfConf.xml'.format(shelfname))
        # Check if the file exist befor continuing
        if os.path.exists(shelfConfFile):
            # This is a fix for the automatically saved shelf function
            # It will delete a previously shelf named dynamicShelf created with the plugin if any exist
            removeDynamicShelf(shelfname)

            # Create a new shelfLayout in $gShelfTopLevel
            maya.mel.eval('${0} = `shelfLayout -cellWidth 33 -cellHeight 33 -p $gShelfTopLevel {0}`;'.format(shelfname))

            # Load yml config file
            yml_shelf = yaml.load(file(shelfConfFile, 'r'))

            if yml_shelf:
                # Loop trough each shelfItem entry in the shelfConfFile
                for button in sorted(yml_shelf.keys()):
                    # Create the actual shelf button with the above parameters
                    separator = False
                    shelf_params = {}
                    for param in sorted(yml_shelf[button].keys()):
                        if param == 'image':
                            if yml_shelf[button]['image']['location'] == 'custom':
                                shelf_params['image'] = '{}'.format(os.path.join(iconsPath, yml_shelf[button]['image']['name']))
                            else:
                                shelf_params['image'] = '{}'.format(yml_shelf[button]['image']['name'])
                        elif param == 'separator':
                            separator = True
                        elif param.startswith('mip'):
                            shelf_params['mi'] = '{}'.format(yml_shelf[button][param]['label']), '{}'.format(yml_shelf[button][param]['command'])
                            shelf_params[param.split(' ')[0]] = int(param.split(' ')[1])
                        else:
                            shelf_params[param] = '{}'.format(yml_shelf[button][param])
                    cmds.shelfButton(**shelf_params)

                    if separator:
                        cmds.separator(enable=1, width=10, height=35, style="shelf",
                                       manage=1, visible=1, preventOverride=0, enableBackground=0, horizontal=0)

            # Rename the shelfLayout with the shelfname
            maya.mel.eval('tabLayout -edit -tabLabel ${0} "'.format(shelfname) + shelfname + '" $gShelfTopLevel;')
            writeDynamicShelfPrefs(shelfname, True)

            print('{} shelf successfully loaded'.format(shelfname))

    except ImportError:
        pass


def reloadDynamicShelf(shelfname):
    # Delete the dynamicShelf if it exist
    """
    Reload shelves in the saved state for the user.
    """
    if readDynamicShelfPrefs(shelfname):
        removeDynamicShelf(shelfname)
        loadDynamicShelf(shelfname)
    elif not readDynamicShelfPrefs(shelfname):
        removeDynamicShelf(shelfname)


# noinspection PyUnresolvedReferences
def writeDynamicShelfPrefs(shelfname, state):
    """
    Write out yaml file preferences to user Maya prefs folder to save which shelves are opened and closed. 
    
    :param state: bool the shelf is True (on) or False (off)
    :param shelfname: name of shelf to write out
    """
    try:
        import yaml

        with open(prefsFileDynamicShelf(), 'r') as yaml_file:
            shelves = yaml.load(yaml_file)
            shelves[shelfname] = state

        with open(prefsFileDynamicShelf(), 'w') as yaml_file:
            yaml.dump(shelves, yaml_file, default_flow_style=False)

    except ImportError:
        pass


# noinspection PyUnresolvedReferences
def readDynamicShelfPrefs(shelfname):
    """
    Read yaml file preferences to user Maya prefs folder to save which shelves are opened and closed. 

    :rtype: state: None, True, or False is the state of the saved shelf.
    :param shelfname: name of shelf to read out
    """

    try:
        import yaml

        state = None
        with open(prefsFileDynamicShelf(), 'r') as yaml_file:
            shelves = yaml.load(yaml_file)
            if shelfname in shelves.keys():
                state = shelves[shelfname]

        return state

    except ImportError:
        pass


# noinspection PyUnresolvedReferences
def prefsFileDynamicShelf(maya_version='2017'):
    """
    Location of jj_dynamicShelfs_prefs.yml
    :param maya_version: default to 2017
    :rtype: prefs_file: location of prefs file for the current operating system
    
    """
    import sys

    try:
        import yaml

        prefs_file = ''
        if sys.platform == 'darwin':
            prefs_file = os.path.expanduser('~/Library/Preferences/Autodesk/maya/{}/prefs/jj_dynamicShelves_prefs.yml'.format(maya_version))
        elif sys.platform == 'win32':
            prefs_file = os.path.expanduser('~\Documents\maya\{}\prefs\jj_dynamicShelves_prefs.yml'.format(maya_version))
        elif sys.platform == 'linux2':
            prefs_file = os.path.expanduser('~/maya/{}/prefs/jj_dynamicShelves_prefs.yml'.format(maya_version))

        if not os.path.exists(prefs_file):
            with open(prefs_file, 'w') as yaml_file:
                empty = {'JJ': 'Dynamic Shelves Prefs', 'jj_ShelfLoader': True}
                yaml.dump(empty, yaml_file, default_flow_style=False)

        return prefs_file

    except ImportError:
        pass


def toggleDynamicShelf(shelfname):
    # Delete the dynamicShelf if it exist
    """
    Delete shelf.
    """
    if maya.mel.eval('shelfLayout -exists {0}'.format(shelfname)):
        removeDynamicShelf(shelfname)
        writeDynamicShelfPrefs(shelfname, False)
    else:
        loadDynamicShelf(shelfname)
        writeDynamicShelfPrefs(shelfname, True)


def removeDynamicShelf(shelfname):
    # Delete the dynamicShelf if it exist
    """
    Delete shelf.
    """
    maya.mel.eval('if (`shelfLayout -exists {0} `) deleteUI {0};'.format(shelfname))
    print('{} shelf successfully unloaded'.format(shelfname))

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
