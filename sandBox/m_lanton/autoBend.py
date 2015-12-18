#--------------By MARTIN L'ANTON--------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#Thank to Christelle Giboin
#-----------------------------------
#--HOW TO USE IT--------------------
#-----------------------------------
#select all the curves you need to be dynamic, then the curve you want to use as controler for your clusters, and run the scripts, then you just have to specify the number of bones you want.
#-----------------------------------
import maya.cmds as cmds

selection = cmds.ls(sl = True, fl = True)
numberOfCurves = len(selection)-1
print(numberOfCurves)

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
print( jointsNumber )

for i in range(0, numberOfCurves):

    # recuperation du nom de la shape
    curveName = selection[i]
    cmds.select( curveName )
    selectionShape = cmds.pickWalk( direction = 'down' )
    curveNameShape = selectionShape[0]
    
    print( curveName )
    print( curveNameShape )

    # calcul du nombre de CV
    curveDegree = cmds.getAttr( curveNameShape + '.degree' )
    curveSpan = cmds.getAttr( curveNameShape + '.spans' )

    CVNumber = curveDegree + curveSpan
    print( CVNumber )
    
    # placement du pivot au debut de la curve 
    curveInf = cmds.createNode( 'curveInfo' , n=curveName + '_curveInfo' ) # Crée un node curveInfo
    cmds.connectAttr( curveNameShape + '.worldSpace' , curveInf + '.inputCurve' )
    
    posCvX = cmds.getAttr( curveInf + '.controlPoints[0].xValue' )
    posCvY = cmds.getAttr( curveInf + '.controlPoints[0].yValue' )
    posCvZ = cmds.getAttr( curveInf + '.controlPoints[0].zValue' )
    cmds.xform( curveName, piv = ( posCvX , posCvY , posCvZ ) , ws = True )

    # creation du stretch
    mult = cmds.shadingNode( 'multiplyDivide' , asUtility = True , name = 'multiplyDivide_STRETCH_' + curveName )
    cmds.connectAttr( curveInf + '.arcLength' , mult + '.input1X' )
    curveArcLength = cmds.getAttr( curveInf + '.arcLength' )
    cmds.setAttr( mult + '.input2X' , curveArcLength )
    cmds.setAttr( mult + '.operation' , 2 )

    # creation de la chaine de bones
    jointsTX = curveArcLength / bonesNumber
    print(jointsTX)
    firstJoint = cmds.joint( p= (posCvX, posCvY, posCvZ), name = 'SK_' + curveName + '_0')
    
    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = cmds.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_' + curveName + '_' + j )
        cmds.connectAttr( mult + '.outputX', currentJoint + '.scaleX') # branchement du stretch

    # creation de l'ikSpline
    endEffectorNumber = str(bonesNumber)
    cmds.ikHandle( curve = curveName, ee = 'SK_' + curveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstJoint, name = 'IKSPLINE_' + curveName, ccv = 0 )
    jointRotation = cmds.xform( firstJoint, q=True, ro=True)
    print(jointRotation)

    # creation des offsets des joints
    skOffset = cmds.group( em = True, name = firstJoint + '.offset')
    skConstraint = cmds.parentConstraint( firstJoint, skOffset )
    cmds.delete( skConstraint )
    cmds.parent( firstJoint, skOffset)

    # offset de l'ik
    ikOffset = cmds.group( em = True, name = 'IKSPLINE_' + curveName + '.offset')
    ikConstraint = cmds.parentConstraint( 'IKSPLINE_' + curveName, ikOffset )
    cmds.delete( ikConstraint )
    cmds.parent( 'IKSPLINE_' + curveName, ikOffset)

    for k in range( 0 , CVNumber ) :
        
        # Creation des clusters :)
        
        clusterNumber = str(k)
        CVName = ( curveName + '.cv[' + clusterNumber + ']' )
        print(CVName)
        
        cmds.select( CVName )
        cluster = cmds.cluster()
        
        cmds.select( deselect = True )
        
        # Recuperation de la position des clusters
        positionClusterX = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].xValue' )
        positionClusterY = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].yValue' )
        positionClusterZ = cmds.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].zValue' )
        print(positionClusterX)
        print(positionClusterY)
        print(positionClusterZ)
        
        #------------------------------------------------------
        # Creation des Controleurs
        ctrlCLuster = cmds.duplicate(selection[-1], name = 'CTRL_' + curveName + '_' + clusterNumber)
        ctrlCLuster = cmds.rename( ctrlCLuster , 'CTRL_' + curveName + '_' + clusterNumber )
        cmds.move( positionClusterX , positionClusterY , positionClusterZ , ctrlCLuster , absolute = True )
        cmds.xform(ctrlCLuster, ro = jointRotation)
        
        # Ofset des controleur ------------------
        
        clOffset = cmds.group( em=True, name= ctrlCLuster + '_offset' )
        constraint = cmds.parentConstraint( ctrlCLuster , clOffset )
        cmds.delete(constraint)
        cmds.parent( ctrlCLuster, clOffset )
        
        # ---------------------------------------------------------------
        
        
        # Parente des clusters sur les controleurs
        
        cmds.parent( cluster , ctrlCLuster )

    cmds.select( 'CTRL_' + curveName + '_*_offset' )
    cmds.group( name= 'Group_CTRL_' + curveName )
    cmds.select( deselect = True )