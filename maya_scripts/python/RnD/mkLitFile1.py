import os
import shutil
import re

'''PROJECT INFO'''
proj = r'C:\Users\robert\Documents\maya\projects\jibjab\sbtv'
sea = 'season_01'
ep = '101_rain'
stage = '2_production'
seq = input('input full seq name (eg \"sq030_reindeer\"):')
if seq == '': seq = 'sq030_reindeer'
seqPath = '\\'.join([proj,sea,ep,stage,seq])

template = 's030_000_reindeer_lit_lightingTemplate.ma'
templateFP = '\\'.join([seqPath,'_master','_render',template])

exclude = [ 'sh_160', 'sh_180', 'sh_200', 'sh_230', 'sh_240', 'sh_250', 'sh_290']


def getAllShots(exclude):
	allShots = [ x for x in os.listdir(seqPath) if 'sh_' in x ]
	allShots = [ x for x in allShots if not x in exclude ]
	return allShots
	

def returnAllFiles(dept = '02_lighting'):
	allShots = getAllShots(exclude)
	for shot in allShots:
		#print('\n', shot)
		lightingDir = '\\'.join( [seqPath,shot,'03_maya', dept] )
		files = os.listdir(lightingDir)
		for f in files:	
			print (os.path.join(lightingDir, f))
			pass
			if 'PUBLISH' in f:
				print (os.path.join(lightingDir, f))
#returnAllFiles()

def createMA(lightingDir, shotNum):
	print (lightingDir, shotNum)
	#Create directory	
	newFileFP = os.path.join( templateFP, lightingDir )
	if os.path.isfile( newFileFP ):
		print ('exists: ', newFileFP)
	else: print ('------ ', newFileFP)
	return
	#Copy template
	newFile = shutil.copy2( templateFP, lightingDir )
	#Rename template
	shot1 = re.sub( 'lightingTemplate', '001', newFile )
	shot1 = re.sub( '000', shotNum, shot1)
	shutil.copy( newFile, shot1 )
	print( 'created: ', shot1 )

	
def populateEmptyDirs():
	allShots = getAllShots(exclude)
	for shot in allShots:
		shotNum = re.findall('\d+', shot)[0]
		lightingDir = '\\'.join( [seqPath,shot,'03_maya','02_lighting'] )
		if not os.path.exists( lightingDir ): 
			newDir = os.mkdir( lightingDir )
			print ( '*Created*', lightingDir )
		createMA( lightingDir, shotNum )
#populateEmptyDirs()

			
def checkDirs():
	allShots = [ x for x in os.listdir(seqPath) if 'sh_' in x ]
	allDirs = []
	for shot in allShots:
		lightingDir = '\\'.join( [seqPath,shot,'03_maya','02_lighting'] )
		if os.path.exists( lightingDir ): 
			allDirs.append(lightingDir)
	return allDirs

def removeUnlabeled():
	#accidentally created unlabeled files while creating script. This was made to delete those.
	allFiles = []
	for x in checkDirs(): 
		for f in os.listdir(x): allFiles.append( os.path.join(x, f ))
	[os.remove( x ) for x in allFiles if '000' in x]
	
def formatWarning():
	print( 'format = ### \neg>>> 010')
	
def importAnimRef(num):
	shot = 'sh_' + str(num)
	import maya.standalone 
	maya.standalone.initialize( name='python' )
	
	import maya.cmds as mc

'''
	shot = 'sh_' + str(num)
	#shot += input('input shot number (eg \"030\"):')
	if not re.match('sh_\d\d\d', shot): 
		formatWarning()
		return
	else: print(shot)
	animPath = os.path.join( seqPath, shot, '03_maya', '01_animation')
	animPub = [ f for f in os.listdir( animPath ) if 'PUBLISH' in f ]
	if len(animPub) == 1:
		animPubFP = os.path.join( animPath, animPub[0] )
	
	os.system('mayabatch -file %s -command "python( \"import importRefCMD\");" & pause'%(animPubFP))
'''

'''
	os.system("echo \"crap\" & Pause")
	mayabatch -file someMayaFile.mb -command "file -save"
'''