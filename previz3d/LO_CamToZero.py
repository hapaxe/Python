import pymel.core as pm

def LO_CamToZero():
	oRoot = pm.PyNode('|e0*')
	oCamRoot = pm.PyNode( oRoot.name()+'|CM_ROOT' )
	oCamShape = pm.listRelatives(oCamRoot, allDescendents = True, type = 'camera')[0]
	oCam = oCamShape.getParent()
	print oCam

	vCamT = oCam.getTranslation(space='world')
	vCamR = oCam.getRotation(space='world')
	vCamS = oCam.getScale()

	oDolly = oCam.getParent().getParent()
	oLocal_SRT = oDolly.getParent().getParent()
	oGlobal_SRT = oLocal_SRT.getParent().getParent()

	print oDolly

	oGlobal_SRT.setTranslation([0,0,0], space='world')
	oGlobal_SRT.setRotation([0,0,0], space='world')
	oLocal_SRT.setTranslation([0,0,0], space='world')
	oLocal_SRT.setRotation([0,0,0], space='world')
	oDolly.setRotation([0,0,0], space='world')
	oDolly.setTranslation([0,0,0], space='world')

	'''oDolly.setTranslation(vCamT, space='world')
	oDolly.setScale(vCamS)'''

	oCam.setTranslation(vCamT, space='world')
	oCam.setRotation(vCamR, space='world')
	oCam.setScale([1,1,1])