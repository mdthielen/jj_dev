#!/usr/bin/python
"""
Animation Cleanup

** Deprectated **
Clean up mental ray rigs to vray rigs.

Attributes:
    
Todo: 
    
"""

import maya.cmds as cmds


def delRenderLayers():
    """
    Delete all render layers.
    """
    print('Running %s...\n' % 'delRenderLayers')
    rLayers = [rln for rln in cmds.ls(type='renderLayer') if not 'default' in rln]
    for rln in rLayers: cmds.delete(rln); print 'Deleted %s renderlayer' % rln


def cleanREF_SG():
    """
    Remove reference shading group assignments
        * Remove unloaded references
        * Remove shading group reference edits
    """
    print('Running %s...' % 'cleanREF_SG')
    allRef = cmds.ls(references=True)

    # remove unloaded reference from the list
    for ref in allRef:
        if not cmds.referenceQuery(ref, isLoaded=1):
            allRef.remove(ref)
            print('****COULDN\'T FIND: %s' % ref)
    print('Found:')
    for ref in allRef: print('    %s' % ref)

    # unloading all references
    print('\nUnloading references...')
    for ref in allRef: cmds.file(unloadReference=ref)

    # remove Shading group reference edits
    print('Removing Shading Group reference edits...')
    for ref in allRef:
        sgEdits = [sge for sge in cmds.referenceQuery(ref, editNodes=True) if 'SG' in sge]
        for sge in sgEdits:
            cmds.referenceEdit(sge + '.dagSetMembers', failedEdits=True, successfulEdits=True, removeEdits=True)

    # reload reference
    print('Reloading...')
    for ref in allRef: print('    %s' % ref); cmds.file(loadReference=ref)
    print('')


'''
def delOldLights(oldLights = [u'mentalrayIbl1', u'Rim_Light', u'Bounce_Light', u'Keylight']):
    cmds.delete( oldLights )
'''


def delAllLights():
    """
    Delete all lights
    """
    print('Running %s...\n' % 'delAllLights')
    lightShapes = cmds.ls(type='light')
    lightTrans = cmds.listRelatives(lightShapes, p=1)
    if lightTrans: [cmds.delete(light) for light in lightTrans]


def groupSoloGeo():
    """
    Group all solo geo meshes
    """
    print('Running %s...' % 'groupSoloGeo')
    rootGeo = []
    for obj in cmds.ls(tr=1):
        if not cmds.listRelatives(obj, p=1):
            if cmds.listRelatives(obj, c=1, type='mesh'):
                rootGeo.append(obj)
    if not cmds.objExists('SHD_GEO_GRP'):
        if rootGeo:
            if len(rootGeo) == 1:
                setGRP = cmds.group(rootGeo[0], name='SHD_GEO_GRP')
            elif len(rootGeo) > 1:
                setGRP = cmds.group(rootGeo[0], rootGeo[1:], name='SHD_GEO_GRP')
            print('    created \"SHD_GEO_GRP\"')
        else:
            print 'No orphaned meshes found'
    else:
        print('****\"SHD_GEO_GRP\" already exists. Doing nothing.')

    '''
def setProxiesHi():
    rigRoots = ['Bing_Rig_Bing_ROOTC', 'Bo_Rig_Bo_ROOTC',]
    for root in rigRoots:
        cmds.setAttr( root + '.Proxy', 0 )
'''


def cleanAll():
    """
    Perform all clean
        * Delete render layers
        * Delete reference shading edits
        * group solo geo
    """
    delRenderLayers()
    cleanREF_SG()
    # delAllLights()
    groupSoloGeo()


'''

    if cmds.referenceQuery(sge + '.dagSetMembers', editStrings = True):
        print sge + '.dagSetMembers is an edit'
    if cmds.connectionInfo(sge + '.dagSetMembers', isSource = 1): print 'isSource'
    elif cmds.connectionInfo(sge + '.dagSetMembers', isDestination = 1): print 'isDestination'
    
sge = sgEdits[0]
cmds.listConnections(sge)

dagEdits = [es for es in editStrings if 'SG.dagSetMembers' in es]
len(dagEdits)
attr_types = cmds.referenceQuery( ref, editAttrs=True )


for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
            cmds.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)

#Clean ref python
for ref in cmds.ls(references=True):
    cmds.file(unloadReference=ref)
    cmds.file (cr=ref) # cleanReference

# Remove all edits
ref = 'myrefRN'
nodes = cmds.referenceQuery( ref, editNodes=True )
attr_types = cmds.referenceQuery( ref, editAttrs=True )
for node in nodes:
    for attr_type in attr_types:
        for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
            cmds.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)

#Pymel method
for ref in pm.listReferences():
    ref.unload()
    for edit in ref.getReferenceEdits():
        # this way you can selectively remove edits
        pm.ReferenceEdit(edit, fileReference=ref).remove(force=True)
    ref.load()

#But if you want to remove ALL edits it might be faster to do a clean(), which removes failed edits. If the ref is unloaded then all edits are failed :)
for ref in pm.listReferences():
    ref.unload()
    ref.clean()
    ref.load()	

#shading group filter
SG.dagSetMember

'''

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
