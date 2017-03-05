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
		seq = sbtvInfo.SeqInfo('101_rain', 'sq100_downpour')
		seq.allShots
		#Returns:
		#['sh_010', 'sh_020', 'sh_030', 'sh_040', 'sh_050', 'sh_060', 'sh_070', 'sh_080', 'sh_090', 'sh_100', 'sh_110', 'sh_120', 'sh_130', 'sh_140', 'sh_150']
		
"""

import os
import re


class SeqInfo():

	def __init__(self, episode, sequence):

		import socket
		systemCheck = socket.gethostname()
		
		if systemCheck == 'robert-PC':
			project = r'C:\Users\robert\Documents\maya\projects\jibjab\sbtv'
		else:
			raise EnvironmentError('\"{0}\" was built to function on the computer, \'robert-PC\' not {1}\
			\n    Notify Robert Showalter if you are recieving this message'.format('sbtvInfo.py', systemCheck))

		stage = '2_production'
		season = 'season_01'
		
		self.seqPath = os.path.join(project,season,episode,stage,sequence)
		self.allShots = [ x for x in os.listdir(self.seqPath) if 'sh_' in x ]
		
		
	
	def getLastAnim(self):
	
		animDir = r'03_maya\02_animation'
		lastAnimMAs = []
		
		for shot in self.allShots:
			maPath = os.path.join(self.seqPath,shot,animDir)
			maFiles = [f for f in os.listdir(maPath) if '.ma' in f]
			
			if maFiles: 
				lastAnimMAs.append(os.path.join(maPath,maFiles[-1]))
				
		return lastAnimMAs

class ShotInfo():
	pass