#import maya.standalone
#maya.standalone.initialize(name='python')

#import maya.cmds as cmds
import os

'''PROJECT INFO'''
proj = r'C:\Users\robert\Documents\maya\projects\jibjab\sbtv'
sea = 'season_01'
ep = '101_rain'
stage = '2_production'
#seq = input('input full seq name (eg \"sq030_reindeer\"):')
#if seq == '': 
seq = 'sq100_downpour'
seqPath = os.path.join(proj,sea,ep,stage,seq)
animDir = r'03_maya\02_animation'


allShots = [ x for x in os.listdir(seqPath) if 'sh_' in x ]
def getlastanim():
	alllastma = []
	for shot in allShots:
		maPath = os.path.join(seqPath,shot,animDir)
		maFiles = [f for f in os.listdir(dir) if '.ma' in f]
		if maFiles: 
			print maFiles[-1]
			alllastma.append(os.path.join(dir,maFiles[-1]))
	return alllastma
alllastma = getlastanim()
		
	
'''	
# The extension to search for
exten = '.ma'
# What will be logged
results = str()
myFiles = [] 
for root, dirs, files in os.walk(seqPath):
	for name in files:
		if '\\02_animation' in root: print( name )
		continue
		if name.endswith(exten):
			# Save to results string instead of printing
			results = '%s' % os.path.join(root, name)
			myFiles.append(name)
'''


'''
for i in myFiles:
	print i

for i in myFiles:
	cmds.file(i, force=True, open=True)
	# Get all meshes in the scene
	cmds.polySphere( n='mySphere', sx=5, sy=5, n="Youpi")
	# Save the file	   
	cmds.file(save=True, force=True)
'''