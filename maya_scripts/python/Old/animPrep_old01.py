import os

os.environ["MAYA_LOCATION"] = "C:\Program Files\Autodesk\Maya2015"

import maya.standalone 
maya.standalone.initialize( name = 'python' )
import maya.cmds as mc

import sbtvInfo
seq = sbtvInfo.SeqInfo(	'season_01', '101_rain', 'sq100_downpour')


import pipelineTools
from Old import animCleanup

#test ma file:						
ma = os.path.join( seq.seqPath, r'sh_020\03_maya\02_animation\sq100_020_downpour_anim_003.ma')
#for ma in seq.getLastAnim():
print( '\nOpening... \n    %s\n\n' % os.path.split(ma)[-1] )
mc.file(ma, force = True, open = True)
animCleanup.all()
pipelineTools.publish( ma, exportOnly = True )
pipelineTools.replaceRigs(ma)
mc.quit()
	

#pipelineTools.publish()
	
	
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
	mc.file(i, force=True, open=True)
	# Get all meshes in the scene
	mc.polySphere( n='mySphere', sx=5, sy=5, n="Youpi")
	# Save the file	   
	mc.file(save=True, force=True)
'''