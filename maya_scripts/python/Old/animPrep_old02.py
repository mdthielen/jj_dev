import os
import re
import sys
import sbtvInfo
import pipelineTools
import animCleanup

#os.environ["MAYA_LOCATION"] = "C:\Program Files\Autodesk\Maya2015"

import maya.standalone 
maya.standalone.initialize( name = 'python' )
import maya.cmds as mc


#ep, seq = raw_input( 'Enter episode and sequence as ### ###: ' ).split(' ')
ep, seq = sys.argv[1:3]
try:
	shot = sys.argv[3]
except: pass

#test variables
#ep, seq = ['101', '100']

def shotTasks(ma):
	print( '\nOpening... \n    %s\n\n' % os.path.split(ma)[-1] )
	mc.file(ma, force = True, open = True)
	animCleanup.all()
	pipelineTools.publish( ma, exportOnly = True )
	pipelineTools.replaceCharRigs(ma)	

seqInfo = sbtvInfo.Info(ep, seq)
seqName = seqInfo.seqName
logFile = os.path.join(seqInfo.seqPath, 'animPrepLog.txt')

orig_sys = sys.stdout
with open(logFile,'w') as out:
    sys.stdout = out
    #test ma file:						
    #ma = os.path.join( seqInfo.seqPath, r'sh_020\03_maya\02_animation\sq100_020_downpour_anim_003.ma')
    for ma in seqInfo.getLastAnim():
        print ma
        try:
            if shot and shot in ma:
                shotTasks(ma)
                break
        except: shotTasks(ma)
    mc.quit()


