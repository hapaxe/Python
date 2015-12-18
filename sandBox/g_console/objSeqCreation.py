__author__ = 'g.console'

import maya.cmds as mc

def prepCreation(objName,frameL,layer,path):
    #init
    objRef=mc.ls(selection=True)
    layer=['Ref']
    objName='Puff001'
    pathImage=path

    #Grp Global
    globalGrp=mc.createNode('transform',n=objName)
    frameL.sort()
    i=0
    for frameC in frameL:
        #init
        tmpObj=objName+'_'+frameC+'_'+layer[0]
        tmpShader=objName+'_mat_'+frameC+'_'+layer[0]
        tmpShaderSG=objName+'_'+frameC+'_'+layer[0]+'SG'
        tmpFile=objName+'_file_'+frameC+'_'+layer[0]
        tmpUvNode=objName+'_place2dT_'+frameC+'_'+layer[0]
        tmpGrp=objName+'_'+frameC+'_'+layer[0]+'_Grp'
        objList=[tmpObj,tmpShader,tmpShaderSG,tmpFile,tmpUvNode,tmpGrp]

        for item in objList:
            if mc.objExists(item)==1:
                mc.delete(item)

        #Creation Obj
        tmpObj=mc.duplicate(objRef[0],n=tmpObj)

        #Creation Shading
        tmpShader=mc.shadingNode('lambert', asShader=True, name=tmpShader)
        tmpShaderSG=mc.sets(renderable=True,empty=1,noSurfaceShader=True,name=tmpShaderSG)
        mc.defaultNavigation(source=tmpShader,destination=tmpShaderSG,connectToExisting=1)
        mc.sets(tmpObj,e=True,fe=tmpShaderSG)

        tmpFile=mc.shadingNode ('file',asTexture=True,name=tmpFile)
        tmpUvNode=mc.shadingNode ('place2dTexture',asUtility=True,name=tmpUvNode)
        mc.connectAttr(tmpUvNode+'.outUV',tmpFile+'.uv',f=True)
        mc.connectAttr(tmpFile+'.outColor',tmpShader+'.color',f=True)
        mc.connectAttr(tmpFile+'.outTransparency',tmpShader+'.transparency',f=True)

        mc.setAttr(tmpFile+'.fileTextureName',pathImage+frameC+'.png',type="string")

        #Creation GrpByFrame
        tmpGrp=mc.createNode('transform',n=tmpGrp)
        mc.setKeyframe(tmpGrp,at='v',t=int(frameL[i-1]),v=0,ott='step')
        mc.setKeyframe(tmpGrp,at='v',t=int(frameC),v=1,ott='step')
        print i
        print len(frameL)
        if len(frameL)>i+1:
            mc.setKeyframe(tmpGrp,at='v',t=int(frameL[i+1]),v=0,ott='step')

        mc.parent(tmpObj,tmpGrp)

        mc.parent(tmpGrp,globalGrp)

        i+=1





path='Z:/FX/Puff/seqKeyLittlePuff01/littlePuff_'
#Pensez a la Frame 0 OFF si pas de cylcle
frameL=['00000','00001','00002','00003','00006','00008','00010','00013','00016','00019','00021','00023','00025','00027']
layer=['Ref']
objName='Puff001'

prepCreation(objName=objName,frameL=frameL,layer=layer,path=path)
