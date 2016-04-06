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
import maya.cmds as mc

selection = mc.ls(sl = True, fl = True)
numberOfCurves = len(selection)-1
print(numberOfCurves)

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
print( jointsNumber )

for i in range(0, numberOfCurves):

    # recuperation du nom de la shape
    curveName = selection[i]
    mc.select( curveName )
    selectionShape = mc.pickWalk( direction = 'down' )
    curveNameShape = selectionShape[0]
    
    print( curveName )
    print( curveNameShape )

    # calcul du nombre de CV
    curveDegree = mc.getAttr( curveNameShape + '.degree' )
    curveSpan = mc.getAttr( curveNameShape + '.spans' )

    CVNumber = curveDegree + curveSpan
    print( CVNumber )
    
    # placement du pivot au debut de la curve 
    curveInf = mc.createNode( 'curveInfo' , n=curveName + '_curveInfo' ) # Crée un node curveInfo
    mc.connectAttr( curveNameShape + '.worldSpace' , curveInf + '.inputCurve' )
    
    posCvX = mc.getAttr( curveInf + '.controlPoints[0].xValue' )
    posCvY = mc.getAttr( curveInf + '.controlPoints[0].yValue' )
    posCvZ = mc.getAttr( curveInf + '.controlPoints[0].zValue' )
    mc.xform( curveName, piv = ( posCvX , posCvY , posCvZ ) , ws = True )

    # creation du stretch
    mult = mc.shadingNode( 'multiplyDivide' , asUtility = True , name = 'multiplyDivide_STRETCH_' + curveName )
    mc.connectAttr( curveInf + '.arcLength' , mult + '.input1X' )
    curveArcLength = mc.getAttr( curveInf + '.arcLength' )
    mc.setAttr( mult + '.input2X' , curveArcLength )
    mc.setAttr( mult + '.operation' , 2 )

    # creation de la chaine de bones
    jointsTX = curveArcLength / bonesNumber
    print(jointsTX)
    firstJoint = mc.joint( p= (posCvX, posCvY, posCvZ), name = 'SK_' + curveName + '_0')
    
    for j in range ( 1 , jointsNumber ):
        j = str( j )
        currentJoint = mc.joint( p = ( jointsTX , 0 , 0 ) , r = True , name = 'SK_' + curveName + '_' + j )
        mc.connectAttr( mult + '.outputX', currentJoint + '.scaleX') # branchement du stretch

    # creation de l'ikSpline
    endEffectorNumber = str(bonesNumber)
    mc.ikHandle( curve = curveName, ee = 'SK_' + curveName + '_' + endEffectorNumber, sol = 'ikSplineSolver', sj = firstJoint, name = 'IKSPLINE_' + curveName, ccv = 0 )
    jointRotation = mc.xform( firstJoint, q=True, ro=True)
    print(jointRotation)

    # creation des offsets des joints
    skOffset = mc.group( em = True, name = firstJoint + '.offset')
    skConstraint = mc.parentConstraint( firstJoint, skOffset )
    mc.delete( skConstraint )
    mc.parent( firstJoint, skOffset)

    # offset de l'ik
    ikOffset = mc.group( em = True, name = 'IKSPLINE_' + curveName + '.offset')
    ikConstraint = mc.parentConstraint( 'IKSPLINE_' + curveName, ikOffset )
    mc.delete( ikConstraint )
    mc.parent( 'IKSPLINE_' + curveName, ikOffset)

    for k in range( 0 , CVNumber ) :
        
        # Creation des clusters :)
        
        clusterNumber = str(k)
        CVName = ( curveName + '.cv[' + clusterNumber + ']' )
        print(CVName)
        
        mc.select( CVName )
        cluster = mc.cluster()
        
        mc.select( deselect = True )
        
        # Recuperation de la position des clusters
        positionClusterX = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].xValue' )
        positionClusterY = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].yValue' )
        positionClusterZ = mc.getAttr( curveInf + '.controlPoints[' + clusterNumber + '].zValue' )
        print(positionClusterX)
        print(positionClusterY)
        print(positionClusterZ)
        
        #------------------------------------------------------
        # Creation des Controleurs
        ctrlCLuster = mc.duplicate(selection[-1], name = 'CTRL_' + curveName + '_' + clusterNumber)
        ctrlCLuster = mc.rename( ctrlCLuster , 'CTRL_' + curveName + '_' + clusterNumber )
        mc.move( positionClusterX , positionClusterY , positionClusterZ , ctrlCLuster , absolute = True )
        mc.xform(ctrlCLuster, ro = jointRotation)
        
        # Ofset des controleur ------------------
        
        clOffset = mc.group( em=True, name= ctrlCLuster + '_offset' )
        constraint = mc.parentConstraint( ctrlCLuster , clOffset )
        mc.delete(constraint)
        mc.parent( ctrlCLuster, clOffset )
        
        # ---------------------------------------------------------------
        
        
        # Parente des clusters sur les controleurs
        
        mc.parent( cluster , ctrlCLuster )

    mc.select( 'CTRL_' + curveName + '_*_offset' )
    mc.group( name= 'Group_CTRL_' + curveName )
    mc.select( deselect = True )