"""
    sbtvInfo
    
    Copyright (c) 2015 Robert Showalter
    All Rights Reserved.
    rshowalt@c.ringling.edu
    
    Description:
        This is the core script for working within the storybot, aka "SBTV" project.
		
		It's purpose is retrieving sequence and shot data based on the project hierarchy.
		
		Many artist have been involved in this organic, and loosely regulated pipeline.
		This script and others using it attempt to organize and make sense of the 
		existing pipeline and, hopefully, iron out some inconsistencies.
    
    Example usage:
        import sbtvInfo
		seqInfo = sbtvInfo.SeqInfo('101', '100')
		seqInfo.allShots
		#Returns:
		#['sh_010', 'sh_020', 'sh_030', 'sh_040', 'sh_050', 'sh_060', 'sh_070', 'sh_080', 'sh_090', 'sh_100', 'sh_110', 'sh_120', 'sh_130', 'sh_140', 'sh_150']
		
"""


import os
import re
import sys

if sys.platform == 'darwin':
    keyFile = r'/Volumes/public/StoryBots/sbtv/03_shared_assets/01_cg/maya_tools/maya_scripts/python/sbtvKey.txt'
elif sys.platform == 'win32':
    keyFile = r'C:\Users\robert\Documents\maya\scripts\storybots\python\sbtvKey.txt'
elif sys.platform == 'linux2':
    keyFile = r'/home/rshowalter/maya/scripts/storybots/python/sbtvKey.txt'
else:
    print('couldn\'t recognize operating system')
    import sys; sys.exit()
stage = '2_production'
season = 'season_01'


def readContents( keyFile ):

		text = open(keyFile, 'r')	
		fileContents = text.read().splitlines()	
		text.close()
		
		return fileContents
		

def getEp( ep, fileContents):

	for line in fileContents:
	
		if 'EPISODE' in line:
		
			if ep == line.split(' ')[1]:			

				epName = line.split(' ')[2]				
				epID = '_'.join( [ep, epName] )
				
				return epID, epName
				
	raise NameError('Episode number not found, check key:\n%s'%keyFile)
	

def getSeq( seq, fileContents):

	for line in fileContents:	
	
		if 'SEQ' in line:
		
			if seq == line.split(' ')[1]:	
			
				seqName = line.split(' ')[2]
				seqID = '_'.join( [seq, seqName] )
				
				return seqID, seqName
				
	raise NameError('Seqence number not found, check input or update keyfile:\n    %s'%keyFile)

class Info():
	
    def __init__(self, ep, seq, shot=''):
        self.ep = ep
        self.seq = seq
        self.shot = shot
		
		
        #import socket
        #systemCheck = socket.gethostname()
        
        if sys.platform == 'darwin':
            project = r'/Volumes/public/StoryBots/sbtv'
        elif sys.platform == 'win32':
            project = r'C:\Users\robert\Documents\maya\projects\jibjab\sbtv'
        elif sys.platform == 'linux2':
            project = r'/home/rshowalter/maya/projects/SBTV'
		#expand this later for mac machines, though many other changes may be needed
        else:
			raise EnvironmentError('This system was not recognised')
		
        fileContents = readContents(keyFile)
		
        self.epID, self.epName = getEp( self.ep, fileContents )
        self.seqID, self.seqName = getSeq( self.seq, fileContents )
        self.sequence = 'sq' + self.seqID		
        self.seqPath = os.path.join(project,season,self.epID,stage,self.sequence)
        self.allShots = [ x for x in os.listdir(self.seqPath) if 'sh_' in x ]
		
		

    def getLastAnim(self):
        
        import socket
        systemCheck = socket.gethostname()
        '''
        if os.name == 'posix':
            animDir = r'03_maya/02_animation'
        elif systemCheck == 'robert-PC':
            animDir = r'03_maya\02_animation'
        '''    
        
        lastAnimMAs = []
		
        for shot in self.allShots:
            shotDirMaya = os.path.join(self.seqPath, shot, '03_maya')
            for dept in os.listdir(shotDirMaya):
            	if 'animation' in dept: 
            		animDir = os.path.join(shotDirMaya, dept)
            	else: NameError('lighting directory not found in...%s\n    '%shotDirMaya)
            print animDir
            maPath = os.path.join(shotDirMaya,animDir)
            maFiles = [f for f in os.listdir(maPath) if '.ma' in f if not 'PUBLISH' in f]
            maFiles.sort()
			
            if maFiles: 
                lastAnimMAs.append(os.path.join(maPath,maFiles[-1]))
				
        return lastAnimMAs

#SeqInfo('season_01', '101_rain', 'sq100_downpour')
'''
class ShotInfo():
	pass

if __name__ == '__main__':
    print 'name = main'
    sys.exit()
    from sys import argv
    ep, seq, shot = argv[1:]
    print Info(ep, seq, shot).seqPath
    for x in Info(ep, seq, shot).allShots: print x
'''	
