# ArcLenthSpline.py
# -------------- Par Christelle GIBOIN -------------
# Outil pour le Bend 
# Script permettant d'automatiser le scale des bone sur un IK spline Youhou !!

#Selectioner D'abord la curve de l'IK Spline puis le premier joint de la chaine concernée :)


import maya.cmds as cmds
import random


SelectionList = cmds.ls( orderedSelection=True )

#>>>  retourne les objets dans le même order que la
#sélection faite par l'utilistateur'''


# récupération des variable de la curve et des bones
NameCurve = SelectionList[0]
NameSK = SelectionList[1]

cmds.select( NameCurve )
cmds.pickWalk( direction='down' )
SelectionShape = cmds.ls( sl = True )
NomCurveShape = SelectionShape[0]

print(NameCurve)
print(NameSK)

# Création de l'arclength 
Arc = cmds.arcLengthDimension ( NomCurveShape + '.u[1]' )
print(Arc)
NomArclength = cmds.select( NomCurveShape + '->arcLengthDimension*' )
Arc = cmds.rename( NomArclength , NameCurve + '_Arc_length' )
print(Arc)

# récupération de la longuere de la chaine au repos
Longueurzero = cmds.getAttr( Arc + 'Shape.arcLength' )

print(Longueurzero)

#Création d'un node Multiply divide
MD = cmds.createNode( 'multiplyDivide' , n = NameCurve + '_MD_Arc_length' )

print(MD)

#initialisation du Multiply Divide pour le calcul de la longueur
cmds.setAttr( MD + '.input2X' , Longueurzero )
cmds.setAttr( MD + '.operation' , 2 )

# Connection des attribut entre l'arcLength et le Multiply divide 
cmds.connectAttr( Arc + 'Shape.arcLength' , MD +'.input1X' )

#cmds.selectMode( leaf = True  )


cmds.select( NameSK , hierarchy = True )

ListSK = cmds.ls( sl=True )

NumbersOfSk = len( ListSK )

print(NumbersOfSk)

#Etablir les connection etre le MD et les Joints

for i in range( 0 , NumbersOfSk - 1 ) :
    print( ListSK[i] )
    cmds.connectAttr( MD + '.outputX' , ListSK[i] +'.scaleX' )

#---------------------------------------------------------------------------------------------------

