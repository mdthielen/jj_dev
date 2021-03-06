'''LIGHTING TOOLS'''

import maya.cmds as mc

'''ADD VRAY OPENSUBDIV TO SELECTED GEO'''
def addVrayOSD(userDepth = 2):
    shapes = mc.ls(sl=1, dag=1, lf=1, s=1)
    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_opensubdiv", 1)
        mc.setAttr( shape+'.vrayOsdSubdivDepth', userDepth)

def addVrayOID():
    shapes = mc.ls(sl=1, dag=1, lf=1, s=1)
    for shape in shapes:
        mc.vray("addAttributesFromGroup", shape, "vray_objectID", 1)
#    mc.setAttr( trans+'.vrayObjectID', userID)


maLightTypes = ['VRayLightDomeShape',
            'VRayLightIESShape',
            'VRayLightMesh',
            'VRayLightMtl',
            'VRayLightRectShape',
            'VRayLightSphereShape',
            'ambientLight',
            'areaLight',
            'directionalLight',
            'pointLight',
            'spotLight',
            'volumeLight',
            'VRaySunShape']

            
def checkSelectedLights( sel = mc.ls( sl = 1) ):
    #use to check if the selection matches the light types defined in maLightTypes
    #a bad egg is returned if it is not one of the predefined light types
    
    ltShapes = []
    badEgg = None

    for obj in sel: 

        shape = mc.listRelatives( obj, s = 1 )
        
        if mc.objectType( shape ) in maLightTypes:
            
            ltShapes.append( shape )
            
        else: 
        
            badEgg = True
            
            break
    
    return ltShapes, badEgg


def listAllLights( ltShapes ):
    #gather all lights as defined by the maLightTypes
     
    for t in maLightTypes:
    
        [ltShapes.append(x) for x in mc.ls(type = t)]
    
    return ltShapes



def mkLightElem( ltShapes ):

    import maya.mel
    
    for lt in ltShapes:
        
        ltTran = mc.listRelatives( lt, p = 1 )[0]
        elem = 'vrayRE_' + ltTran    
        maya.mel.eval('vrayAddRenderElement( "LightSelectElement" );')
        mc.rename( 'vrayRE_Light_Select', elem )
        mc.setAttr( elem + '.vray_name_lightselect', 'lt_' + ltTran, type = 'string' )
        mc.sets(ltTran, addElement=elem)


def autoCreateLightElem():

    ltShapes, badEgg = checkSelectedLights()
    
    if badEgg:
        
        mc.warning( 'Selection contains unrecognised light types' )
        
    elif ltShapes:
        
        mkLightElem( ltShapes )
        
    elif not ltShapes:
        
        result = mc.promptDialog(
            title='Create VRay Light Element(s)',
            message='No light selected, create elements for all lights in the scene?',
            button=['OK', 'Cancel'],
            defaultButton='Cancel', cancelButton='Cancel', dismissString='Cancel')

        if result == 'OK':
            ltShapes = listAllLights( ltShapes )
            mkLightElem( ltShapes )


def characterEyes():

    visMesh = mc.ls(et = "mesh", v = 1) 
    characters = [ "bang", "boop", "bing", "bo", "beep" ]
    leftEyePattern = "_lpupil|_l_.*pupil"
    rightEyePattern = "_rpupil|_r_.*pupil"
    charEyes = []

    for mesh in visMesh:

        for char in characters:

            if re.search( char + "_.*pupil", mesh, re.I ) and not re.search( "orig$|rig1$", mesh, re.I ):

                if re.search( leftEyePattern, mesh, re.I ):       # LEFT EYES
                    
                    charEyes.append( [mesh, char + "_R_eyeSpec"]) # pair rig-left with screen-right

                if re.search( rightEyePattern, mesh, re.I ):      # RIGHT EYES

                    charEyes.append( [mesh, char + "_L_eyeSpec"]) # pair rig-right with screen-left
    
    return charEyes



def createEyeSpecLight( mesh, lightName ): #multiple meshes can be used with the syntax: ( "obj1", "obj2", "obj3" )
    #create vray dome with a disc and link it only to the mesh objects.
    
    lightShape = lightName + "Shape"
    
    
    #create a vray dome
    newDome = mc.shadingNode( "VRayLightDomeShape", asLight = True, name = lightShape )
    
    #set the dome attributes
    mc.setAttr( lightShape + ".intensityMult", 10 )
    mc.setAttr( lightShape + ".shadows", 0 )
    mc.setAttr( lightShape + ".useDomeTex", 1 )
    ###
    mc.setAttr( lightShape + ".invisible", 1 )
    mc.setAttr( lightShape + ".affectDiffuse", 0 )
    mc.setAttr( lightShape + ".affectSpecular", 1 )
    mc.setAttr( lightShape + ".affectReflections", 0 )
    mc.setAttr( lightShape + ".affectAlpha", 0 )
    
    
    #create ramp texture
    newRamp = mc.shadingNode( "ramp", asTexture = True, name = lightName + "_Ramp" )
    
    #first ramp point
    mc.setAttr( newRamp + ".colorEntryList[0].position", 0.93 )
    mc.setAttr( newRamp + ".colorEntryList[0].color", 0, 0, 0, type = "double3" )
    #second ramp point
    mc.setAttr( newRamp + ".colorEntryList[1].position", 0.945 )
    mc.setAttr( newRamp + ".colorEntryList[1].color", 1, 1, 1, type = "double3" )
    

    #Break light links with everything but the mesh(s)
    mc.lightlink( b = True, light = newDome, object = mc.ls() )
    mc.lightlink( make = True, light = newDome, object = mesh )
        
    return newDome, newRamp



def buildEyeLights():
    charEyes = characterEyes()
    for eye in charEyes:
        createLightAndLink( eye[0], eye[1] )

'''
def eyeSpecCleanup():
    setAttr "VRayPlaceEnvTex2.useTransform" 1;
'''

def lightingCleanup():
    charAll = ['Bing_Riglocator', 'Beep_Riglocator', 'Bo_Riglocator', 'Boop_Riglocator', 'Bang_Riglocator']
    for char in charAll: 
        mc.editRenderLayerMembers( 'shd', char, noRecurse = 1 )
    mc.editRenderLayerMembers( 'shd', 'SHD_GEO_GRP', noRecurse = 1 )
    mc.select( 'SHD_GEO_GRP', r = 1 )
    newShdGrp = mc.duplicate( rr = 1 )[0]
    children = mc.listRelatives( newShdGrp, c = 1 )
    for c in children:
        shd = mc.rename( newShdGrp + '|' + c, c + '_shd' )
        noVis = mc.duplicate( shd, n= c+'_noVis', rr=1)[0]
        mc.setAttr( noVis + '.primaryVisibility', 0 )
        mc.sets( shd , addElement = 'groundPlane_shd_vrayobjectproperties')
        if not mc.objExists('groundPlane_noVis_set'): mc.sets( noVis , n = 'groundPlane_noVis_set')
        else: mc.sets( noVis , add = 'groundPlane_noVis_set')
        mc.hide( shd )
    mc.hide( 'SHD_GEO_GRP' )    








