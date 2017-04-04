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
import pipelineTools

# Get scripts path from the Maya.env SCRIPTS_PATH variable
scriptsPath = os.environ.get('MAYA_SCRIPT_PATH', None)

# Get the DYNAMIC_SHELF_PATH from the Maya.env file and get the configuration files for the specified project
dynamicShelfPath = os.environ.get('DYNAMIC_SHELF_PATH', None)


# Append the scriptsPath
sys.path.append(scriptsPath)


def initializePlugin(mobject):
    #
    """
    Initialize plug-in and create shelf.
    Get the shelf configuration file.
    
    """
    import pipelineTools
    # shelfConfFile = os.path.join(prjConfFiles, 'dynamicShelfConf.xml')
    maya.mel.eval('global string $gShelfTopLevel;')

    jj_shelf_loader = 'jj_ShelfLoader'
    pipelineTools.loadDynamicShelf(jj_shelf_loader)

    dynamic_shelves = [shelf.split('_dynamicShelfConf.yml')[0] for shelf in os.listdir(dynamicShelfPath)
                       if 'dynamicShelfConf.yml' in shelf and 'ShelfLoader' not in shelf]

    for dynamic_shelf in dynamic_shelves:
        pipelineTools.reloadDynamicShelf(dynamic_shelf)


def uninitializePlugin(mobject):
    # Delete the dynamicShelf if it exist
    """
    Un-Initialize plug-in and delete shelf.
    """
    dynamic_shelves = [shelf.split('_dynamicShelfConf.yml')[0] for shelf in os.listdir(dynamicShelfPath)
                       if 'dynamicShelfConf.yml' in shelf]
    for dynamic_shelf in dynamic_shelves:
        pipelineTools.removeDynamicShelf(dynamic_shelf)


__author__ = "Nicolas Koubi"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/14/17"
__credits__ = ["Nicolas Koubi, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"

