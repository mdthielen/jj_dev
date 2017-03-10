#!/usr/bin/python

"""
Animation prep

Cleans, publishes, and replaces character rigs in maya file. Runs through all shots in a sequence.

Attributes:
    Accepts episode and sequence as input.
    
Todo:
    
    
"""

import os
import sys

# todo-mark not finding standalone. Does this need to be run from command line?
import maya.standalone
import maya.cmds as cmds

import animCleanup
import pipelineTools
import sbtvInfo

maya.standalone.initialize(name='python')

# ep, seq = raw_input( 'Enter episode and sequence as ### ###: ' ).split(' ')
try:
    ep, seq = sys.argv[1:3]
except ValueError:
    ep, seq = raw_input('Enter episode, sequence as ### ###: ').split(' ')

try:
    shot = sys.argv[3]  # todo-mark this is failing
except ValueError:
    pass


# test variables
# ep, seq = ['101', '100']

def shotTasks(ma_file):
    """
    Cleans, publishes, and replaces character rigs in maya file.
    :param ma_file: mayaAscii file for shot
    """
    print('\nOpening... \n    %s\n\n' % os.path.split(ma_file)[-1])
    # print(ma_file)
    cmds.file(ma_file, force=True, open=True)
    animCleanup.cleanAll()
    pipelineTools.publish(ma_file)
    pipelineTools.replaceCharRigs(ma_file)


seqInfo = sbtvInfo.Info(ep, seq)
print('seqInfo: \n\t{}'.format(seqInfo))
seqName = seqInfo.seqName
print('seqName: \n\t{}'.format(seqName))
logFile = os.path.join(seqInfo.seqPath, 'animPrepLog.txt')

orig_sys = sys.stdout
with open(logFile, 'w') as out:
    sys.stdout = out
    # test last_anim file:
    # last_anim = os.path.join( seqInfo.seqPath, r'sh_020\03_maya\02_animation\sq100_020_downpour_anim_003.ma')
    for last_anim in seqInfo.getLastAnim():
        print last_anim
        shotTasks(last_anim)
        '''
        try:
            if shot and shot in last_anim:
                shotTasks(last_anim)
                break
        except: shotTasks(last_anim)
        '''
    cmds.quit()

__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/9/17"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
