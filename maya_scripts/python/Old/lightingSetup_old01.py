'''
Lighting setup
'''
#(u"C:/Users/robert/Documents/maya/projects/jibjab/sbtv/season_01/101_rain/2_production/sq030_reindeer/sh_110/03_maya/01_animation/s030_110_reindeer_animREF.mb").replace("\\","/");
import maya.cmds as mc
import os
import re


def importRef():
	curFile = mc.file(q=1, l=1)[0]
	curRoot = curFile.split('02_lighting')[0]
	animPath = curRoot + '01_animation'
	animPub = [ f for f in os.listdir( animPath ) if 'PUBLISH' in f ]
	if len(animPub) == 1:
		animPubFP = os.path.join( animPath, animPub[0] )
		mc.file( animPubFP, mergeNamespacesOnClash = 1, reference = 1, namespace = ':')
		print( '\n\# Reference imported \#' )
	elif len(animPub) < 1:
		print ('\# Error: no publish file present')
	elif len(animPub) > 1:
		print ('\# Error: more than one publish file present')


def importRefOld():
	#Reference in anim file
	currentFile = mc.file(q=1, l=1)[0]

	dept = '02_lighting' #department, used to crop file path
	ver = '_\d+.ma' #version syntax, in this case, to search for '_###.ma'

	animRef = re.split('/', currentFile)[-1]
	animRef = re.split( '_lit_', animRef)[0] #remove lighting file id
	animRef += '_animPUBLISH.ma' #add anim ref file id
	refFile = re.split( dept, currentFile)[0] #remove version suffix
	refFile += '/'.join(['01_animation', animRef]) #add REF suffix

	mc.file( refFile, defaultNamespace = 1, mergeNamespacesOnClash = 1, reference = 1)

def lightingCleanup():
	charAll = ['Bing_Riglocator', 'Beep_Riglocator', 'Bo_Riglocator', 'Boop_Riglocator', 'Bang_Riglocator']
	for char in charAll: 
		mc.editRenderLayerMembers( 'shd', char, noRecurse = 1 )
	mc.editRenderLayerMembers( 'shd', 'SHD_GEO_GRP', noRecurse = 1 )
	mc.select( 'SHD_GEO_GRP', r = 1 )
	newShdGrp = mc.duplicate( rr = 1 )[0]
	children = mc.listRelatives( newShdGrp, c = 1 )
	for c in children:
		shd = mc.rename( newShdGrp + '|' + c, c + '_shd' )
		noVis = mc.duplicate( shd, n= c+'_noVis', rr=1)[0]
		mc.setAttr( noVis + '.primaryVisibility', 0 )
		mc.sets( shd , addElement = 'groundPlane_shd_vrayobjectproperties')
		if not mc.objExists('groundPlane_noVis_set'): mc.sets( noVis , n = 'groundPlane_noVis_set')
		else: mc.sets( noVis , add = 'groundPlane_noVis_set')
		mc.hide( shd )
	mc.hide( 'SHD_GEO_GRP' )
	'''
	for char in charAll:
		for r in mc.listRelatives( char, ad = 1 ):
			if mc.objExists( r + '.primaryVisibility' ): 
				mc.setAttr( r + '.primaryVisibility', 0 )
	'''
		
'''
def setRenderGlobals():
	if mc.getAttr( 'defaultRenderGlobals.currentRenderer' ) != 'vray':
		mc.setAttr( 'defaultRenderGlobals.currentRenderer', 'vray', type = 'string' )
		
def swapRef(charAllRN = ['Bang_RigRN', 'Beep_RigRN', 'Bing_RigRN', 'Bo_RigRN', 'Boop_RigRN']):
	allRef = mc.ls(references=True)
	#remove unloaded reference from the list

	for char in charAllRN:
		if char in allRef:  
			origRef = mc.referenceQuery(char, f = 1)
			if '_Rig.ma' in origRef:
				vrayRef = origRef.split('_Rig.ma')[0] + '_Rig_Vray.ma'
				mc.file( vrayRef, loadReferenceDepth = 'asPrefs', loadReference = char)
'''
'''
create renderLayers
'''


'''Setup render directory Mel ref
// This will change the directory where
// batchRender-ed images go:
workspace -renderType "images" "c:/temp";
//Save the change into the workspace.mel afterwards:
workspace -saveWorkspace ;
'''


'''create groups 
bangGeo = 'Bang_Rig_GRP_All_Bang'
beepGeo = 'Beep_Rig_GRP_Beep_All'
bingGeo = 'Bing_Rig_Bing_ALL'
boGeo = 'Bo_Rig_BO_ALL'
boopGeo = 'Boop_Rig_BoopGeo'
eyeWhites = cmds.ls('*eye*', v = 1, type = 'mesh')
#for sel in cmds.ls(sl=1): print sel

charAll = [ bangGeo, beepGeo, bingGeo, boGeo, boopGeo ]

#Remove any characters that don't exist
for char in charAll:
	if not cmds.objExists( char ): charAll.remove( char )
'''

'''mel ref to find ref location, filename
cmds.referenceQuery( 'midRN',filename=True )
# Result: C:/Documents and Settings/user/My Documents/maya/projects/default/scenes/mid.ma
cmds.referenceQuery( 'mid:pCone1', filename=True, shortName=True )
# Result: mid.ma
'''
'''
setAttr "groundPlane_shd_vrayobjectproperties.matteSurface" 1;
setAttr "groundPlane_shd_vrayobjectproperties.alphaContribution" -1;
setAttr "groundPlane_shd_vrayobjectproperties.generateRenderElements" 0;
setAttr "groundPlane_shd_vrayobjectproperties.shadows" 1;
setAttr "groundPlane_shd_vrayobjectproperties.affectAlpha" 1;
setAttr "groundPlane_shd_vrayobjectproperties.giAmount" 0;
'''
