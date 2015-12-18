__author__ = 'g.console'

'''
Obj Sequencer
Give the name of final Object
All the name's mesh sequence is type like: [objName]_M_[Frame]
'''

import maya.cmds as mc


name='Puff001'
##"constant","linear","cycle","cycleRelative","oscillate"
animType='constant'


#Search layer
allObj=mc.listRelatives(name,allDescendents=True,shapes=False,type='transform')
print allObj
tmplayer=[]
for i in allObj:
    element=i.split('_')
    tmplayer.append(element[2])

#make layer list with unique name
layer=[]
for i in tmplayer:
    if not i in layer:
        layer.append(i)

print layer

for l in layer:

    #init
    objName = name+l
    expoNode=objName+'_Expo'
    choiceNode=objName+'_Choise'

    #Create the sequence for the current layer
    seq=mc.ls(name+'*'+l,type='transform')
    seqOff=mc.ls(name+'*'+l+'_OFF',type='transform')
    seq=seq+seqOff
    seq.sort()
    print seq

    #Node Creation
    if mc.objExists(choiceNode)==1:
        mc.delete(choiceNode)
    choiceNode=mc.shadingNode ('choice',asUtility=True,n=choiceNode)

    if mc.objExists(expoNode)==1:
        mc.delete(expoNode)
    expoNode=mc.createNode('animCurveUU', n=expoNode)

    #Target Shape
    if mc.objExists(objName)==1:
        mc.delete(objName)
    objTrans=mc.createNode( 'transform', n=objName )
    objShape=mc.createNode( 'mesh', n=objName+'Shape',p=objTrans )
    mc.sets (objShape,e=True,include='lambert3SG')


    #Connection and Set Expositions
    i=0
    for item in seq:
        mc.connectAttr (item+'.outMesh', choiceNode+'.input['+str(i)+']', f=True)
        frameC=item.split('_')
        mc.setKeyframe (expoNode,f=int(frameC[1]),v=i,ott='step')
        i +=1
    mc.selectKey(expoNode)
    mc.setInfinity(poi=animType)

    mc.connectAttr(expoNode+'.output',choiceNode+'.selector',f=True)
    mc.connectAttr('time1.outTime',expoNode+'.input',f=True)
    mc.connectAttr(choiceNode+'.output',objShape+'.inMesh',f=True)

