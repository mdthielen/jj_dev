from pymel.core import *

#   This is a stripped down version of my unfinished materialSync 
#   script which expanded towards UI, namespace considerations, 
#   and multiple imported shader files. That script, however, 
#   lacked the versitity to work outside of a specific workflow.

DEBUG = True

''''''''''''
'''EXPORT'''
''''''''''''

def materialSyncExport(shadingExportGRP= 'GRP_MTL'):

    '''
    GET SHADERS
    '''            
    #grab all shaders   
    shadingEngines = ls(type='shadingEngine')
    
    #remove lambert1
    shadingEngines.remove('initialParticleSE')
    
    #Make sure there are shaders
    if not shadingEngines:
    
        cmds.confirmDialog(message='No applied shading groups found') 
        
        return
        
        
    #prune unused shaders from the list
    for se in shadingEngines:
    
        if not sets(se, query=True): 
        
            shadingEngines.remove(se)
            
            
    '''
    CREATE SHADER GROUP
    ''' 
    #check if shadingExportGRP exists
    if objExists(shadingExportGRP): 
    
        error('!!! \"{0}\" node already exists.  Please delete or rename it !!!'.format(shadingExportGRP))
    
    
    #create the group for shader export
    group( em=1 , n=shadingExportGRP )
    
    #hide it
    setAttr( shadingExportGRP + '.visibility', 0)
    
    
    '''CREATE EACH SHADER SPHERE'''
    for se in shadingEngines:
        
        #check which objects have the shader applied
        onObj = sets(se, q=1)
                       
        if DEBUG: 
            
            #method reference: print('\n'.join('{}: {}'.format(*k) for k in enumerate(lst)))
            print('\n' + se + ':\n\t' + '\n\t'.join('{}'.format(obj) for obj in onObj) + '\n') 
               
               
        #turn list into a comma separated string
        objStr = ', '.join( [str(x) for x in onObj] )
        
        #make sure there's a notes attribute for the shading group
        if not attributeQuery( 'notes', node = se, exists = True ): 
        
            addAttr( se, longName = 'notes', dataType = 'string' )  
        
        
        #add string to shading group notes
        setAttr( (se + ".notes"), objStr, type='string' )   
                 
        #create a name according to the shading group
        mtlSphereName = str(se) + '_GEO'
        
        #create the sphere
        polySphere( n=mtlSphereName, ch=0, sx=5, sy=4 )
            
        #apply the shading group to the new sphere
        sets( str(se), e=1, forceElement=1 )
        
        #place in the shadingExportGRP 
        parent( selected(), shadingExportGRP )
    
    
    '''
    EXPORT THE SHADER GROUP
    '''
    select( shadingExportGRP )
    
    filePlacement = cmds.fileDialog2( okc='Export', ff='*.ma' )
    
    if filePlacement: 
    
        cmds.file(filePlacement,
            force = True,
            shader = True, 
            exportSelected = True, 
            type = 'mayaAscii' )
            
    else:
    
        delete( shadingExportGRP ) 
        
        error( 'operation cancled' )

        
    '''
    REMOVE THE NEW GROUP
    '''
    delete( shadingExportGRP )
    cmds.confirmDialog(
        title = 'Success!', 
        button = 'OK', 
        message='Shader file exported to: {0}'.format(str(filePlacement[0]))
    )
    
      
         
         

''''''''''''
'''IMPORT'''
''''''''''''
def materialSyncApply( shadingExportGRP = 'GRP_MTL' ):
    '''
    FIND THE SHADER GROUP AND MATCHING OBJECTS
    '''
    #check that shadingExportGRP exists
    if not objExists( shadingExportGRP ):
    
        cmds.confirmDialog( message = 'Could not find \'{}\'. Please import a shader group.'.format( shadingExportGRP ) ) 
        
        return
    
    if DEBUG: print('\n\FOUND: \'{}\''.format(shadingExportGRP) ) 
    
    #make sure shadingExportGRP has children
    
    MTLSpheres = listRelatives( shadingExportGRP )
        
    if not MTLSpheres:
    
        cmds.confirmDialog( message = 'No children found under {}. \n Make sure it exported properly'.format( shadingExportGRP ) )
        
        return
    
    
    #collect all shaders
    shadingEngines = []
    
    for obj in MTLSpheres: 
    
        shadingEngines.append( listSets(extendToShape = True, object = str( obj ))[0] )#Assumes shading group is first listed set

    
    #gather assignments for each imported shader    
    materialSets = {}
    
    for se in shadingEngines:
    
        #check that the notes exist
        if not attributeQuery('notes', n=se, ex=1): 
            
            cmds.confirmDialog( message = 'assignments not found for {0}'.format( se ) ) 
        
            return

            
        #store the shading group and object relation in a dictionary
        materialSets[se] = getAttr( se + '.notes' ).split( ', ' )
    
    
    if DEBUG: 
    
        print('\n\'materialSets\'')   
        
        for mtl in materialSets.keys():
        
            #method reference: print('\n'.join('{}: {}'.format(*k) for k in enumerate(lst)))
            print('\n' + mtl + ':\n\t' + '\n\t'.join('{}'.format(obj) for obj in materialSets[mtl]) + '\n') 
        
        
    #create mtl for unassigned geo
    #noMatch_mtl = shadingNode('surfaceShader', asShader=True, name='no_match_mtl')

    #setAttr( noMatch_mtl + '.outColor', 0.0, 1.0, 0.0, type='float3' )
        
    #
    matched = {}    
    notMatched = {}
    for mtl in materialSets.keys():
    
        for obj in materialSets[mtl]:
            
            if objExists( obj ):
                
                #assign imported shader to matching object
                sets( mtl, e=True, forceElement = obj )
                
                matched[mtl] = obj
            
            else:
                
                #assign new mtl for unassigned geo
                #sets( noMatch_mtl, edit=True, forceElement = obj )
                
                notMatched[mtl] = obj
    
    '''
    PRINT RESULTS
    '''
    print( '\n\nRESULTS:\n' )
    
    if matched:
    
        print( '\n\tMatched:\n' )
        
        for mtl in matched.keys():
            
            print( '\n\t\t' + mtl + '\n\t\t\t'.format( obj ) for obj in matched[mtl] ) 
            
            
    if notMatched:
    
        print( '\n\tMatch Not Found:\n' )
        
        for mtl in notMatched.keys():
            
            print( '\n\t\t' + mtl + '\n\t\t\t'.format( obj ) for obj in notMatched[mtl] )     
    
    warning('script complete. See script editor for details')
