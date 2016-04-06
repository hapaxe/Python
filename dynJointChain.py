#--------------By MARTIN L'ANTON
#
#
#-----------------------------------
#--HOW TO USE IT--------------------
#-----------------------------------
#select all the curves you need to be dynamic, then the curve you want to use as controler for your clusters, and run the scripts, then you just have to specify the number of bones you want.
#-----------------------------------
import maya.cmds as mc

#define how to offset
def offset(var):
    offset = mc.group( em = True, name = var + '_offset')
    constraint = mc.parentConstraint( var, offset )
    mc.delete( constraint )
    mc.parent( var, offset)
    return offset

#define how to get the name of the shape
def nameShape(var1):
    mc.select( var1 )
    selectionShape = mc.pickWalk( direction = 'down' )
    return selectionShape[0]

# define how to create a stretch network
def stretch(obj1, obj2):
    curveInf = mc.createNode( 'curveInfo' , n = obj1 + '_curveInfo' ) # Crée un node curveInfo
    mc.connectAttr( obj2 + '.worldSpace' , curveInf + '.inputCurve' )
    mult = mc.shadingNode( 'multiplyDivide' , asUtility = True , name = 'MULT_STRETCH_' + obj1 )
    mc.connectAttr( curveInf + '.arcLength' , mult + '.input1X' )
    curveArcLength = mc.getAttr( curveInf + '.arcLength' )
    mc.setAttr( mult + '.input2X' , curveArcLength )
    mc.setAttr( mult + '.operation' , 2 )
    return mult

# creation de la chaine de bones
def jointChain(pos1, obj1) :
    firstChainJoint = mc.joint( p= pos1, name = 'SK_' + obj1 + '_0')
    mult = 'MULT_STRETCH_' + obj1
    mc.connectAttr( mult + '.outputX', firstChainJoint + '.scaleX') # branchement du stretch

    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = mc.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_' + obj1 + '_' + j )
        mc.connectAttr( mult + '.outputX', currentJoint + '.scaleX') # branchement du stretch

    return firstChainJoint


selection = mc.ls(sl = True, fl = True)
numberOfCurves = len(selection)-1

# dialog box
result = mc.promptDialog(
        title='Numbre of bones',
        message='Type the number of bones that you want on your curve(s)',    
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

if result == 'OK':
            bonesNumber = mc.promptDialog(query=True, text=True)
    
else :
            Anulation = mc.confirmDialog(
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
    curveDegree = mc.getAttr( dynCurveNameShape + '.degree' )
    curveSpan = mc.getAttr( dynCurveNameShape + '.spans' )

    CVNumber = curveDegree + curveSpan
    
    # creation du stretch
    multCtrl = stretch(dynCurveName, dynCurveNameShape)
    curveInf = dynCurveName + '_curveInfo'
    curveArcLength = mc.getAttr( dynCurveName + '_curveInfo.arcLength' )
    jointsTX = curveArcLength / bonesNumber
    
    posCvX = mc.getAttr( curveInf + '.controlPoints[0].xValue' )
    posCvY = mc.getAttr( curveInf + '.controlPoints[0].yValue' )
    posCvZ = mc.getAttr( curveInf + '.controlPoints[0].zValue' )
    posPiv = (posCvX, posCvY, posCvZ)
    mc.xform( dynCurveName, piv = ( posCvX , posCvY , posCvZ ) , ws = True )

    # ctrl curve creation
    ctrlCurveName = mc.duplicate(dynCurveName)
    ctrlCurveName = mc.rename(ctrlCurveName, 'CTRL_' + dynCurveName)   
    ctrlCurveNameShape = nameShape(ctrlCurveName)
    print(ctrlCurveName)

    multDyn = stretch(ctrlCurveName, ctrlCurveNameShape)



# creation of dynamic bones and ik
    firstJoint = jointChain(posPiv, dynCurveName)


    # creation de l'ikSpline
    endEffectorNumber = str(bonesNumber)
    ikName = mc.ikHandle( curve = dynCurveName, ee = 'SK_' + dynCurveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstJoint, name = 'IKSPLINE_' + dynCurveName, ccv = 0 )
    ikName = ikName[0]
    jointRotation = mc.xform( firstJoint, q=True, ro=True)

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
    ikName = mc.ikHandle( curve = ctrlCurveName, ee = 'SK_' + ctrlCurveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstDynJoint, name = 'IKSPLINE_' + ctrlCurveName, ccv = 0 )
    ikName = ikName[0]

    # creation des offsets des joints
    offset(firstDynJoint)

    # offset de l'ik
    offset(ikName)

    # offset of the curve
    offset(ctrlCurveName)

    chaineDyn = 'SK_' + ctrlCurveName + '_'

# creation of driven bones chain
    firstDrivenJoint = mc.joint( p= posPiv, name = 'SK_DRIVEN_' + dynCurveName + '_0')

    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = mc.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_DRIVEN_' + dynCurveName + '_' + j )

    # offset of the driven bones chain
    offset(firstDrivenJoint)

    chaine1 = 'SK_DRIVEN_' + dynCurveName + '_'

# creation and positionning of the clusters and controlers
    for k in range( 0 , CVNumber ) :
        
        # creation of the clusters
        
        clusterNumber = str(k)
        CVName = ( ctrlCurveName + '.cv[' + clusterNumber + ']' )
        
        mc.select( CVName )
        cluster = mc.cluster()
        
        mc.select( deselect = True )
        
        # Recuperation de la position des clusters
        positionClusterX = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].xValue' )
        positionClusterY = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].yValue' )
        positionClusterZ = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].zValue' )
        
        #------------------------------------------------------
        # Creation des Controleurs
        ctrlCluster = mc.duplicate(selection[-1], name = 'CTRL_' + ctrlCurveName + '_' + clusterNumber)
        ctrlCluster = mc.rename( ctrlCluster , 'CTRL_' + ctrlCurveName + '_' + clusterNumber )
        mc.move( positionClusterX , positionClusterY , positionClusterZ , ctrlCluster , absolute = True )
        mc.xform(ctrlCluster, ro = jointRotation)
        
        # Ofset des controleur ------------------
        offset(ctrlCluster)
        
        # ---------------------------------------------------------------
        
        
        # Parente des clusters sur les controleurs
        
        mc.parent( cluster , ctrlCluster )

        if k==0:
            mc.select(ctrlCluster)
            mc.addAttr( ln='SWITCH', at='double', dv=0, minValue=0, maxValue=1 , h = False, k = True)
            nameReverse = ctrlCluster + '_REVERSE'
            mc.shadingNode('reverse', asUtility=True, name = nameReverse)
            mc.connectAttr(ctrlCluster + '.SWITCH', nameReverse + '.inputX')

            for l in range(0, jointsNumber):
                m = str(l)
                skChaine = chaine1 + m
                skChaineDyn = chaineDyn + m
                skChaineCTRL = chaineCTRL + m
                ctName = "chainConstrain" + m

                mc.parentConstraint( skChaineDyn, skChaineCTRL, skChaine, name = ctName)
                mc.connectAttr(ctrlCluster + '.SWITCH', ctName + '.' + skChaineDyn + 'W0')
                mc.connectAttr(nameReverse + '.outputX', ctName + '.' + skChaineCTRL + 'W1')

    mc.select( 'CTRL_' + ctrlCurveName + '_*_offset' )
    mc.group( name= 'Group_CTRL_' + ctrlCurveName )
    mc.select( deselect = True )