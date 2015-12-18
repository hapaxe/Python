import maya.cmds as mc

sel= mc.ls( sl= True )

for i in range( 0, len(sel), 3):
    # --- Get item
    bone_FK= sel[i]
    bone_IK= sel[i+1]
    bone_Skin= sel[i+2]
    
    # --- Create pairBlend
    pairBlend_Node= mc.createNode( 'pairBlend', name= 'pairBleand_'+ bone_Skin.replace('_jnt', '') )
    # - Change rotIntrepolation to Quaternions
    mc.setAttr( pairBlend_Node +'.rotInterpolation', 1)
    
    # --- Do connection
    mc.connectAttr( bone_FK +'.rotateX', pairBlend_Node +'.inRotateX1', f= True)
    mc.connectAttr( bone_FK +'.rotateY', pairBlend_Node +'.inRotateY1', f= True)
    mc.connectAttr( bone_FK +'.rotateZ', pairBlend_Node +'.inRotateZ1', f= True)
    
    mc.connectAttr( bone_FK +'.scaleX', pairBlend_Node +'.inTranslateX1', f= True)

    mc.connectAttr( bone_IK +'.rotateX', pairBlend_Node +'.inRotateX2', f= True)
    mc.connectAttr( bone_IK +'.rotateY', pairBlend_Node +'.inRotateY2', f= True)
    mc.connectAttr( bone_IK +'.rotateZ', pairBlend_Node +'.inRotateZ2', f= True)
    
    mc.connectAttr( bone_IK +'.scaleX', pairBlend_Node +'.inTranslateX2', f= True)
    
    mc.connectAttr( pairBlend_Node +'.outRotateX', bone_Skin +'.rotateX', f= True)
    mc.connectAttr( pairBlend_Node +'.outRotateY', bone_Skin +'.rotateY', f= True)
    mc.connectAttr( pairBlend_Node +'.outRotateZ', bone_Skin +'.rotateZ', f= True)
    
    mc.connectAttr( pairBlend_Node +'.outTranslateX', bone_Skin +'.scaleX', f= True)
