#!/usr/bin/python
"""
Lighting setup
Sets up new lighting shots based on animation publishes and then references in the anim PUBLISH file.
Upon running with episode, sequence and shot as parameters, buildMA is called as main function.

Syntax:
    lightingSetup <episode> <sequence> <shot>

Arguments: (requires all 3)
    episode, sequence, shot
"""

# todo-mark clean up code that would be best inside a function and then called from __main__
# REVIEW[mark] Test running lightingSetup on a sample shot to create new lighting file.

# shotDirMaya variable modified on 12/3/2015 to accomodate an inproperly named directory structure
# changed again on 1/20/2016 to accomodate 01_maya directory of old 102/070 directory naming
# changed again on 1/30/2016 to accomodate 103/040 artist directory structure

import os
import re
from sys import argv

import maya.standalone
import maya.cmds as cmds
import sbtvInfo
import pipelineTools

try:
    ep, seq, shot = argv[1:]
except IOError:
    ep, seq, shot = raw_input('enter episode, sequence, shot as ### ### ###: ').split(' ')
# test input
# ep, seq, shot = ['101', '100', '120']
print 'ep  =', ep
print 'seq =', seq
print 'shot=', shot

maya.standalone.initialize(name='python')

seqInfo = sbtvInfo.Info(ep, seq, shot)
seqPath = seqInfo.seqPath
seqName = seqInfo.seqName

# epNum/seqNum/sh_shotNum/<Layer> - to be used for output directory
essid = r'/'.join([seqInfo.epID, seqInfo.seqID, 'sh_' + shot, '<Layer>'])

for x in os.listdir(seqPath):
    if 'sh_' in x:
        shotDirMaya = os.path.join(seqPath, 'sh_' + shot, '03_maya')
        break
else:
    shotDirMaya = os.path.join(seqPath, shot, '03_maya')

litDir = None
for dept in os.listdir(shotDirMaya):
    if 'lighting' in dept:
        litDir = os.path.join(shotDirMaya, dept)
    else:
        pass
        # raise NameError('lighting directory not found in...%s\n    '%shotDirMaya)

try:
    litDir
except IOError:
    dept = raw_input('Enter lighting folder name [05_lighting]: ') or '05_lighting'
    litDir = os.path.join(shotDirMaya, dept)
    os.makedirs(litDir)

newShot = '_'.join(['sq' + seq, shot, seqName, 'lit.0001.last_anim'])


def buildMA(destDir, sourcePath, newShot):
    newFile = os.path.join(destDir, newShot)

    if os.path.isfile(newFile):
        # raise  StandardError('this file already exists')
        startStop = raw_input('\n' + newFile + '\n\nAlready exists. Overwrite? (y/n):')
        if startStop == 'n':
            print 'canceled file creation'
            return
        elif startStop == 'y':
            pass
        else:
            print 'try again. Enter only \"y\" or \"n\"'
            return
    else:
        print '\n*Creating \n    ', newFile

    # Create new lighting file with proper naming and in correct folder
    cmds.file(rename=newFile)
    cmds.file(type='mayaAscii')

    # Load reference animation PUBLISH file into new lighting file
    pipelineTools.loadRef(sourcePath)

    # Set render settings, set VRay settings and render layers,
    # set persp cam to not renderable, set shotCam to renderable,
    # remove image planes from visibility, remove unknown nodes
    lightingBasics(essid)

    # Set time range to match animation PUBLISH time range
    setFrameRange(animDir)

    # Save lighting file
    cmds.file(save=True, force=True, type='mayaAscii')
    print '\nSaved', newFile

    cmds.quit()


def lightingBasics(essid=None):  # essid = epNum/seqNum/sh_shotNum/<Layer>

    # set renderer to vray
    cmds.loadPlugin("vrayformaya.mll")
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "vray", type="string")

    # on unix systems, the vray renderGlobals are not loading, therefore vraySettings cannot be set.

    # set output directory
    if essid:
        try:
            cmds.setAttr("vraySettings.fileNamePrefix", essid, type="string")
        except IOError:
            pass
    # set output format
    if cmds.optionMenuGrp("vrayImageFormatMenu", exists=1):
        cmds.setAttr("vraySettings.imageFormatStr", "exr", type="string")
    # Disable persp camera
    cmds.setAttr("perspShape.renderable", 0)
    # Set shot camera to renderable
    try:
        cmds.setAttr("shotCamShape.renderable", 1)
    except IOError:
        print('No shotCam found. No camera is renderable')

    # set render resolution
    try:
        cmds.setAttr("vraySettings.width", 1920)
        cmds.setAttr("vraySettings.height", 1080)
        cmds.setAttr("defaultRenderGlobals.animation", 1)
        cmds.setAttr("vraySettings.animBatchOnly", 1)
    except IOError:
        cmds.setAttr("defaultResolution.width", 1920)
        cmds.setAttr("defaultResolution.height", 1080)

    # setup render elements
    import maya.mel
    matteElements = ['vrayRE_Multi_Matte0',
                     'vrayRE_Multi_Matte1',
                     'vrayRE_Multi_Matte2']
    i = 1
    for elem in matteElements:
        maya.mel.eval('vrayAddRenderElement( "MultiMatteElement" );')
        cmds.rename('vrayRE_Multi_Matte', elem)
        cmds.setAttr(elem + '.vray_name_multimatte', re.split('_', elem)[-1], type='string')
        cmds.setAttr(elem + '.vray_redid_multimatte', i)
        i += 1
        cmds.setAttr(elem + '.vray_greenid_multimatte', i)
        i += 1
        cmds.setAttr(elem + '.vray_blueid_multimatte', i)
        i += 1
        cmds.setAttr(elem + '.vray_usematid_multimatte', 1)
    createVRayMultiMattes('vrayRE_matteChar1', 3, 2, 1)
    createVRayMultiMattes('vrayRE_matteChar2', 5, 4, 0)
    createVRayMultiMattes('vrayRE_matteCharEyesL', 11, 12, 13, 1)
    createVRayMultiMattes('vrayRE_matteCharEyesR', 14, 15, 16, 1)
    maya.mel.eval('vrayAddRenderElement( "diffuseChannel" );')
    maya.mel.eval('vrayAddRenderElement( "giChannel" );')
    maya.mel.eval('vrayAddRenderElement( "velocityChannel" );')
    maya.mel.eval('vrayAddRenderElement( "zdepthChannel" );')
    maya.mel.eval('vrayAddRenderElement( "specularChannel" );')

    # turn off default image plane
    try:
        cmds.setAttr('imagePlaneShape1.displayMode', 0)
    except IOError:
        pass

    # delete unknown nodes
    unknownNodes = cmds.ls(type='unknown')
    try:
        if unknownNodes:
            print "Deleting..."
            for n in unknownNodes:
                cmds.delete(n)
                print('    ' + n)
    except IO:
        print 'No unknown nodes found'


def createVRayMultiMattes(elem, r, g, b, MID=0):
    import maya.mel
    maya.mel.eval('vrayAddRenderElement( "MultiMatteElement" );')
    cmds.rename('vrayRE_Multi_Matte', elem)
    cmds.setAttr(elem + '.vray_name_multimatte', re.split('_', elem)[-1], type='string')
    cmds.setAttr(elem + '.vray_redid_multimatte', r)
    cmds.setAttr(elem + '.vray_greenid_multimatte', g)
    cmds.setAttr(elem + '.vray_blueid_multimatte', b)
    cmds.setAttr(elem + '.vray_usematid_multimatte', MID)


def getPlaybackSettings(animDir):
    # get start and end frame numbers from file.
    pubFile = pipelineTools.findPUBLISH(animDir)
    pubFile = os.path.join(animDir, pubFile)
    # setAttr ".b" -type "string" "playbackOptions -min 1 -max 200 -ast 1 -aet 200 ";
    fileContents = pipelineTools.readMA(pubFile)
    for line in fileContents:
        if ' -ast ' in line:
            playbackSettings = line
            return playbackSettings
    raise NameError('playbackOptions not found in {}'.format(pubFile))


def getFrameRange(playbackSettings):
    settingsList = playbackSettings.split(' ')

    ''' example
    
    (0, ' ', u'\tsetAttr')
    (1, ' ', u'".b"')
    (2, ' ', u'-type')
    (3, ' ', u'"string"')
    (4, ' ', u'"playbackOptions')
    (5, ' ', u'-min')
    (6, ' ', u'1')
    (7, ' ', u'-max')
    (8, ' ', u'200')
    (9, ' ', u'-ast')
    (10, ' ', u'1')
    (11, ' ', u'-aet')
    (12, ' ', u'200')
    (13, ' ', u'";')
    '''
    for n, s in enumerate(playbackSettings.split(' ')):
        print n, s

    if settingsList[4] == '"playbackOptions' and settingsList[11] == '-aet':

        return settingsList

    else:

        raise NameError('Misread playbackOptions. Unable to get start and end frames')


def setFrameRange(animDir):
    playbackSettings = getPlaybackSettings(animDir)

    print '\nplaybackSettings:\n{}\n'.format(playbackSettings)

    settingsList = getFrameRange(playbackSettings)

    animMin = settingsList[6]
    animMax = settingsList[8]
    animStart = settingsList[10]
    animEnd = settingsList[12]

    print '\nAnimation:\n    Min = {} \n    Max = {} \n    animationStartTime = {} \n    animationEndTime = {}'.format(animMin, animMax, animStart, animEnd)

    # set time slider and range slider
    cmds.playbackOptions(animationStartTime=animStart, min=animMin)
    cmds.playbackOptions(animationEndTime=animEnd, max=animMax)

    # set render frame range
    cmds.setAttr('defaultRenderGlobals.startFrame', animStart)
    cmds.setAttr('defaultRenderGlobals.endFrame', animEnd)


animDir = None
for dept in os.listdir(shotDirMaya):
    if 'animation' in dept:
        animDir = os.path.join(shotDirMaya, dept)

        break

try:
    animDir
except:
    raise NameError('animation directory not found in...%s\n    ' % shotDirMaya)

if __name__ == '__main__':
    # print('\n{}\n{}\n{}\n'.format(litDir, animDir, newShot))
    buildMA(litDir, animDir, newShot)

'''
    os.system("echo \"crap\" & Pause")
    mayabatch -file someMayaFile.mb -command "file -save"
'''

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
