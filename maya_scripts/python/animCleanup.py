'''ANIM CLEANUP'''

import maya.cmds as mc

def delRenderLayers():
	print('Running %s...\n' % 'delRenderLayers' )
	rLayers = [rln for rln in mc.ls(type = 'renderLayer') if not 'default' in rln]
	for rln in rLayers: mc.delete( rln ); print 'Deleted %s renderlayer' % rln

#remove shading group assignments
def cleanREF_SG():
	print('Running %s...' % 'cleanREF_SG' )
	allRef = mc.ls(references=True)
	
	#remove unloaded reference from the list
	for ref in allRef:
		if not mc.referenceQuery(ref, isLoaded=1): 
			allRef.remove(ref) 
			print( '****COULDN\'T FIND: %s' % ref )
	print( 'Found:' )
	for ref in allRef: print('    %s'%ref ) 
	
	#unloading all references
	print( '\nUnloading references...' )
	for ref in allRef: mc.file(unloadReference=ref) 
	
	#remove Shading group reference edits
	print( 'Removing Shading Group reference edits...' )
	for ref in allRef:		
		sgEdits = [sge for sge in mc.referenceQuery( ref, editNodes=True ) if 'SG' in sge]
		for sge in sgEdits:
			mc.referenceEdit( sge + '.dagSetMembers', failedEdits=True, successfulEdits=True, removeEdits=True)
	
	#reload reference
	print( 'Reloading...' )
	for ref in allRef: print( '    %s'%ref ); mc.file(loadReference = ref)
	print( '' )
'''
def delOldLights(oldLights = [u'mentalrayIbl1', u'Rim_Light', u'Bounce_Light', u'Keylight']):
	mc.delete( oldLights )
'''
def delAllLights():
	print('Running %s...\n' % 'delAllLights' )
	lightShapes = mc.ls(type = 'light')
	lightTrans = mc.listRelatives( lightShapes, p = 1)
	if lightTrans: [mc.delete(light) for light in lightTrans]
	
def groupSoloGeo():
	print('Running %s...' % 'groupSoloGeo' )
	rootGeo = []
	for obj in mc.ls(tr = 1):
		if not mc.listRelatives( obj, p = 1 ):
			if mc.listRelatives( obj, c = 1, type = 'mesh' ):
				rootGeo.append(obj)
	if not mc.objExists('SHD_GEO_GRP'):
		if rootGeo:
			if len(rootGeo) == 1:
				setGRP = mc.group( rootGeo[0], name = 'SHD_GEO_GRP')
			elif len(rootGeo) > 1:
				setGRP = mc.group( rootGeo[0], rootGeo[1:], name = 'SHD_GEO_GRP')
			print('    created \"SHD_GEO_GRP\"')	
		else: 
			print 'No orphaned meshes found'
	else: print('****\"SHD_GEO_GRP\" already exists. Doing nothing.')

	'''
def setProxiesHi():
	rigRoots = ['Bing_Rig_Bing_ROOTC', 'Bo_Rig_Bo_ROOTC',]
	for root in rigRoots:
		mc.setAttr( root + '.Proxy', 0 )
'''	

def all():
	delRenderLayers()
	cleanREF_SG()
	#delAllLights()
	groupSoloGeo()

'''

    if mc.referenceQuery(sge + '.dagSetMembers', editStrings = True):
        print sge + '.dagSetMembers is an edit'
    if mc.connectionInfo(sge + '.dagSetMembers', isSource = 1): print 'isSource'
    elif mc.connectionInfo(sge + '.dagSetMembers', isDestination = 1): print 'isDestination'
    
sge = sgEdits[0]
mc.listConnections(sge)

dagEdits = [es for es in editStrings if 'SG.dagSetMembers' in es]
len(dagEdits)
attr_types = mc.referenceQuery( ref, editAttrs=True )


for edit_command in ['addAttr', 'connectAttr', 'deleteAttr', 'disconnectAttr', 'parent', 'setAttr', 'lock', 'unlock']:
            mc.referenceEdit( node+'.'+attr_type, failedEdits=True, successfulEdits=True, removeEdits=True, editCommand=edit_command)

#Clean ref python
for ref in mc.ls(references=True):
	mc.file(unloadReference=ref)
	mc.file (cr=ref) # cleanReference
	
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