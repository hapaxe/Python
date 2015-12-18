__author__ = 'g.console'

'''
SHADER PARAMETER LIST
animM_int : number of Frame textur anim
animOf_int : Start frame texture anim

animU_float : animation UV.U
animV_float : animation UV.V

colorR_float : color rgb.r    (0,1) Maya  (0,255)Max
colorG_float : color rgb.g   (0,1) Maya  (0,255)Max
colorB_float : color rgb.b   (0,1) Maya   (0,255)Max

blend_float : blending color  (0,1)

vis_float : Maya’s shader opacity or Max’s shader opacity   (0,100)

switchT_bol : switch boolean  (0/1)
preset_int : preset selector sous forme de liste  [0,1,2,3,...]
'''


import maya.cmds as mc


def goldParam(type='gold'):

    #init
    stateShader= type+'mat'
    stateShaderSG= stateShader+'SG'

    objMesh= mc.ls(selection=True)

    #Add Attr State
    if not mc.objExists('walk_ctrl.'+type+'_switch'):
        mc.addAttr('*walk_ctrl', shortName=type+'_switch',attributeType='long', defaultValue=0, minValue=0, maxValue=1,keyable=True )

    #Creation State Shading
    if mc.objExists(stateShader):
        mc.delete(stateShader)
    if mc.objExists(stateShaderSG):
        mc.delete(stateShaderSG)

    if type =='gold':
        stateShader=mc.shadingNode('phong', asShader=True, name=stateShader)
        stateShaderSG=mc.sets(renderable=True, empty=1, noSurfaceShader=True, name=stateShaderSG)
        mc.defaultNavigation(source=stateShader, destination=stateShaderSG, connectToExisting=1)
        mc.setAttr( stateShader +'.color', 1, 0.92, 0, type= 'double3' )

    if type =='stone':
        stateShader=mc.shadingNode('lambert', asShader=True, name=stateShader)
        stateShaderSG=mc.sets(renderable=True, empty=1, noSurfaceShader=True, name=stateShaderSG)
        mc.defaultNavigation(source=stateShader, destination=stateShaderSG, connectToExisting=1)
        mc.setAttr( stateShader +'.color', 0.5, 0.5, 0.5, type= 'double3' )



    for obj in objMesh:
        stateBlend= type+'_BlendColor'
        #Get Shape
        objShape=mc.listRelatives(obj, shapes=True, noIntermediate=True)[0]

        #Get Shader Group
        curShGConnect=mc.connectionInfo(objShape+'.instObjGroups', destinationFromSource=True)
        curShGConnectTMP=curShGConnect[0].split('.')
        currentShaderSG=curShGConnectTMP[0]
        print 'ShadingGroup '+currentShaderSG

        #Debug Shader
        if currentShaderSG== 'initialShadingGroup' or currentShaderSG== type+'_MatSwitchSG' :
            #Generic Shader Case
            if not mc.objExists(type+'_MatSwitch'):
                #Create New StateShader
                newShader=mc.shadingNode('lambert', asShader=True, name=type+'_MatSwitch')
                newShaderSG=mc.sets(renderable=True, empty=1, noSurfaceShader=True, name=newShader+'SG')
                mc.defaultNavigation(source=newShader, destination=newShaderSG, connectToExisting=1)

                currentShader= newShader
                currentShaderSG=newShaderSG
                if not mc.objExists(stateBlend):
                    stateBlend=mc.shadingNode('blendColors', asUtility=True, name=stateBlend)

            else:
                #Reuse StateShader
                currentShaderSG=type+'_MatSwitchSG'
                if not mc.objExists(stateBlend):
                    stateBlend=mc.shadingNode('blendColors', asUtility=True, name=stateBlend)

        else:
            #Use Old Shader with Own Branch
            stateBlend=mc.shadingNode('blendColors', asUtility=True, name=obj+'_'+stateBlend)

        #Get Shader
        curShConnect=mc.connectionInfo(currentShaderSG+'.surfaceShader', sourceFromDestination=True)
        curShConnectTMP=curShConnect.split('.')
        currentShader=curShConnectTMP[0]
        print currentShader


        #Set Blend Color
        if mc.connectionInfo(currentShader+'.color', isDestination=True):
            colorConnect=mc.connectionInfo(currentShader+'.color', sourceFromDestination=True)
            print colorConnect
            if not colorConnect==stateBlend+'.output':
                mc.connectAttr(colorConnect, stateBlend+'.color2',f=True)

        else:
            colorValue=mc.getAttr(currentShader+'.color')
            print colorValue
            mc.setAttr(stateBlend+'.color2', colorValue[0][0], colorValue[0][1], colorValue[0][2] )

        #Connect Blend Color to current Shader
        testConnect=mc.connectionInfo(currentShader+'.color', sourceFromDestination=True)
        print 'testConection '+ testConnect
        if not testConnect==stateBlend+'.output':
            mc.connectAttr(stateShader+'.outColor', stateBlend+'.color1',f=True)
            mc.connectAttr(stateBlend+'.output', currentShader+'.color',f=True)
            mc.connectAttr( 'walk_ctrl.'+type+'_switch', stateBlend+'.blender',f=True)

        #Assign Shader
        mc.sets(obj,e=True,fe=currentShaderSG)

        #Connect ShaderParam to Setup
        if not mc.objExists(objShape+'.SP_'+type+'_int'):
            mc.addAttr(objShape, shortName='SP_'+type+'_int', attributeType='long', keyable=True)
            mc.connectAttr('walk_ctrl.'+type+'_switch', objShape+'.SP_'+type+'_int',f=True)
        '''
        connectAttr -force goldmat.outColor blendColors1.color2;
        connectAttr -force blendColors1.output gold_MatSwitch.color;
        getAttr gold_MatSwitch.color
        setAttr "blendColors1.color1" -type double3 0 1 0.460667 ;
        '''
goldParam(type='gold')