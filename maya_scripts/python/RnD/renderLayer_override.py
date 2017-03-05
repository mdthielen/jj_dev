rlCME = cmds.createRenderLayer( cmds.ls(sl=1), name='CME', nr = 1)
matteNode = 'surfaceShader'
bMatte = cmds.shadingNode( matteNode, asShader = 1, n = 'matteBlue_mtl')
cmds.setAttr( bMatte+'.outColor', 0, 0, 1, type = 'double3')

#single render layer
eye_R_geoShape.instObjGroups[0] -> blinn1SG.dagSetMembers[0]
#new renderlayer with objects, no overrides
CME.renderInfo -> eye_R_geo.renderLayerInfo[0]
'''
connectAttr -f matteBlue_mtl.outColor matteBlue_mtlSG.surfaceShader;
sets -e -forceElement matteBlue_mtlSG;
'''
#override masterLayer
eye_R_geoShape.instObjGroups[0] -> blinn1SG.dagSetMembers[3]
defaultRenderLayer.outAdjustments[0].outValue -> blinn1SG.dagSetMembers[2]
#override CME
eye_R_geoShape.instObjGroups[0] -> matteBlue_mtlSG.dagSetMembers[2]
CME.outAdjustments[0].outValue -> matteBlue_mtlSG.dagSetMembers[1]
#override shared
eye_R_geoShape.instObjGroups[0] -> CME.outAdjustments[0].outPlug
eye_R_geoShape.instObjGroups[0] -> defaultRenderLayer.outAdjustments[0].outPlug


''''''
cme_attr = cmds.listAttr('CME')
connections = cmds.listConnections('matteBlue_mtlSG', type = 'mesh')
connections = cmds.listConnections('CME', t = 'transform')

allGeo = []
for c in connections: 
    for d in cmds.listRelatives(c, ad=1,type='mesh'):
        allGeo.append(d)
for geo in allGeo:
    if 'pupil' in geo: allGeo.remove(geo)
pupils = [geo for geo in allGeo if 'pupil' in geo]
for p in pupils:
    cmds.select(p, add = 1)
    cmds.select([p for p in pupils], add = 1)
#if allGeo[0] == '*brow*': print 'match'
#else: print 'no match'
#    if geo == '*eye*'
matching = [s for s in allGeo if 'eye' in s]
ta = allGeo[0]       
any('eye' in ta)

for at in cme_attr: print at
CME.outAdjustments.outValue
.dagSetMembers
cmds.connectAttr(rl,SG,na=1)


#Create render layer for eye masks
rlCME = cmds.createRenderLayer( charAll, name='CME', nr = 1)

#Create mattes
matteNode = 'surfaceShader'
rMatte = cmds.shadingNode( matteNode, asShader = 1, n = 'matteRed_mtl')
cmds.setAttr( rMatte+'.outColor', 1, 0, 0, type = 'double3')
gMatte = cmds.shadingNode( matteNode, asShader = 1, n = 'matteGreen_mtl')
cmds.setAttr( gMatte+'.outColor', 0, 1, 0, type = 'double3')
bMatte = cmds.shadingNode( matteNode, asShader = 1, n = 'matteBlue_mtl')
cmds.setAttr( bMatte+'.outColor', 0, 0, 1, type = 'double3')