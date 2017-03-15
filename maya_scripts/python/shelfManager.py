#!/usr/bin/python
"""
Shelf manager to load in updates for any studio shelves.


Attributes:
    
    
Todo:
    
    
"""

import maya.cmds as cmds
import maya.mel as mel


def createMyShelf():
    shelfName = 'My_Shelf'
    test = cmds.shelfLayout(shelfName, ex=True)
    if test:
        # If the shelf already exists, clear the contents and re-add the buttons.
        newShelf = shelfName
        buttons = cmds.shelfLayout(newShelf, query=True, childArray=True)
        cmds.deleteUI(buttons, control=True)
    else:
        newShelf = mel.eval('addNewShelfTab %s' % shelfName)
        cmds.setParent(newShelf)
        # add buttons here


def removeShelf():
    shelfName = 'My_Shelf'
    test = cmds.shelfLayout(shelfName, ex=True)
    if test:
        mel.eval('deleteShelfTab %s' % shelfName)
        gShelfTopLevel = mel.eval('$tmpVar=$gShelfTopLevel')
        cmds.saveAllShelves(gShelfTopLevel)
    else:
        return


def shelfPrevious():
    import maya.mel as mel
    mel.eval("incrementSelectedShelf(-1)")


__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/14/17"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
