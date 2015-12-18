#-----
# Create a SoftMod Rig like Sticky to add directly in rig
#-----

def ch4_CheckCreate_Group( sGroupName ):
    '''
    Check if a group exist and Create it if not exist
    ---
    sGroupName : string | Define the name of Group to check existance
    '''
    # Test if RIG_TRASH exist
    bRT_Exist = mc.objExists(sGroupName)
    
    # If not Exist we create it
    if not bRT_Exist:
        mc.group( em=True, name=sGroupName )
    
    return sGroupName

def add_circle_shape( inObj, normal= (1,0,0), center= (0,0,0), size= 1 ):
    '''
    Add a circle shape on in Object

    :param inObj: The name of the Transform
    :type inObj: string
    :param normal: Define the normal align of the shape
    :type normal: list
    :param center: Define the center offset of the shape
    :type center: list
    :param size: Define the size of the shape
    :type size: float
    '''
    lNCircle = mc.circle( normal= normal, center= center, r=size, d=1 )
    sShape   = mc.listRelatives(lNCircle[0], s=True)
    mc.parent( sShape[0], inObj, s=True, r=True )
    mc.rename( sShape[0], '%sShape' %(inObj) )
    mc.delete( lNCircle[0] )

def create_SoftMod(name='SoftMod'):
    ''''''
    #--- get current selection
    cSelection = mc.ls( sl = True ) or list()

    if not cSelection:
        return

    tmp_root = ch4_CheckCreate_Group( 'TMP_ROOT_RIG' )
    
    #--- add an orig
    sOrig = mc.group(em=True, p=tmp_root, n='%s_orig' %name)
    
    #--- add a root manip
    sRoot = mc.group(em=True, p=sOrig, n='%s_deformation_root' %name)
    add_circle_shape( sRoot, normal= (0,0,0), center= (0,0,0), size= 0.4 )
    
    #---  add manip
    tmp = mc.softMod( cSelection[0], n=name )

    deform = tmp[0]
    handle = tmp[1]

    #---  add manip
    manip = mc.group(em=True, p=sRoot, n='%s_manip' %name)
    add_circle_shape( manip, normal= (0,0,0), center= (0,0,0), size= 0.3 )
    
    #---  plug softMod to manip
    mc.softMod(deform, e=True, wn=(manip, manip))
    
    #---  falloffMode
    mc.addAttr(manip, ln='mode', at='enum', en='Volume:Surface')
    mc.setAttr('%s.mode' %manip, k=False, cb=True)
    mc.connectAttr('%s.mode' %manip, '%s.falloffMode' %deform, f=True)
    
    #---  falloffRadius
    mc.addAttr(manip, ln='smRadius', at='float', min=0.0, dv=.5)
    mc.setAttr('%s.smRadius' %manip, e=True, k=True)
    mc.connectAttr('%s.smRadius' %manip, '%s.falloffRadius' %deform, f=True)
    
    #---  offset
    mc.addAttr(manip, ln='offset', at='short', min=0, max=1)
    mc.setAttr('%s.offset' %manip, e=True, k=False, cb=True)
    
    smOffset = mc.spaceLocator(n='%s_offset' %manip)[0]
    mc.parent(smOffset, sRoot, r=True)
    mc.connectAttr('%s.offset' %manip, '%s.v' %smOffset)
    mc.setAttr('%sShape.localScale' %smOffset, .2, .2, .2)
    
    #---  connect softMod falloff center
    mc.connectAttr('%s.worldPosition' %smOffset, '%s.falloffCenter' %deform, f=True)
    
    #---  connect bpm
    mc.connectAttr('%s.parentInverseMatrix' %manip, '%s.bindPreMatrix' %deform, f=True)
    
    #---  set values
    smShape  = mc.listConnections(deform, s=True, d=False, p=True, type='softModHandle')[0].rpartition('.')[0]
    mc.setAttr('%s.v' %smShape, 0)
    
    #--- clean setup
    mc.delete(handle)

create_SoftMod( name= 'SoftMod')