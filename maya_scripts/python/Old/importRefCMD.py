import maya.cmds as mc
try: reload(lightingSetup)
except: import lightingSetup
lightingSetup.importRef()
try: reload(pipelineTools)
except: import pipelineTools
pipelineTools.publish()