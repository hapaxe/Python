import maya.cmds as mc

sel= mc.ls( sl= True )

source= sel[0]
targets= sel[1:]

source_shape= mc.listRelatives( source, s= True )[0]

for item in targets:
    target_shape= mc.listRelatives( item, s= True )[0]
    mc.connectAttr( source_shape +'.outMesh', target_shape +'.inMesh', f= True )__author__ = 'f.rault'
