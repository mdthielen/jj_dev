#!/usr/bin/python
"""
Propogate Lighting shot to other lighting shots.
Use published animation files to create lightings shots.

Attributes:
    
    
Todo:
    
    
"""
# REVIEW[mark] Test this out
#  todo-mark clean up code

import os
import shutil
from sys import argv
import sbtvInfo
import pipelineTools


'''
os.environ["MAYA_LOCATION"] = "C:\Program Files\Autodesk\Maya2015"
import maya.standalone 
maya.standalone.initialize( name = 'python' )
import maya.cmds as cmds	
'''

try:
    ep, seq, srcShot = argv[1:4]
except:
    ep, seq, srcShot = raw_input('Enter Source: episode, sequence, shot as ### ### ###: ').split(' ')
try:
    destEntry = argv[4:][0]
except:
    destEntry = raw_input('Enter Destination: shot(s) as ###,###: ')
# test input
# ep, seq, srcShot = ['101', '100', '020']
# destEntry = '030, 040'
destShots = destEntry.split(',')
print 'Source:'
print '  ep  =', ep
print '  seq =', seq
print '  shot=', srcShot
print '\nDestination:'
for x in destShots:
    print '  shot = ', x


def getDeptID(shotMayaDir, department):
    """
    Get department ID
    this was built to bypass naming inconsistencies in the maya directory from sequence to sequence
    """
    for deptID in os.listdir(shotMayaDir):
        if department in deptID:
            return deptID  # sets dept to lighting dir name, regardless of prefix
        else:
            NameError('lighting directory not found in...%s\n    ' % shotMayaDir)


#
# Get source PUBLISH info
#

seqInfo = sbtvInfo.Info(ep, seq, srcShot)
seqPath = seqInfo.seqPath
seqName = seqInfo.seqName

srcMayaDir = os.path.join(seqPath, srcShot, '03_maya')  # sh removed for ep 103 seq 020
srcLitDir = os.path.join(srcMayaDir, getDeptID(srcMayaDir, 'lighting'))
srcAnimDir = os.path.join(srcMayaDir, getDeptID(srcMayaDir, 'animation'))


srcMAFile = pipelineTools.findPUBLISH(srcLitDir)
srcAnimPub = pipelineTools.findPUBLISH(srcAnimDir)
srcLong = os.path.join(srcLitDir, srcMAFile)
print '\nCopying from:\n%s  ' % srcLong

#
# Get new shot info
#
newShots = []
dstMayaDir = []

for shot in destShots:
    newShots.append('_'.join(['sq' + seq, shot, seqName, 'lit.0001.last_anim']))
    dstMayaDir.append(os.path.join(seqPath, shot, '03_maya'))  # sh removed for ep 103 seq 020

#
# copy src to dst, then edit reference directory
#
for i, shot in enumerate(newShots):

    dstLong = os.path.join(dstMayaDir[i], getDeptID(srcMayaDir, 'lighting'), shot)

    print '\nCreating...\n  ', dstLong, '\n'
    newFile = shutil.copy(srcLong, dstLong)

    print 'Reading contents...'
    fileContents = pipelineTools.readMA(dstLong)
    dstAnimDir = os.path.join(dstMayaDir[i], getDeptID(dstMayaDir[i], 'animation'))
    dstAnimPub = pipelineTools.findPUBLISH(dstAnimDir)
    # scrReplace = os.path.join( srcAnimDir.split( seqName )[-1], srcAnimPub.split('.ma')[0] ).replace('\\','/')
    scrFileReplace = srcAnimPub.split('.last_anim')[0]
    scrPathReplace = srcAnimDir.split(seqName)[-1].replace('\\', '/')
    # dstReplace = os.path.join( dstAnimDir.split( seqName )[-1], dstAnimPub.split('.ma')[0] ).replace('\\','/')
    dstFileReplace = dstAnimPub.split('.last_anim')[0]
    dstPathReplace = dstAnimDir.split(seqName)[-1].replace('\\', '/')

    print 'Updating references...'
    for j, line in enumerate(fileContents):

        if scrFileReplace in line or scrPathReplace in line:

            if len(fileContents[j]) < 250:  # limited to 250 characters for readability, though risking missed changes
                print '\nline', j, fileContents[j]

            fileContents[j] = fileContents[j].replace(scrFileReplace, dstFileReplace)
            fileContents[j] = fileContents[j].replace(scrPathReplace, dstPathReplace)

            if len(fileContents[j]) < 250:
                print 'line', j, fileContents[j]

    pipelineTools.writeMA(dstLong, fileContents)
    print '\n#Rewrote: \n  %s\n' % dstLong

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
