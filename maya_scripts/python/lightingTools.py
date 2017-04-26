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
    cmds.playbackOptions()
    return ltShapes


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


def buildEyeLights():
    """
    Build eye lights for all main characters
    """
    print('\nJib Jab - buildEyeLights:')
    sel_before_starting = cmds.ls(sl=1, l=1)
    # Get main character pupils
    eyes = characterEyes()

    # Create light and link to pupils
    print('\nBegin create lights and light linking:')

    for eye in eyes:
        createLightAndLink(eye[0], eye[1])

    cmds.select(sel_before_starting, r=1)
    print('Jib Jab - buildEyeLights COMPLETE')


def characterEyes():
    """
    Find all main character pupils
    :return: charEyes all pupils
    """

    import re

    print('Searching for eye geo and existing eye light rigs:')

    eyes_visible = cmds.ls('*eye_*GEO', et='transform', v=1, l=1)
    characters = ["bang", "boop", "bing", "bo", "beep"]

    charEyes = []
    eye_lights_old_char = []

    for char in characters:
        for mesh in eyes_visible:

            # Test if old light rig exists
            update_eye_lights = 'Yes'
            eye_lights_old = cmds.ls('*ye_*pec_LGT*', v=1, type='transform', l=1)

            if eye_lights_old:
                light_old_exists = False
                for light_old in eye_lights_old:
                    if char in light_old:
                        light_old_exists = True
                        eye_lights_old_char.append(light_old)
                if light_old_exists:
                    # Ask to update eye light rig
                    update_eye_lights = cmds.confirmDialog(title='Replace current eye lights for {}'.format(char),
                                                           message='Are you sure?',
                                                           button=['Yes', 'No'],
                                                           defaultButton='Yes',
                                                           cancelButton='No',
                                                           dismissString='No')
                    if update_eye_lights == 'Yes':
                        if eye_lights_old_char:
                            # Ask to delete old rig
                            confirm_delete_lights = cmds.confirmDialog(title='Delete light setup for {}'.format(char),
                                                                       message='Are you sure?',
                                                                       button=['Yes', 'No'],
                                                                       defaultButton='Yes',
                                                                       cancelButton='No',
                                                                       dismissString='No')
                            if confirm_delete_lights == 'Yes':
                                for light_old_del in eye_lights_old_char:
                                    if cmds.objExists(light_old_del):
                                        cmds.delete(light_old_del)
                                old_groups = cmds.ls('*LGT_GRP', l=1)

                                # Look for old Spec_LGT_GRP nodes in char to delete
                                if old_groups:
                                    for group in old_groups:
                                        if char in group:
                                            if cmds.objExists(group):
                                                cmds.delete(group)
            # Create running list of all geo and lights for eye light
            if update_eye_lights == 'Yes':
                if re.search('{}_L'.format(char), mesh, re.IGNORECASE):  # LEFT EYES
                    charEyes.append([mesh, '{}_L_eye_spec_LGT'.format(char)])
                    print('Found L_eye:   {}'.format(mesh))
                if re.search('{}_R'.format(char), mesh, re.IGNORECASE):  # RIGHT EYES
                    charEyes.append([mesh, '{}_R_eye_spec_LGT'.format(char)])
                    print('Found R_eye:   {}'.format(mesh))

    return charEyes


def createLightAndLink(mesh, lightName, dome=False, rect=True):  #
    """
    create vray dome with a disc and link it only to the mesh objects.
    :param dome: specify to create a dome light for the eyes. Default is False
    :param rect: specify to create a Rect light for the eyes. Default is True
    :param mesh: multiple meshes can be used with the syntax: ( "obj1", "obj2", "obj3" )
    :param lightName: light to link to
    :return: new_eye_light, newRamp: new light (dome or rect) and new ramp on dome
    """

    lightShape = lightName + "Shape"
    char = lightName.split('_')[0]
    eye_group = '{}_eye_spec_LGT_GRP'.format(char)
    if not cmds.objExists(eye_group):
        cmds.group(empty=1, parent='{}'.format(char), name=eye_group)
        cmds.parentConstraint('{}_ROOTC'.format(char), eye_group)
    eye_group_longname = cmds.ls(eye_group, l=1)[0]
    new_eye_light = None

    if dome:
        # create a vray dome
        new_eye_light = cmds.shadingNode("VRayLightDomeShape", asLight=True, name=lightShape)
        cmds.parent(new_eye_light, eye_group_longname)
        print('Created VRay Light Dome light:   {}'.format(new_eye_light))

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

        print('Set attributes for:   {}'.format(new_eye_light))

    elif rect:
        # Create Groups for L and R eye light
        light_group = cmds.group(empty=1, parent=eye_group, name='{}_GRP'.format(lightShape.split('Shape')[0]))

        # Create VRay Light Rect
        new_eye_light = cmds.shadingNode("VRayLightRectShape", asLight=True, name=lightShape)
        cmds.parent(new_eye_light, light_group)
        cmds.xform(new_eye_light, t=[0, 0, 0], ro=[0, 0, 0], s=[1, 1, 1])
        print('Created VRay Light Rect:   {}'.format(new_eye_light))

        # set the rect attributes

        # Transform Left
        if '_L_' in light_group:
            cmds.setAttr(light_group + ".tx", -2.5, l=1)
            cmds.setAttr(light_group + ".ty", 10, l=1)
            cmds.setAttr(light_group + ".tz", 8, l=1)
            cmds.setAttr(light_group + ".rx", -5, l=1)
            cmds.setAttr(light_group + ".ry", -24, l=1)
            cmds.setAttr(light_group + ".rz", -0.75, l=1)
            cmds.setAttr(light_group + ".sx", 1.6, l=1)
            cmds.setAttr(light_group + ".sy", 1.6, l=1)
            cmds.setAttr(light_group + ".sz", 1.6, l=1)

        # Transform Right
        if '_R_' in light_group:
            cmds.setAttr(light_group + ".tx", -8, l=1)
            cmds.setAttr(light_group + ".ty", 10, l=1)
            cmds.setAttr(light_group + ".tz", 6, l=1)
            cmds.setAttr(light_group + ".rx", -5, l=1)
            cmds.setAttr(light_group + ".ry", -24, l=1)
            cmds.setAttr(light_group + ".rz", -3, l=1)
            cmds.setAttr(light_group + ".sx", 1.6, l=1)
            cmds.setAttr(light_group + ".sy", 1.6, l=1)
            cmds.setAttr(light_group + ".sz", 1.6, l=1)

        # Basic parameters
        cmds.setAttr(lightShape + ".intensityMult", 38.889)
        cmds.setAttr(lightShape + ".shapeType", 1)

        # Options
        cmds.setAttr(lightShape + ".invisible", 1)
        cmds.setAttr(lightShape + ".affectDiffuse", 0)
        cmds.setAttr(lightShape + ".affectSpecular", 1)
        cmds.setAttr(lightShape + ".affectReflections", 1)

        # shadows
        cmds.setAttr(lightShape + ".shadows", 1)
        cmds.setAttr(lightShape + ".shadowBias", 0.02)

        print('Set attributes for: {}'.format(new_eye_light))

    # Break light links with everything but the mesh(s)
    print('Light linking:')
    if new_eye_light:
        cmds.lightlink(b=True, light=new_eye_light, object=cmds.ls())
        cmds.lightlink(make=True, light=new_eye_light, object=mesh)
        print ('Linked\t{}  --->  {}'.format(new_eye_light, mesh))
        for mat in cmds.ls(materials=1):
            import re
            shading_group = cmds.listConnections(mat, d=1, type='shadingEngine')[0]
            if re.search(char, mat, re.IGNORECASE):
                cmds.lightlink(make=True, light=new_eye_light, object=shading_group)
                print ('Linked\t{}  --->  {}'.format(new_eye_light, shading_group))


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


def selGEO(prefix='', shapes=True, transforms=False, suffix='GEO'):
    """
    Select transform or shape nodes.
    
    Can specify a character, all characters, selected nodes, or if nothing selected then the whole scene.
    The search will go through the heirarchies of which ever is specified.
    If a character is given, search will happen only with the prefix of that character.
    
    :type suffix: default is GEO. This would be the suffix of a transform node.
    :param prefix: None is default. Name of character can be passed. All or all can be passed to select all characters.
    :param shapes: True is default. Select shape nodes of character.
    :param transforms: False is default. Select transforms of character.
    """

    print('\nJib Jab - selGEO:')

    geo_type_shapes = '{}Shape\\b'.format(suffix)
    geo_type_transforms = '{}\\b'.format(suffix)

    parents = []
    if 'all' == prefix.lower():
        parents = ['beep', 'bing', 'bang', 'boop', 'bo']
        print('Searching for all characters: {}'.format(parents))
    elif prefix != '':
        parents = [prefix]
        print('Searching for: {}'.format(prefix))
    elif cmds.ls(sl=1):
        for sel in cmds.ls(sl=1, l=1):
            parent = sel.split('|')[1]
            if suffix in parent:
                parent = parent.split(suffix)[0].rstrip('_')
            if parent not in parents:
                parents.append(parent)
    else:
        parents.append(prefix)

    cmds.select(cl=1)
    import re

    for parent in parents:
        sel_added = False

        # Setup regular expression search pattern
        if cmds.listRelatives(cmds.ls('{}*:*{}'.format(parent, suffix), l=1) + cmds.ls('{}*{}'.format(parent, suffix), l=1), s=0, f=1):
            if shapes:
                regex_search_shapes = '{}[_:|A-Za-z].*({})'.format(parent, geo_type_shapes)
                for item in cmds.listRelatives(cmds.ls('{}*:*{}'.format('', suffix), l=1) + cmds.ls('{}*{}'.format('', suffix), l=1), s=1, f=1):
                    if re.search(regex_search_shapes, item):
                        cmds.select(item, add=1)
                        sel_added = True
            if parent and sel_added:
                print('Selected nodes under "{}" with suffix: {}Shape'.format(parent, suffix))
            elif sel_added:
                print('Selected nodes with suffix: {}Shape\tAll in scene'.format(suffix))
            sel_added = False
            if transforms:
                regex_search_geo = '{}[_:|A-Za-z].*({})'.format(parent, geo_type_transforms)
                for item in (cmds.ls('{}*:*{}'.format('', suffix), l=1) + cmds.ls('{}*{}'.format('', suffix), l=1)):
                    if re.search(regex_search_geo, item):
                        cmds.select(item, add=1)
                        sel_added = True
            if parent and sel_added:
                print('Selected nodes under "{}" with suffix: {}'.format(parent, suffix))
            elif sel_added:
                print('Selected nodes with suffix: {}     \tAll in scene'.format(suffix))

    print('\nJib Jab - selGEO COMPLETE')


def deadlineSubmit():
    """ wrapper for SubmitJobToDeadline found on Deadline shelf.
    This is a wrapper function to call Deadline submit with extra settings for render globals and Deadline

    Attributes:

    Returns:

    Todo:

    """

    import maya.OpenMaya as OpenMaya
    import os
    import maya.mel as mel
    # Set VRay settings w/o using render settings json file
    try:
        mel.eval('fixRenderLayerOutAdjustmentErrors')  # request for layer errors
        cmds.setAttr('vraySettings.fnprx', lock=0)
        cmds.setAttr('vraySettings.fnprx', '<Layer>/<Version>/<Scene>.<Layer>', type='string')  # vray File Name Prefix
        cmds.setAttr('vraySettings.fnprx', lock=1)
        current_file = cmds.file(q=1, sn=1)
        if os.path.basename(current_file).split('.')[-2]:
            version = os.path.basename(current_file).split('.')[-2]
        else:
            version = '000'
        if 'v' not in version:
            version = 'v{}'.format(version)
        cmds.setAttr('defaultRenderGlobals.renderVersion', lock=0)
        cmds.setAttr('defaultRenderGlobals.renderVersion', '{}'.format(version), type='string')
        cmds.setAttr('defaultRenderGlobals.renderVersion', lock=1)
        cmds.setAttr('vraySettings.imageFormatStr', 'exr (multichannel)', type='string')  # vray Image Format
        cmds.setAttr('vraySettings.animType', 1)  # vray Animation Standard
        cmds.setAttr('vraySettings.animBatchOnly', 1)  # vray Render animation only in batch mode
        cmds.setAttr('vraySettings.aspl', 1)  # vray Resolution Maintain Weidth/Height Ratio
        cmds.setAttr('defaultResolution.ldar', 1)  # Maintain Ratio
        cmds.setAttr('vraySettings.wi', 1920)  # vray Resolution Width
        cmds.setAttr('vraySettings.he', 1080)  # vray Resolution Height
        cmds.setAttr('vraySettings.aspr', 1.778)  # vray Resolution Device Aspect Ratio
        cmds.setAttr('vraySettings.pxa', 1.0)  # vray Resolution Pixel Aspect Ratio
        try:
            step = current_file.split('02_maya')[1].split('/')[1]
            cmds.setAttr('defaultRenderGlobals.deadlineDepartment', step, type='string')
        except Exception, e:
            print ('Could not load department into Deadline. Please set. Exception: {}'.format(e))
        mel.eval('SubmitJobToDeadline')
        mel.eval('SetJobName')
    except Exception, e:
        OpenMaya.MGlobal.displayError('Could not load: {}'.format(e))


__author__ = "Robert Showalter"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/6/2017"
__credits__ = ["Robert Showalter, Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
