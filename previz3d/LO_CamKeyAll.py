import pymel.core as pm
import maya.cmds as cmds

def LO_CamKeyAll() :
	oRoot = pm.PyNode('|e0*')
	oCamRoot = pm.PyNode( oRoot.name()+'|CM_ROOT' )
	oCamShape = pm.listRelatives(oCamRoot, allDescendents = True, type = 'camera')[0]

	oCam = oCamShape.getParent()
	oDolly = oCam.getParent().getParent()
	oLocal_SRT = oDolly.getParent().getParent()
	oGlobal_SRT = oLocal_SRT.getParent().getParent()

	cmds.setKeyframe( oGlobal_SRT.longName(), oLocal_SRT.longName(), oDolly.longName(), oCam.longName(), attribute=['translateX', 'translateY','translateZ', 'rotateX', 'rotateY', 'rotateZ'] )
	cmds.setKeyframe( oCam.longName(), attribute=['focalLength'] )

	'''cmds.setKeyframe( oCamShape.longName(), attribute=['fl'])'''