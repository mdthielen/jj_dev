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

keyFile = r'C:\Users\robert\Documents\maya\scripts\storybots\python\sbtvKey.txt'

'''	
#epSeqShot = raw_input('Enter Episode Sequence Shot as ### ### ###: ')

test shot
epSeqShot = '101 100 020'

'''
#verify input format
'''
if not re.match('\d\d\d \d\d\d \d\d\d', epSeqShot): 	
	raise ValueError('please enter in the following format: ### ### ###')

ep, seq, shot = epSeqShot.split(' ')
'''
ep, seq, shot = argv[1:]

def readContents(filename):

	text = open(filename, 'r')	
	fileContents = text.read().splitlines()	
	text.close()
	
	return fileContents
	
fileContents = readContents(keyFile)


def getEp(ep, fileContents):

	for line in fileContents:
	
		if 'EPISODE' in line:
		
			if ep == line.split(' ')[1]:			

				epName = line.split(' ')[2]				
				epID = '_'.join( [ep, epName] )
				
				return epID, epName
				
	raise NameError('Episode number not found, check key:\n%s'%keyFile)
	
epID, epName = getEp( ep, fileContents )


def getSeq(seq, fileContents):

	for line in fileContents:	
	
		if 'SEQ' in line:
		
			if seq == line.split(' ')[1]:	
			
				seqName = line.split(' ')[2]
				seqID = '_'.join( [seq, seqName] )
				
				return seqID, seqName
				
	raise NameError('Seqence number not found, check input or update keyfile:\n    %s'%keyFile)
	
seqID, seqName = getSeq( seq, fileContents )

print epID, seqID
sequence = 'sq' + seqID		
import sbtvSandbox2
testSeq = sbtvSandbox2.SeqInfo(epID, sequence)		
