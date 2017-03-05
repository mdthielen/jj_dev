#shotDirMaya variable modified on 12/3/2015 to accomodate an inproperly named directory structure
#changed again on 1/20/2016 to accomodate 01_maya directory of old 102/070 directory naming
#changed again on 1/30/2016 to accomodate 103/040 artist directory structure

import os
from sys import argv
import re

try: ep, seq, shot = argv[1:]
except: ep, seq, shot = raw_input( 'enter episode, sequence, shot as ### ### ###: ' ).split(' ')
#test input
#ep, seq, shot = ['101', '100', '120']
print 'ep  =', ep
print 'seq =', seq
print 'shot=', shot

#os.environ["MAYA_LOCATION"] = "C:\Program Files\Autodesk\Maya2015"
import maya.standalone 
maya.standalone.initialize( name = 'python' )
import maya.cmds as mc


import sbtvInfo

import pipelineTools

seqInfo = sbtvInfo.Info(ep, seq, shot)
seqPath = seqInfo.seqPath
seqName = seqInfo.seqName

#episode, sequence, shot ID - to be used for output directory
essid = r'/'.join([seqInfo.epID, seqInfo.seqID, 'sh_' + shot, '<Layer>'])

for x in os.listdir(seqPath):
    
    if 'sh_' in x:
        
        shotDirMaya = os.path.join(seqPath, 'sh_' + shot, '03_maya')
        
        break
        
else:

    shotDirMaya = os.path.join(seqPath, shot, '03_maya')


for dept in os.listdir(shotDirMaya):

    if 'lighting' in dept: 
    
        litDir = os.path.join(shotDirMaya, dept)
        
    else: 
        
        pass
        #raise NameError('lighting directory not found in...%s\n    '%shotDirMaya)
    
    
try:

    litDir
    
except:
    
    dept = raw_input( 'Enter lighting folder name [05_lighting]: ' ) or '05_lighting'
    
    litDir = os.path.join(shotDirMaya, dept)
    
    os.makedirs( litDir )


newShot = '_'.join( ['sq' + seq, shot, seqName, 'lit.0001.ma'] )

'''
#Moved to pipelineTools.py
def importRef(sourcePath):

    #curFile = mc.file(q=1, l=1)[0] #not needed?
    srcPub = [ f for f in os.listdir( sourcePath ) if 'PUBLISH' in f ]
    
    if len(srcPub) == 1:
        srcPubFP = os.path.join( sourcePath, srcPub[0] )
        if os.path.isfile(srcPubFP): 
            print '\nImporting reference from...\n    ', srcPubFP
            mc.file( srcPubFP, mergeNamespacesOnClash = 1, reference = 1, namespace = ':')
        else: raise NameError('could not find:\n    ' + srcPubFP)
    elif len(srcPub) < 1:
        StandardError ('No publish file present. \n    \
                        Check for a \'PUBLISH\' file in:\n    \
                        %s'%sourcePath)
    elif len(srcPub) > 1:
        StandardError ('More than one publish file present. \n    \
                        Clean up directory:\n    \
                        %s'%sourcePath)
'''

def buildMA(destDir, sourcePath, newShot):
    
    newFile = os.path.join( destDir, newShot )
    
    if os.path.isfile( newFile ):
        #raise  StandardError('this file already exists')
        startStop = raw_input('\n' + newFile +'\n\nAlready exists. Overwrite? (y/n):')
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
    
    mc.file(rename = newFile)
    mc.file( type = 'mayaAscii')
    
    pipelineTools.importRef(sourcePath)
    
    lightingBasics(essid)
    
    setFrameRange( animDir )
    
    mc.file( save = True, force = True, type = 'mayaAscii')
    print '\nSaved', newFile
    
    mc.quit()

def lightingBasics( essid = None ): #episode, sequence, shot ID

    #set renderer to vray
    mc.loadPlugin( "vrayformaya.mll" )
    mc.setAttr( "defaultRenderGlobals.currentRenderer", "vray", type = "string" )

    #on unix systems, the vray renderGlobals are not loading, therefore vraySettings cannot be set.

    #set output directory
    if essid:
        try: mc.setAttr( "vraySettings.fileNamePrefix", essid, type = "string" )
        except: pass
    #set output format
    if mc.optionMenuGrp( "vrayImageFormatMenu", exists = 1):
        mc.setAttr("vraySettings.imageFormatStr", "exr", type = "string" )
    #Disable persp camera
    mc.setAttr( "perspShape.renderable", 0 )
    #set render resolution
    try: 
        mc.setAttr( "vraySettings.width", 1920 )
        mc.setAttr( "vraySettings.height", 1080 )
        mc.setAttr( "defaultRenderGlobals.animation", 1 )
        mc.setAttr( "vraySettings.animBatchOnly", 1 )
    except:
        mc.setAttr( "defaultResolution.width", 1920 )
        mc.setAttr( "defaultResolution.height", 1080 )

    
    #setup render elements
    import maya.mel
    matteElements = ['vrayRE_Multi_Matte0',
                    'vrayRE_Multi_Matte1',
                    'vrayRE_Multi_Matte2']
    i = 1
    for elem in matteElements:
        maya.mel.eval('vrayAddRenderElement( "MultiMatteElement" );')
        mc.rename( 'vrayRE_Multi_Matte', elem )
        mc.setAttr( elem + '.vray_name_multimatte', re.split('_', elem)[-1], type = 'string' )
        mc.setAttr( elem + '.vray_redid_multimatte', i ); i += 1
        mc.setAttr( elem + '.vray_greenid_multimatte', i ); i += 1
        mc.setAttr( elem + '.vray_blueid_multimatte', i ); i += 1
        mc.setAttr( elem + '.vray_usematid_multimatte', 1 )
    createMultiMattes( 'vrayRE_matteChar1', 3, 2, 1 )
    createMultiMattes( 'vrayRE_matteChar2', 5, 4, 0 )
    createMultiMattes( 'vrayRE_matteCharEyesL', 11, 12, 13, 1)
    createMultiMattes( 'vrayRE_matteCharEyesR', 14, 15, 16, 1)
    maya.mel.eval( 'vrayAddRenderElement( "diffuseChannel" );')
    maya.mel.eval( 'vrayAddRenderElement( "giChannel" );')
    maya.mel.eval( 'vrayAddRenderElement( "velocityChannel" );')
    maya.mel.eval( 'vrayAddRenderElement( "zdepthChannel" );')
    maya.mel.eval( 'vrayAddRenderElement( "specularChannel" );')
    
    #turn off default image plane
    try: mc.setAttr( 'imagePlaneShape1.displayMode', 0 )
    except: pass
    
    #delete unknown nodes
    unknownNodes = mc.ls( type = 'unknown')
    try:
        if unknownNodes:
            print "Deleting..."
            for n in unknownNodes:
                mc.delete(n)
                print('    ' + n )
    except: print 'No unknown nodes found'
                

        
def createMultiMattes(elem, r, g, b, MID = 0):
    import maya.mel
    maya.mel.eval('vrayAddRenderElement( "MultiMatteElement" );')
    mc.rename( 'vrayRE_Multi_Matte', elem )
    mc.setAttr( elem + '.vray_name_multimatte', re.split('_', elem)[-1], type = 'string' )
    mc.setAttr( elem + '.vray_redid_multimatte', r ); 
    mc.setAttr( elem + '.vray_greenid_multimatte', g ); 
    mc.setAttr( elem + '.vray_blueid_multimatte', b ); 
    mc.setAttr( elem + '.vray_usematid_multimatte', MID )

    
def getPlaybackSettings( animDir ):
    #get start and end frame numbers from file.
    pubFile = pipelineTools.findPUBLISH( animDir )
    pubFile = os.path.join( animDir, pubFile )
    #setAttr ".b" -type "string" "playbackOptions -min 1 -max 200 -ast 1 -aet 200 ";
    fileContents = pipelineTools.readMA(pubFile)
    for line in fileContents:
        if ' -ast ' in line:
            playbackSettings = line
            return playbackSettings
    raise NameError( 'playbackOptions not found in {}'.format( pubFile ) )

    
def getFrameRange( playbackSettings ):
    
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
    for n, s in enumerate(playbackSettings.split(' ')): print n, s

    if settingsList[4] == '"playbackOptions' and settingsList[11] == '-aet': 

        return settingsList
           
    else:

        raise NameError('Misread playbackOptions. Unable to get start and end frames')
    

    
    
def setFrameRange( animDir ): 
    
    playbackSettings = getPlaybackSettings( animDir )
    
    print '\nplaybackSettings:\n{}\n'.format( playbackSettings )
    
    settingsList = getFrameRange( playbackSettings )
    
    animMin = settingsList[6]    
    animMax = settingsList[8]    
    animStart = settingsList[10]    
    animEnd = settingsList[12]
    
    print '\nAnimation:\n    Min = {} \n    Max = {} \n    animationStartTime = {} \n    animationEndTime = {}'.format( animMin, animMax, animStart, animEnd )
    
    #set time slider and range slider
    mc.playbackOptions( animationStartTime = animStart, min = animMin )
    mc.playbackOptions( animationEndTime = animEnd, max = animMax )
    
    #set render frame range
    mc.setAttr( 'defaultRenderGlobals.startFrame', animStart )
    mc.setAttr( 'defaultRenderGlobals.endFrame', animEnd )

    
    
for dept in os.listdir(shotDirMaya):
    if 'animation' in dept: 
    
        animDir = os.path.join(shotDirMaya, dept)
        
        break
        
try: animDir    
except: raise NameError('animation directory not found in...%s\n    '%shotDirMaya)

    
 
if __name__ == '__main__':
    #print('\n{}\n{}\n{}\n'.format(litDir, animDir, newShot))   
    buildMA(litDir, animDir, newShot)



'''
    os.system("echo \"crap\" & Pause")
    mayabatch -file someMayaFile.mb -command "file -save"
'''
