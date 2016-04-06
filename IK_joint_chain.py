__author__ = 'm.lanton'
# --------------By MARTIN L'ANTON--------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#---------------------------------------------
#-----------------------------------
#--HOW TO USE IT--------------------
#-----------------------------------
#select all the curves you need to be rigged, then the curve you want to use as controler for your clusters,
#and run the scripts, then you just have to specify the number of bones you want.
#-----------------------------------
import maya.cmds as mc

import ml_utilities as mlutilities


def ik_joint_chain():
    selection = mc.ls(sl=True, fl=True)
    numberOfCurves = len(selection) - 1
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

    else:
        Annulation = mc.confirmDialog(
            title='Confirm',
            message='You have to type a number of bone(s)',
            button=['Yes'],
            defaultButton='Yes')

    bonesNumber = int(bonesNumber)
    jointsNumber = bonesNumber + 1

    for i in range(0, numberOfCurves):

        # get name of the shape
        curveName = selection[i]
        mc.select(curveName)
        selectionShape = mc.pickWalk(direction='down')
        curveNameShape = selectionShape[0]

        # get number of CV
        curveDegree = mc.getAttr(curveNameShape + '.degree')
        curveSpan = mc.getAttr(curveNameShape + '.spans')

        CVNumber = curveDegree + curveSpan

        # pivot at the start of the curve
        curveInf = mc.createNode('curveInfo', n=curveName + '_curveInfo')  # curveInfo node creation
        mc.connectAttr(curveNameShape + '.worldSpace', curveInf + '.inputCurve')

        posCvX = mc.getAttr(curveInf+'.controlPoints[0].xValue')
        posCvY = mc.getAttr(curveInf+'.controlPoints[0].yValue')
        posCvZ = mc.getAttr(curveInf+'.controlPoints[0].zValue')
        mc.xform(curveName, piv=(posCvX, posCvY, posCvZ), ws=True)

        # stretch creation
        mult = mc.shadingNode('multiplyDivide', asUtility=True, name='multiplyDivide_STRETCH_' + curveName)
        mc.connectAttr(curveInf + '.arcLength', mult + '.input1X')
        curveArcLength = mc.getAttr(curveInf + '.arcLength')
        mc.setAttr(mult + '.input2X', curveArcLength)
        mc.setAttr(mult + '.operation', 2)

        # bones chain creation
        jointsTX = curveArcLength / bonesNumber
        firstJoint = mc.joint(p=(posCvX, posCvY, posCvZ), name='SK_' + curveName + '_0')
        mc.connectAttr(mult + '.outputX', firstJoint + '.scaleX')  # branchement du stretch

        for j in range(0, jointsNumber-1):
            j = str(j+1)
            currentJoint = mc.joint(p=(jointsTX, 0, 0), r=True, name='SK_' + curveName + '_' + j)
            mc.connectAttr(mult + '.outputX', currentJoint + '.scaleX')  # branchement du stretch

        # ikSpline creation
        endEffectorNumber = str(bonesNumber)
        mc.ikHandle(curve=curveName, ee='SK_' + curveName + '_' + endEffectorNumber, sol='ikSplineSolver', sj=firstJoint,
                    name='IKSPLINE_' + curveName, ccv=0)
        jointRotation = mc.xform(firstJoint, q=True, ro=True)
        print(jointRotation)

        # joints offset
        skOffset = mc.group(em=True, name=firstJoint + '.offset')
        skConstraint = mc.parentConstraint(firstJoint, skOffset)
        mc.delete(skConstraint)
        mc.parent(firstJoint, skOffset)

        # ik offset
        ikOffset = mc.group(em=True, name='IKSPLINE_' + curveName + '.offset')
        ikConstraint = mc.parentConstraint('IKSPLINE_' + curveName, ikOffset)
        mc.delete(ikConstraint)
        mc.parent('IKSPLINE_' + curveName, ikOffset)

        ctrl_list = list()

        for k in range(0, CVNumber):
            # clusters creation

            clusterNumber = str(k)
            CVName = (curveName + '.cv[' + clusterNumber + ']')
            print(CVName)

            mc.select(CVName)
            cluster = mc.cluster()
            mc.setAttr(cluster[0] + 'Handle.visibility', 0)

            mc.select(deselect=True)

            # get clusters position
            positionClusterX = mc.getAttr(curveInf + '.controlPoints[' + clusterNumber + '].xValue')
            positionClusterY = mc.getAttr(curveInf + '.controlPoints[' + clusterNumber + '].yValue')
            positionClusterZ = mc.getAttr(curveInf + '.controlPoints[' + clusterNumber + '].zValue')
            print(positionClusterX)
            print(positionClusterY)
            print(positionClusterZ)

            #------------------------------------------------------
            # controllers creation
            ctrlCLuster = mc.duplicate(selection[-1], name=curveName + '_' + clusterNumber + '_ctrl')
            ctrlCLuster = mc.rename(ctrlCLuster, curveName + '_' + clusterNumber + '_ctrl')
            mlutilities.color([curveName + '_' + clusterNumber + '_ctrl'], 'yellow')
            mc.move(positionClusterX, positionClusterY, positionClusterZ, ctrlCLuster, absolute=True)
            mc.xform(ctrlCLuster, ro=jointRotation)

            # controllers offset ------------------

            clOffset = mc.group(em=True, name=ctrlCLuster + '_offset')
            constraint = mc.parentConstraint(ctrlCLuster, clOffset)
            mc.delete(constraint)
            mc.parent(ctrlCLuster, clOffset)

            # ---------------------------------------------------------------
            # parent clusters on controllers

            mc.parent(cluster, ctrlCLuster)
            ctrl_list.append(clOffset)


        mc.group(ctrl_list, name='Group_CTRL_' + curveName)
        mc.select(deselect=True)