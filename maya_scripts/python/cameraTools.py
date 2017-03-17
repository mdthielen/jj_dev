#!/usr/bin/python
"""
Camera Tools
Create standard shot camera.
Connect to renderer as renderable.

Attributes:
    
    
Todo:
    
    
"""
# REVIEW[mark] Test at studio
import maya.cmds as cmds


def createShotCam(camera_name='shotCam'):
    """
    createShotCam creates camera, sets Far Clip Plane, Film Aspect Ratio, and Renderable
    
    :type camera_name: name of shot camera. Defaults to shotCam
    
    """

    print('\nJib Jab createShotCam:')

    # defaults - maybe promote as params to pass into createShotCam

    aspect_ratio = 1.77
    far_clip = 1000000
    overscan = 1.1
    film_fit = 3  # overscan
    focal_length = 35.0
    near_clip = 0.01

    cam_exists_dialog = ''
    new_shot_cam = False
    modify_cam_attr_safe = True
    current_selection = None

    if len(cmds.ls(sl=1)) == 1:
        current_selection = cmds.ls(sl=1)[0]
        current_selection_type = cmds.nodeType(cmds.listRelatives(current_selection))
        if current_selection_type == 'camera' and current_selection not in ['top', 'side', 'front']:
            camera_selected = True
        else:
            camera_selected = False
    else:
        camera_selected = False

    if existsShotCam(camera_name):
        cam_exists_dialog = cmds.confirmDialog(title='"{}" exists'.format(camera_name),
                                               message='Overwrite the following attributes that could effect rendering?\n'
                                                       'aspect ratio:\t{}\n'
                                                       'clip planes:\t{} to {}'.format(aspect_ratio, near_clip, far_clip),
                                               button=['Yes', 'No', 'Cancel'],
                                               defaultButton='No', cancelButton='Cancel', dismissString='No')

        modify_cam_attr_safe = True
    elif camera_selected:
        if 'persp' == current_selection:
            sel_or_dup = 'a duplicated'
        else:
            sel_or_dup = 'selected'
        use_selected_cam_dialog = cmds.confirmDialog(title='No "{}" exists!'.format(camera_name),
                                                     message='Use {} "{}" camera as "{}"?'.format(sel_or_dup, current_selection, camera_name),
                                                     button=['Yes', 'No', 'Cancel'],
                                                     defaultButton='No', cancelButton='Cancel', dismissString='No')
        if use_selected_cam_dialog == 'Yes':
            cam_exists_dialog = cmds.confirmDialog(title='{}'.format(camera_selected),
                                                   message='Overwrite the following attributes that could effect rendering?\n'
                                                           'aspect ratio:\t{}\n'
                                                           'clip planes:\t{} to {}'.format(aspect_ratio, near_clip, far_clip),
                                                   button=['Yes', 'No', 'Cancel'],
                                                   defaultButton='No', cancelButton='Cancel', dismissString='No')
            modify_cam_attr_safe = True
            if current_selection == 'persp':
                cmds.duplicate(current_selection, name=camera_name)
                print('Duplicated persp to {}'.format(camera_name))
            else:
                cmds.rename(current_selection, camera_name)
                print('Renamed {} to {}'.format(current_selection, camera_name))
        elif use_selected_cam_dialog == 'No':
            cmds.warning('Select 1 camera to use as "{}" and run again.'.format(camera_name))
            modify_cam_attr_safe = False

    else:
        use_existing_cam_dialog = cmds.confirmDialog(title='No "{}" exists!'.format(camera_name),
                                                     message='Use existing camera from scene as {}?'.format(camera_name),
                                                     button=['Yes', 'No', 'Cancel'],
                                                     defaultButton='No', cancelButton='Cancel', dismissString='No')
        if use_existing_cam_dialog == 'Yes':
            cmds.warning('Select 1 camera to use as "{}" and run again.'.format(camera_name))
            modify_cam_attr_safe = False
        else:
            # Create new camera
            cam_generic = cmds.camera(focalLength=focal_length)
            cmds.rename(cam_generic[0], camera_name)
            new_shot_cam = True
            modify_cam_attr_safe = True
            print('Created   "{}"'.format(camera_name))

    if new_shot_cam or cam_exists_dialog == 'Yes':
        cmds.setAttr('{}Shape.horizontalFilmAperture'.format(camera_name), cmds.getAttr('{}Shape.verticalFilmAperture'.format(camera_name)) * aspect_ratio)
        cmds.setAttr('{}Shape.farClipPlane'.format(camera_name), far_clip)
        cmds.setAttr('{}Shape.nearClipPlane'.format(camera_name), near_clip)
        print('Modified focal length to {}'.format(focal_length))
        print('Modified aspect ratio to {}'.format(aspect_ratio))
        print('Modified near clip to    {}'.format(near_clip))
        print('Modified far clip to     {}'.format(far_clip))

    if modify_cam_attr_safe:
        # change these to any shotCam
        cmds.setAttr('{}Shape.displayGateMask'.format(camera_name), True)
        cmds.setAttr('{}Shape.displayGateMaskOpacity'.format(camera_name), 0.95)
        cmds.setAttr('{}Shape.displayGateMaskColor'.format(camera_name), 0, 0, 0)
        cmds.setAttr('{}Shape.displayResolution'.format(camera_name), True)
        cmds.setAttr('{}Shape.filmFit'.format(camera_name), film_fit)
        cmds.setAttr('{}Shape.overscan'.format(camera_name), overscan)
        cmds.setAttr('{}Shape.renderable'.format(camera_name), 1)
        cmds.setAttr('{}.visibility'.format(camera_name), 1)
        cmds.setAttr('perspShape.renderable', 0)

        print('Set "{}" attributes renderable and display gates setup'.format(camera_name))
        print('Set "persp" attribute renderable off')

    print('\nJib Jab createShotCam COMPLETE')


def existsShotCam(camera):
    """
    Check if shotCam exists
    
    :rtype: bool Does camera exist
    :param camera: name of shot camera transform node
    """

    shot_cam_exists = cmds.objExists(camera)

    return shot_cam_exists


__author__ = "Mark Thielen"
__copyright__ = "Copyright 2017, Jib Jab Studios"
__date__ = "3/15/17"
__credits__ = ["Mark Thielen"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Mark Thielen"
__email__ = "mdthielen@gmail.com"
__status__ = "Production"
