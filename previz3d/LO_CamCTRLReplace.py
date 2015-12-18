import pymel.core as pm

def LO_CamCTRLReplace():
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

	oGlobal_SRT.setTranslation([vCamT[0],0,vCamT[2]], space='world')
	oGlobal_SRT.setRotation([0,vCamR[1],0], space='world')
	oLocal_SRT.setTranslation(vCamT, space='world')
	oLocal_SRT.setRotation([0,vCamR[1],0], space='world')
	oDolly.setRotation(vCamR, space='world')
	oDolly.setTranslation([0,0,0], space='object')

	'''oDolly.setTranslation(vCamT, space='world')
	oDolly.setScale(vCamS)'''

	oCam.setTranslation([0,0,0], space='object')
	oCam.setRotation([0,0,0], space='object')
	oCam.setScale([1,1,1])