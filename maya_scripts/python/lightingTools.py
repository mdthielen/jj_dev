#!/usr/bin/python
"""
Lighting tools
VRay lighting and subdivision surfaces tools
use these on lightingTools shelf

Attributes:
    
    
Todo:
    
    
"""


import maya.cmds as cmds

maLightTypes = ['VRayLightDomeShape',
                'VRayLightIESShape',
                'VRayLightMesh',
                'VRayLightMtl',
                'VRayLightRectShape',
                'VRayLightSphereShape',
                'VRayPluginNodeLightShape',
                'VRaySunShape',
                'ambientLight',
                'areaLight',
                'directionalLight',
                'pointLight',
                'spotLight',
                'volumeLight']


def getShapeNodesList(all_in_heirarchy=False):
    """
    Get shape nodes list from selected or all geometry shape nodes if nothing is selected.
    
    :rtype: shapes: list of all geometry shape nodes
    :type all_in_heirarchy: select all geometry shape nodes in heirarchy based on anything selected in heirarchy 
    """
    if all_in_heirarchy:
        pass

    if cmds.ls(sl=1):
        transforms = cmds.ls(sl=1)
        shapes = cmds.listRelatives(transforms)
    else:
        shapes = cmds.ls(type='geometryShape')

    return shapes


def addVrayOsd(userDepth=2):
    """
    Add VRay open subdivision surface to shape nodes
    :param userDepth: default 2, subdivision depth
    """

    shapes = cmds.ls(sl=1, dag=1, lf=1, s=1)
    for shape in shapes:
        cmds.vray("addAttributesFromGroup", shape, "vray_opensubdiv", 1)
        cmds.setAttr(shape + '.vrayOsdSubdivDepth', userDepth)


def addVrayOID():
    """
    Add VRay object ID to all selected nodes
    """

    shapes = cmds.ls(sl=1, dag=1, lf=1, s=1)
    for shape in shapes:
        cmds.vray("addAttributesFromGroup", shape, "vray_objectID", 1)


def selVrayOsd():
    """
    Select VRay Osd shape nodes either from selection or if nothing selected, then parse all scene elements.
    
    :param : none
    """

    shapes = getShapeNodesList()
    cmds.select(cl=1)
    if shapes:
        for shape in shapes:
            if cmds.attributeQuery('vrayOsdSubdivEnable', node=shape, exists=True):
                cmds.select(shape, add=True)
        if cmds.ls(sl=1):
            print('\nSelected shapes with vrayOsdSubdivEnable on:')
            for sel in cmds.ls(sl=1):
                print sel
    else:
        print('No shapes found')


def toggleVrayOsd(force_all=False, force_toggle=1):
    """
    Toggle VRay Osd shape nodes to be opposite of current setting.
    
    :param force_toggle: set toggle to be 1 or 0 if force_all is True
    :param force_all: This will force all to be on or off
    """

    sel_start = cmds.ls(sl=1)
    shapes = getShapeNodesList()
    cmds.select(cl=1)
    if shapes:
        print('Toogle VRay Osd:')
        for shape in shapes:
            if cmds.attributeQuery('vrayOsdSubdivEnable', node=shape, exists=True):
                if force_all:
                    newstate = force_toggle
                else:
                    newstate = not cmds.getAttr(shape + '.vrayOsdSubdivEnable')
                print ('VRay Osd: {} -->  {}'.format(int(newstate), shape))
                cmds.setAttr(shape + '.vrayOsdSubdivEnable', newstate)
    else:
        print('No shapes found')
    cmds.select(sel_start)


def checkSelectedLights(sel=cmds.ls(sl=1)):
    """
    use to check if the selection matches the light types defined in maLightTypes
    :param sel: selected lights
    :return: light shapes and lights not using predefined light types
    """

    ltShapes = []
    badEgg = None

    for obj in sel:
        shape = cmds.listRelatives(obj, s=1)
        if cmds.objectType(shape) in maLightTypes:
            ltShapes.append(shape)
        else:
            badEgg = True
            break

    return ltShapes, badEgg


def listAllLights(ltShapes):
    """
    gather all lights as defined by the maLightTypes
    :param ltShapes: light shape nodes
    :return: light shapes of type maLightTypes
    """
    for t in maLightTypes:
        [ltShapes.append(x) for x in cmds.ls(type=t)]

    return ltShapes


def mkLightElem(ltShapes):
    """
    Make render element for lights
    :param ltShapes: selected light shape nodes
    """
    import maya.mel

    for lt in ltShapes:
        ltTran = cmds.listRelatives(lt, p=1)[0]
        elem = 'vrayRE_' + ltTran
        maya.mel.eval('vrayAddRenderElement( "LightSelectElement" );')
        cmds.rename('vrayRE_Light_Select', elem)
        cmds.setAttr(elem + '.vray_name_lightselect', 'lt_' + ltTran, type='string')
        cmds.sets(ltTran, addElement=elem)


def autoCreateLightElem():
    """
    Auto create render element for lights
    """
    ltShapes, badEgg = checkSelectedLights()

    if badEgg:
        cmds.warning('Selection contains unrecognised light types')
    elif ltShapes:
        mkLightElem(ltShapes)
    elif not ltShapes:
        result = cmds.confirmDialog(
                title='Create VRay Light Element(s)',
                message='No light selected, create elements for all lights in the scene?',
                button=['Yes', 'No'],
                defaultButton='No', cancelButton='No', dismissString='No')

        if result == 'Yes':
            ltShapes = listAllLights(ltShapes)
            mkLightElem(ltShapes)


def characterEyes():
    """
    Find all main character pupils
    :return: charEyes all pupils
    """
    import re

    visMesh = cmds.ls(et="mesh", v=1)
    characters = ["bang", "boop", "bing", "bo", "beep"]
    leftEyePattern = "_lpupil|_l_.*pupil"
    rightEyePattern = "_rpupil|_r_.*pupil"
    charEyes = []

    for mesh in visMesh:
        for char in characters:
            if re.search(char + "_.*pupil", mesh, re.I) and not re.search("orig$|rig1$", mesh, re.I):
                if re.search(leftEyePattern, mesh, re.I):  # LEFT EYES
                    charEyes.append([mesh, char + "_R_eyeSpec"])  # pair rig-left with screen-right

                if re.search(rightEyePattern, mesh, re.I):  # RIGHT EYES
                    charEyes.append([mesh, char + "_L_eyeSpec"])  # pair rig-right with screen-left
    return charEyes


def createLightAndLink(mesh, lightName):  #
    """
    create vray dome with a disc and link it only to the mesh objects.
    :param mesh: multiple meshes can be used with the syntax: ( "obj1", "obj2", "obj3" )
    :param lightName: light to link to
    :return: newDome, newRamp: new light dome and new ramp on dome
    """
    lightShape = lightName + "Shape"

    # create a vray dome
    newDome = cmds.shadingNode("VRayLightDomeShape", asLight=True, name=lightShape)

    # set the dome attributes
    cmds.setAttr(lightShape + ".intensityMult", 10)
    cmds.setAttr(lightShape + ".shadows", 0)
    cmds.setAttr(lightShape + ".useDomeTex", 1)
    ###
    cmds.setAttr(lightShape + ".invisible", 1)
    cmds.setAttr(lightShape + ".affectDiffuse", 0)
    cmds.setAttr(lightShape + ".affectSpecular", 1)
    cmds.setAttr(lightShape + ".affectReflections", 0)
    cmds.setAttr(lightShape + ".affectAlpha", 0)

    # create ramp texture
    newRamp = cmds.shadingNode("ramp", asTexture=True, name=lightName + "_Ramp")
    placeTex = cmds.shadingNode("VRayPlaceEnvTex", asUtility=True, name=lightName + "_VRayPlaceEnvTex")
    cmds.setAttr(placeTex + ".mappingType", 2)
    cmds.setAttr(placeTex + ".useTransform", 1)

    # first ramp point
    cmds.setAttr(newRamp + ".colorEntryList[0].position", 0.96)
    cmds.setAttr(newRamp + ".colorEntryList[0].color", 0, 0, 0, type="double3")
    # second ramp point
    cmds.setAttr(newRamp + ".colorEntryList[1].position", 0.97)
    cmds.setAttr(newRamp + ".colorEntryList[1].color", 1, 1, 1, type="double3")

    # Connect texture
    cmds.connectAttr(newRamp + ".outColor", lightShape + ".domeTex", force=True)
    cmds.connectAttr(placeTex + ".outUV", newRamp + ".uvCoord", force=True)
    cmds.connectAttr(lightShape + ".worldMatrix[0]", placeTex + ".transform")

    # Break light links with everything but the mesh(s)
    cmds.lightlink(b=True, light=newDome, object=cmds.ls())
    cmds.lightlink(make=True, light=newDome, object=mesh)

    return newDome, newRamp


def buildEyeLights():
    """
    Build eye lights for all main characters
    """
    # Get main character pupils
    charEyes = characterEyes()

    # Create light and link to pupils
    for eye in charEyes:
        createLightAndLink(eye[0], eye[1])


def lightingCleanup():
    """
    Lighting cleanup
    """
    charAll = ['Bing_Riglocator', 'Beep_Riglocator', 'Bo_Riglocator', 'Boop_Riglocator', 'Bang_Riglocator']
    for char in charAll:
        cmds.editRenderLayerMembers('shd', char, noRecurse=1)
    cmds.editRenderLayerMembers('shd', 'SHD_GEO_GRP', noRecurse=1)
    cmds.select('SHD_GEO_GRP', r=1)
    newShdGrp = cmds.duplicate(rr=1)[0]
    children = cmds.listRelatives(newShdGrp, c=1)
    for c in children:
        shd = cmds.rename(newShdGrp + '|' + c, c + '_shd')
        noVis = cmds.duplicate(shd, n=c + '_noVis', rr=1)[0]
        cmds.setAttr(noVis + '.primaryVisibility', 0)
        cmds.sets(shd, addElement='groundPlane_shd_vrayobjectproperties')
        if not cmds.objExists('groundPlane_noVis_set'):
            cmds.sets(noVis, n='groundPlane_noVis_set')
        else:
            cmds.sets(noVis, add='groundPlane_noVis_set')
        cmds.hide(shd)
    cmds.hide('SHD_GEO_GRP')


__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/6/2017"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
