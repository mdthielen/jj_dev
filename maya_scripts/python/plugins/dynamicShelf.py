#!/usr/bin/python
"""
Dynamic shelf plug-in for Maya.

   AUTHOR : Nicolas Koubi
   WEBSITE : http://www.nkoubi.com/blog/tutorial/how-to-create-a-dynamic-shelf-plugin-for-maya/

Attributes:
    
Todo:
    * clean up code
    
"""

import sys
import os
import maya.mel
import maya.cmds as cmds
from xml.dom import minidom


# Get icons path from the Maya.env ICONS_PATH variable
iconsPath = os.environ.get('ICONS_PATH', None)

# Get scripts path from the Maya.env SCRIPTS_PATH variable
scriptsPath = os.environ.get('MAYA_SCRIPT_PATH', None)

# Get project name from the Maya.env PRJ_NAME variable
prjName = os.environ.get('PRJ_NAME', None)

# Get the CONFIGS_PATH from the Maya.env file and get the configuration files for the specified project
configsPath = os.environ.get('CONFIGS_PATH', None)


# Append the scriptsPath
sys.path.append(scriptsPath)


#
def initializePlugin(mobject):
    #
    """
    Initialize plug-in and create shelf.
    Get the shelf configuration file.
    
    """
    # shelfConfFile = os.path.join(prjConfFiles, 'dynamicShelfConf.xml')
    loadShelf(prjName)


def loadShelf(shelfname):

    # todo-mark how to load multiple shelves
    prjConfFiles = os.path.join(configsPath, shelfname)
    shelfConfFile = os.path.join(prjConfFiles, 'dynamicShelfConf.xml')

    # Check if the file exist befor continuing
    if os.path.exists(shelfConfFile) == True:

        # This is a fix for the automatically saved shelf function
        # It will delete a previously shelf named dynamicShelf created with the plugin if any exist
        maya.mel.eval('if (`shelfLayout -exists dynamicShelf `) deleteUI dynamicShelf;')

        # Declare the $gShelfTopLevel variable as a python variable
        # $gShelfTopLevel mel variable is the Maya default variable for the shelves bar UI
        maya.mel.eval('global string $gShelfTopLevel;')
        # shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
        # Declare the $dynamicShelf (the shelfLayout) as a global variable in order to unload it after
        # todo-mark set global var to store all shelves
        maya.mel.eval('global string $dynamicShelf;')
        # Create a new shelfLayout in $gShelfTopLevel
        maya.mel.eval('$dynamicShelf = `shelfLayout -cellWidth 33 -cellHeight 33 -p $gShelfTopLevel dynamicShelf`;')

        # Parse the menuConfFile
        xmlMenuDoc = minidom.parse(shelfConfFile)

        # Loop trough each shelfItem entry in the shelfConfFile
        for eachShelfItem in xmlMenuDoc.getElementsByTagName("shelfItem"):
            # Get the icon name
            getIcon = eachShelfItem.attributes['image'].value
            # Join the icon name to the icons path in order to get the full path of the icon
            shelfBtnIcon = os.path.join(iconsPath, getIcon)
            # Get the annotation
            getAnnotation = eachShelfItem.attributes['ann'].value
            # Get the command to launch
            getCommand = eachShelfItem.attributes['command'].value

            # todo-mark loading other attributes of shelves such as the pull downs
            getMi01 = eachShelfItem.attributes['mi01'].value
            getMi02 = eachShelfItem.attributes['mi02'].value
            getMip0 = int(eachShelfItem.attributes['mip0'].value)

            # Create the actual shelf button with the above parameters
            if getMi01 != '':
                cmds.shelfButton(command=getCommand, annotation=getAnnotation, image=shelfBtnIcon, mi=[getMi01, getMi02], mip=getMip0)
            else:
                cmds.shelfButton(command=getCommand, annotation=getAnnotation, image=shelfBtnIcon)

        # Rename the shelfLayout with the shelfname
        maya.mel.eval('tabLayout -edit -tabLabel $dynamicShelf "' + shelfname + '" $gShelfTopLevel;')

        print "//-- " + shelfname + " shelf successfully loaded --//"


def uninitializePlugin(mobject):
    # Delete the dynamicShelf if it exist
    """
    Un-Initialize plug-in and delete shelf.
    """
    # todo-mark how to unload multiple shelves - iterate through global shelf variable defined in this file
    maya.mel.eval('if (`shelfLayout -exists dynamicShelf `) deleteUI dynamicShelf;')


__author__ = "Nicolas Koubi"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/14/17"
__credits__ = ["Nicolas Koubi"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"

