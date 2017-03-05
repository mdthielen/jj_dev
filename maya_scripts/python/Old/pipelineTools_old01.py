'''PUBLISH FILE'''
import maya.cmds as mc
import re
'''
class pipelineTools:
	def __init__(self, ma):
		currentFile = mc.file( ma, force = True, open = True )
		print currentFile
		ver = '_?\d+.ma$' #version syntax, in this case, to search for '###.ma'
		refFile = re.split( ver, currentFile)[0] #remove version suffix
		print refFile
		refFile += r'PUBLISH.ma' #add PUBLISH suffix
		print refFile
		mc.file( rename = refFile)
		mc.file( save = True , force = True)
		print(mc.file( q=1, l=1)[0])
'''
def refName( currentFile = mc.file(q=1, l=1)[0] ):
    ver = '_?\d+.ma$' #version syntax, in this case, to search for '###.ma'
    refFile = re.split( ver, currentFile)[0] #remove version suffix
    refFile += r'PUBLISH.ma' #add PUBLISH suffix
    return refFile

def publish():
	refFile = refName()
    #export all as a .ma file, overwrite if existing.
	mc.file( rename = refFile)
	mc.file( save = True , force = True)
	print mc.file(q=1, l=1)[0]
	#mc.file( refFile, force = 1, options= "v=0;", type= "mayaAscii", pr = 1, ea = 1) 
    
    #save the current file
    #mc.file( save = 1, force = 1)

'''REPLACE ANIM RIGS WITH VRAY RIGS'''
def replaceRigs( refFile = refName()+'.ma' ):
    if '01_animation' in refFile:
        mayaFile = open(refFile, 'r')
        fileContents = mayaFile.readlines()
        mayaFile.close()
        for i in range(len(fileContents)):
            fileContents[i] = fileContents[i].replace('_Rig.ma', '_Rig_Vray.ma')
        mayaFile = open(refFile, 'w')
        mayaFile.writelines(fileContents)
        mayaFile.close()
    else: print 'please run from a versioned animation file'