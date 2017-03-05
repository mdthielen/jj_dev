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

seqInfo = sbtvInfo.Info(ep, seq, shot)
seqPath = seqInfo.seqPath
seqName = seqInfo.seqName

#episode, sequence, shot ID - to be used for output directory
essid = r'/'.join([seqInfo.epID, seqInfo.seqID, 'sh_' + shot, '<Layer>'])



shotDirMaya = os.path.join(seqPath, shot, '03_maya') #sh removed for ep 103 seq 020

for dept in os.listdir(shotDirMaya):

    if 'lighting' in dept: 
    
        litDir = os.path.join(shotDirMaya, dept)
        
    else: 
        
        pass
        #NameError('lighting directory not found in...%s\n    '%shotDirMaya)
    
    
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
    
    import pipelineTools
    
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

'''
#creating render elements. (might only work in gui, not batch)
import maya.mel
maya.mel.eval('vrayAddRenderElement( "MultiMatteElement" );')
'''

for dept in os.listdir(shotDirMaya):
    if 'animation' in dept: 
        animDir = os.path.join(shotDirMaya, dept)
    else: NameError('animation directory not found in...%s\n    '%shotDirMaya)

    
print('\n{}\n{}\n{}\n'.format(litDir, animDir, newShot))    
if __name__ == '__main__':
    buildMA(litDir, animDir, newShot)


'''
retrieving render range info from MA:
createNode script -n "sceneConfigurationScriptNode";
    setAttr ".b" -type "string" "playbackOptions -min 1 -max 99 -ast 1 -aet 99 ";
'''


'''
    os.system("echo \"crap\" & Pause")
    mayabatch -file someMayaFile.mb -command "file -save"
'''
