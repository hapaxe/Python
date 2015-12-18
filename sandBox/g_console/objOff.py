__author__ = 'g.console'

import maya.cmds as mc

name='Puff001'
frame='00027'
layer='Puff'

objName=name+'_'+frame+'_'+layer+'_OFF'
mc.polyCreateFacet( p=[(0,0,0),(0,0,0),(0,0,0)],n=objName)

'''
objTrans=mc.createNode( 'transform', n=objName )
mc.createNode( 'mesh', n=objName+'Shape',p=objTrans )
mc.setAttr( objName+'.vtx[0:1]', 0, 0, 0, 1, 1, 1,type="double3" )
'''
