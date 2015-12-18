#--------------By MARTIN L'ANTON
#
#
#-----------------------------------
#--HOW TO USE IT--------------------
#-----------------------------------
#select all the curves you need to be dynamic, then the curve you want to use as controler for your clusters, and run the scripts, then you just have to specify the number of bones you want.
#-----------------------------------
import maya.cmds as cmds

#define how to offset
def offset(var):
    offset = cmds.group( em = True, name = var + '_offset')
    constraint = cmds.parentConstraint( var, offset )
    cmds.delete( constraint )
    cmds.parent( var, offset)
    return offset

#define how to get the name of the shape
def nameShape(var1):
    cmds.select( var1 )
    selectionShape = cmds.pickWalk( direction = 'down' )
    return selectionShape[0]

# define how to create a stretch network
def stretch(obj1, obj2):
    curveInf = cmds.createNode( 'curveInfo' , n = obj1 + '_curveInfo' ) # Crée un node curveInfo
    cmds.connectAttr( obj2 + '.worldSpace' , curveInf + '.inputCurve' )
    mult = cmds.shadingNode( 'multiplyDivide' , asUtility = True , name = 'MULT_STRETCH_' + obj1 )
    cmds.connectAttr( curveInf + '.arcLength' , mult + '.input1X' )
    curveArcLength = cmds.getAttr( curveInf + '.arcLength' )
    cmds.setAttr( mult + '.input2X' , curveArcLength )
    cmds.setAttr( mult + '.operation' , 2 )
    return mult

# creation de la chaine de bones
def jointChain(pos1, obj1) :
    firstChainJoint = cmds.joint( p= pos1, name = 'SK_' + obj1 + '_0')
    mult = 'MULT_STRETCH_' + obj1
    cmds.connectAttr( mult + '.outputX', firstChainJoint + '.scaleX') # branchement du stretch

    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = cmds.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_' + obj1 + '_' + j )
        cmds.connectAttr( mult + '.outputX', currentJoint + '.scaleX') # branchement du stretch

    return firstChainJoint


selection = cmds.ls(sl = True, fl = True)
numberOfCurves = len(selection)-1

# dialog box
result = cmds.promptDialog(
        title='Numbre of bones',
        message='Type the number of bones that you want on your curve(s)',    
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

if result == 'OK':
            bonesNumber = cmds.promptDialog(query=True, text=True)
    
else :
            Anulation = cmds.confirmDialog(
            title='Confirm', 
            message='You have to type a number of bone(s)', 
            button=['Yes'], 
            defaultButton='Yes')

bonesNumber = int( bonesNumber )
jointsNumber = bonesNumber + 1

for i in range(0, numberOfCurves):

    # recuperation du nom de la shape
    dynCurveName = selection[i]
    dynCurveNameShape = nameShape(dynCurveName)    

    # calcul du nombre de CV
    curveDegree = cmds.getAttr( dynCurveNameShape + '.degree' )
    curveSpan = cmds.getAttr( dynCurveNameShape + '.spans' )

    CVNumber = curveDegree + curveSpan
    
    # creation du stretch
    multCtrl = stretch(dynCurveName, dynCurveNameShape)
    curveInf = dynCurveName + '_curveInfo'
    curveArcLength = cmds.getAttr( dynCurveName + '_curveInfo.arcLength' )
    jointsTX = curveArcLength / bonesNumber
    
    posCvX = cmds.getAttr( curveInf + '.controlPoints[0].xValue' )
    posCvY = cmds.getAttr( curveInf + '.controlPoints[0].yValue' )
    posCvZ = cmds.getAttr( curveInf + '.controlPoints[0].zValue' )
    posPiv = (posCvX, posCvY, posCvZ)
    cmds.xform( dynCurveName, piv = ( posCvX , posCvY , posCvZ ) , ws = True )

    # ctrl curve creation
    ctrlCurveName = cmds.duplicate(dynCurveName)
    ctrlCurveName = cmds.rename(ctrlCurveName, 'CTRL_' + dynCurveName)   
    ctrlCurveNameShape = nameShape(ctrlCurveName)
    print(ctrlCurveName)

    multDyn = stretch(ctrlCurveName, ctrlCurveNameShape)



# creation of dynamic bones and ik
    firstJoint = jointChain(posPiv, dynCurveName)


    # creation de l'ikSpline
    endEffectorNumber = str(bonesNumber)
    ikName = cmds.ikHandle( curve = dynCurveName, ee = 'SK_' + dynCurveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstJoint, name = 'IKSPLINE_' + dynCurveName, ccv = 0 )
    ikName = ikName[0]
    jointRotation = cmds.xform( firstJoint, q=True, ro=True)

    # joints' offset
    offset(firstJoint)

    # ik's offset
    offset(ikName)

    # offset of the curve
    curveOffset = offset(dynCurveName)

    chaineCTRL = 'SK_' + dynCurveName + '_'

# creation of dynamic bones and ik
    # bones chain creation
    firstDynJoint = jointChain(posPiv, ctrlCurveName)

    # creation de l'ikSpline
    ikName = cmds.ikHandle( curve = ctrlCurveName, ee = 'SK_' + ctrlCurveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstDynJoint, name = 'IKSPLINE_' + ctrlCurveName, ccv = 0 )
    ikName = ikName[0]

    # creation des offsets des joints
    offset(firstDynJoint)

    # offset de l'ik
    offset(ikName)

    # offset of the curve
    offset(ctrlCurveName)

    chaineDyn = 'SK_' + ctrlCurveName + '_'

# creation of driven bones chain
    firstDrivenJoint = cmds.joint( p= posPiv, name = 'SK_DRIVEN_' + dynCurveName + '_0')

    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = cmds.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_DRIVEN_' + dynCurveName + '_' + j )

    # offset of the driven bones chain
    offset(firstDrivenJoint)

    chaine1 = 'SK_DRIVEN_' + dynCurveName + '_'

# creation and positionning of the clusters and controlers
    for k in range( 0 , CVNumber ) :
        
        # creation of the clusters
        
        clusterNumber = str(k)
        CVName = ( ctrlCurveName + '.cv[' + clusterNumber + ']' )
        
        cmds.select( CVName )
        cluster = cmds.cluster()
        
        cmds.select( deselect = True )
        
        # Recuperation de la position des clusters
        positionClusterX = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].xValue' )
        positionClusterY = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].yValue' )
        positionClusterZ = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].zValue' )
        
        #------------------------------------------------------
        # Creation des Controleurs
        ctrlCluster = cmds.duplicate(selection[-1], name = 'CTRL_' + ctrlCurveName + '_' + clusterNumber)
        ctrlCluster = cmds.rename( ctrlCluster , 'CTRL_' + ctrlCurveName + '_' + clusterNumber )
        cmds.move( positionClusterX , positionClusterY , positionClusterZ , ctrlCluster , absolute = True )
        cmds.xform(ctrlCluster, ro = jointRotation)
        
        # Ofset des controleur ------------------
        offset(ctrlCluster)
        
        # ---------------------------------------------------------------
        
        
        # Parente des clusters sur les controleurs
        
        cmds.parent( cluster , ctrlCluster )

        if k==0:
            cmds.select(ctrlCluster)
            cmds.addAttr( ln='SWITCH', at='double', dv=0, minValue=0, maxValue=1 , h = False, k = True)
            nameReverse = ctrlCluster + '_REVERSE'
            cmds.shadingNode('reverse', asUtility=True, name = nameReverse)
            cmds.connectAttr(ctrlCluster + '.SWITCH', nameReverse + '.inputX')

            for l in range(0, jointsNumber):
                m = str(l)
                skChaine = chaine1 + m
                skChaineDyn = chaineDyn + m
                skChaineCTRL = chaineCTRL + m
                ctName = "chainConstrain" + m

                cmds.parentConstraint( skChaineDyn, skChaineCTRL, skChaine, name = ctName)
                cmds.connectAttr(ctrlCluster + '.SWITCH', ctName + '.' + skChaineDyn + 'W0')
                cmds.connectAttr(nameReverse + '.outputX', ctName + '.' + skChaineCTRL + 'W1')

    cmds.select( 'CTRL_' + ctrlCurveName + '_*_offset' )
    cmds.group( name= 'Group_CTRL_' + ctrlCurveName )
    cmds.select( deselect = True )