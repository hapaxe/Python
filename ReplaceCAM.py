#Replace CAM MIROIR
import maya.cmds as cmds

maSelection = cmds.ls(sl=True, fl=True)

#create group and place it
cmds.group(em = True, name='GRP_CAM' )
cmds.setAttr("GRP_CAM.tx", -296.2943)
cmds.setAttr("GRP_CAM.ty", 0)
cmds.setAttr("GRP_CAM.tz", 592.7813)
cmds.setAttr("GRP_CAM.sx", -1)
cmds.setAttr("GRP_CAM.sz", -1)

# group under GRP_CAM and place it
cmds.parent(maSelection, 'GRP_CAM')
cmds.setAttr("GRP_CAM.tx", -5.7813)
cmds.setAttr("GRP_CAM.ty", 0)
cmds.setAttr("GRP_CAM.tz", 4.0096)
cmds.setAttr("GRP_CAM.sx", 1)
cmds.setAttr("GRP_CAM.sz", 1)

controlerBase = cmds.ls('*CTRL_BASE')
# def attributes
sx = controlerBase[0] + '.sx'
sz = controlerBase[0] + '.sz'
tx = controlerBase[0] + '.tx'
tz = controlerBase[0] + '.tz'
# get attributes
txValue = cmds.getAttr(tx)
tzValue = cmds.getAttr(tz)
# calcul new values
newTxValue = txValue - (-290.513)
newTzValue = tzValue - (588.7717)
# set attributes
cmds.setAttr(tx, newTxValue)
cmds.setAttr(tz, newTzValue)
cmds.setAttr(sx, -1)
cmds.setAttr(sz, -1)