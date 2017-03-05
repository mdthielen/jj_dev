'''PUBLISH FILE'''
import maya.cmds as mc
import re
import os


def pubName( currentFile ):# = mc.file(q=1, l=1)[0] ):
    ver = '_?\d+.ma$' #version syntax, in this case, to search for '###.ma'
    pubFile = re.split( ver, currentFile)[0] #remove version suffix
    pubFile += r'PUBLISH.ma' #add PUBLISH suffix
    return pubFile

def publish( currentFile, exportOnly = False ):#= mc.file(q=1, l=1)[0]:
    pubFile = pubName(currentFile)
    #export all as a .ma file, overwrite if existing.
    #mc.file( rename = pubFile)
    if exportOnly == False: 
        #save the current file
        mc.file( save = True , force = True)
        print('Saved %s'%currentFile)
    try:
        mc.file( pubFile, force = 1, options= "v=0;", type= "mayaAscii", pr = 1, ea = 1)
    except:
        print('FAILED TO EXPORT\n%s'%pubFile)
        return
    print('\n*Exported: \n    %s \n\n' % pubFile.split('\\')[-1]) #only works on windows, returns long name on others
    return pubFile
    

'''REPLACE ANIM RIGS WITH VRAY RIGS'''

def replaceCharRigs(currentFile ):#= mc.file(q=1, l=1)[0]):
    pubFile = pubName(currentFile)    
    print( 'Replacing rigs... \n    %s' % pubFile.split('/')[-1] )
    characters = ['Bing', 'Bing', 'Bang', 'Beep', 'Bo', 'Boop']
    molephiusRig = 'Molepheus.ma'
    if '_animation' in pubFile:
        fileContents = readMA(pubFile)
        for i in range(len(fileContents)):
            if '_Rig.ma' in fileContents[i]:
                if len(fileContents[i])<250: print( '%s' % fileContents[i] )
                #fileContents[i] = fileContents[i].replace('_Rig.ma', '_Rig_Vray.ma')
                for char in characters:
                    fileContents[i] = fileContents[i].replace(char + '_Rig.ma', char + '_Rig_Vray.ma')
                if len(fileContents[i])<255: print( '%s\n' % fileContents[i] )
            elif molephiusRig in fileContents[i]:
                if len(fileContents[i])<250: print( '%s' % fileContents[i] )
                fileContents[i] = fileContents[i].replace( molephiusRig, 'Molepheus_Vray.ma') 
                if len(fileContents[i])<255: print( '%s\n' % fileContents[i] )
        mayaFile = open(pubFile, 'w')
        mayaFile.writelines(fileContents)
        mayaFile.close()
    else: print 'please run from a versioned animation file'

def readMA(maFile):    
    mayaFile = open(maFile, 'r')
    fileContents = mayaFile.readlines()#.splitlines()    
    mayaFile.close()
    return fileContents

def writeMA(maFile, fileContents):
    mayaFile = open(maFile, 'w')
    mayaFile.writelines(fileContents)
    mayaFile.close()

def findPUBLISH(sourcePath):
    srcPub = [ f for f in os.listdir( sourcePath ) if 'PUBLISH.ma' in f ]
    if len(srcPub) < 1:
        import sys
        sys.exit('No publish file present. \n  Check for a \'PUBLISH\' file in:\n  %s'%sourcePath)
    elif len(srcPub) > 1:
        import sys
        sys.exit ('More than one publish file present. \n  Clean up directory:\n  %s'%sourcePath)
    else: return srcPub[0]

def importRef(sourcePath):
    #print 'sourcePath:\n  ', sourcePath
    srcPub = findPUBLISH( sourcePath )    
    #print 'srcPub:\n  ', srcPub
    srcPubFP = os.path.join( sourcePath, srcPub )
    #print 'srcPubFP:\n  ', srcPubFP
    #return
    if os.path.isfile(srcPubFP): 
        print '\nImporting reference from...\n    ', srcPubFP
        mc.file( srcPubFP, mergeNamespacesOnClash = 1, reference = 1, namespace = ':')
    else: raise NameError('could not find:\n    ' + srcPubFP)
                        
