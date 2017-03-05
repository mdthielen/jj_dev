import os
from sys import argv
import shutil
import re



'''
os.environ["MAYA_LOCATION"] = "C:\Program Files\Autodesk\Maya2015"
import maya.standalone 
maya.standalone.initialize( name = 'python' )
import maya.cmds as mc	
'''

try: ep, seq, srcShot = argv[1:4]
except: ep, seq, srcShot = raw_input( 'Enter Source: episode, sequence, shot as ### ### ###: ' ).split(' ')
try: destEntry = argv[4:][0]
except: destEntry = raw_input( 'Enter Destination: shot(s) as ###,###: ' )
#test input
#ep, seq, srcShot = ['101', '100', '020']
#destEntry = '030, 040'
destShots = destEntry.split(',')
print 'Source:'
print '  ep  =', ep
print '  seq =', seq
print '  shot=', srcShot
print '\nDestination:'
for x in destShots: print '  shot = ', x


def getDeptID( shotMayaDir, department):
	'''this was built to bypass naming inconsistencies in the maya directory from sequence to sequence'''
	for deptID in os.listdir(shotMayaDir):
		if department in deptID: 
			return deptID #sets dept to lighting dir name, regardless of prefix
		else: NameError('lighting directory not found in...%s\n    '%shotMayaDir)
		
		
#
# Get source PUBLISH info
#
import sbtvInfo

seqInfo = sbtvInfo.Info(ep, seq, srcShot)
seqPath = seqInfo.seqPath
seqName = seqInfo.seqName

srcMayaDir = os.path.join(seqPath, 'sh_' + srcShot, '03_maya')	
srcLitDir = os.path.join(srcMayaDir, getDeptID(srcMayaDir,'lighting'))
srcAnimDir = os.path.join(srcMayaDir, getDeptID(srcMayaDir,'animation'))

import pipelineTools

srcMAFile = pipelineTools.findPUBLISH(srcLitDir)
srcAnimPub = pipelineTools.findPUBLISH(srcAnimDir)
srcLong = os.path.join( srcLitDir, srcMAFile )
print '\nCopying from:\n%s  ' % srcLong

#
# Get new shot info
#
newShots = []
dstMayaDir = []

for shot in destShots:
	newShots.append( '_'.join(['sq' + seq, shot, seqName, 'lit.0001.ma']) )
	dstMayaDir.append( os.path.join(seqPath, 'sh_' + shot, '03_maya') )

	
#
#copy src to dst, then edit reference directory
#
for i, shot in enumerate(newShots):

	dstLong = os.path.join( dstMayaDir[i], getDeptID(srcMayaDir,'lighting'), shot )
	
	print '\nCreating...\n  ', dstLong, '\n'
	newFile = shutil.copy( srcLong, dstLong )
	
	print 'Reading contents...'
	fileContents = pipelineTools.readMA(dstLong)	
	dstAnimDir = os.path.join( dstMayaDir[i], getDeptID(dstMayaDir[i], 'animation') )
	dstAnimPub = pipelineTools.findPUBLISH(dstAnimDir)
	#scrReplace = os.path.join( srcAnimDir.split( seqName )[-1], srcAnimPub.split('.ma')[0] ).replace('\\','/')
	scrFileReplace = srcAnimPub.split('.ma')[0]
	scrPathReplace = srcAnimDir.split( seqName )[-1].replace('\\','/')
	#dstReplace = os.path.join( dstAnimDir.split( seqName )[-1], dstAnimPub.split('.ma')[0] ).replace('\\','/')
	dstFileReplace = dstAnimPub.split('.ma')[0]
	dstPathReplace = dstAnimDir.split( seqName )[-1].replace('\\','/')
	
	print 'Updating references...'
	for i, line in enumerate(fileContents):

		if scrFileReplace in line or scrPathReplace in line:
		
			if len(fileContents[i])<250: #limited to 250 characters for readability, though risking missed changes
				print '\nline', i, fileContents[i] 
			
			fileContents[i] = fileContents[i].replace(scrFileReplace, dstFileReplace)
			fileContents[i] = fileContents[i].replace(scrPathReplace, dstPathReplace)
			
			if len(fileContents[i])<250: 
				print 'line', i, fileContents[i]
		
	pipelineTools.writeMA(dstLong, fileContents)
	print '\n#Rewrote: \n  %s\n' % dstLong

	
