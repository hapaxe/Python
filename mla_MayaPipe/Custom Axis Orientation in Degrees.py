# BETA PHASE
# CUSTOM AXIS ORIENTATION IN DEGREES
# BY PETER MAKAL

# 0.2.5.20131126001

import maya.cmds as cmds
import math

def caoidWindow() :

   """
      This function creates a Maya window.
    """

   caoid = 'caoid'      # Name of the window

   # Check if window already exists. If it exists, delete it.
   if cmds.window(caoid, ex=True) :
      cmds.deleteUI(caoid, window=True)

   # Build window
   cmds.window(
      caoid,
      title='Custom axis orientation in degrees',
      wh=(580, 370),
      retain=False)

   mainContainer = cmds.frameLayout(
      labelVisible=False,
      borderVisible=False,
      marginHeight=6,
      marginWidth=6)

   # This subContainer prevetns frameLayout children to scale in height
   subContainer = cmds.columnLayout(
      adjustableColumn=True,
      rowSpacing=4)
   # SUBCONTAINER CHILDREN : DESCRIPTION FRAME, CURRENT VALUES FRAME, SETTINGS FRAME

   # DESCRIPTION FRAME
   cmds.frameLayout(
      label="Description",
      borderStyle="etchedIn",
      marginHeight=3,
      labelIndent=5)
   cmds.columnLayout(
      columnAttach=("left", 18))
   cmds.text(
      l="This tool is setting up values in degrees for 'Custom axis orientation'.",
      align='left')
   cmds.setParent(subContainer)

   # CURRENT VALUES FRAME
   cmds.frameLayout(
      label="Current values in degrees",
      borderStyle="etchedIn",
      marginHeight=6,
      labelIndent=5)
   cmds.columnLayout(
      adjustableColumn=True,
      rowSpacing=4,
      columnAttach=("left", 18))

   # Retrieve current radian values from Move and Scale 'Custom axis orientation'
   curMoveVal = cmds.manipMoveContext('Move', query=True, orientAxes=True)
   curScaleVal = cmds.manipScaleContext('Scale', query=True, orientAxes=True)

   # Create a new list with converted values (Rad -> Deg)
   curMoveDegVal = []
   for i in curMoveVal :
      curMoveDegVal.append(math.degrees(i))
   curScaleDegVal = []
   for i in curScaleVal :
      curScaleDegVal.append(math.degrees(i))

   cmds.text(
      l='{0:>18} {1:>13} {2:>13}'.format('X', 'Y', 'Z'),
      align='left')
   cmds.text(
      l='Move: {0:>10.3f} {1:>10.3f} {2:>10.3f}'.format(curMoveDegVal[0], curMoveDegVal[1], curMoveDegVal[2]),
      align='left')
   cmds.text(
      l='Scale: {0:>10.3f} {1:>10.3f} {2:>10.3f}'.format(curScaleDegVal[0], curScaleDegVal[1], curScaleDegVal[2]),
      align='left')
   cmds.setParent(subContainer)

   # SETTINGS FRAME
   cmds.frameLayout(
      label='Settings',
      borderStyle='etchedIn',
      marginHeight=3,
      labelIndent=5)
   cmds.columnLayout(
      adjustableColumn=True)
   xDeg = cmds.floatSliderGrp(
      l='X axis (deg):',
      field=True,
      minValue=-360, maxValue=360,
      fieldMinValue=-360, fieldMaxValue=360,
      columnAttach3=('right', 'both', 'left'),
      columnOffset3=(6, 0, 0))
   yDeg = cmds.floatSliderGrp(
      l='Y axis (deg):',
      field=True,
      minValue=-360, maxValue=360,
      fieldMinValue=-360, fieldMaxValue=360,
      columnAttach3=('right', 'both', 'left'),
      columnOffset3=(6, 0, 0))
   zDeg = cmds.floatSliderGrp(
      l='Z axis (deg):',
      field=True,
      minValue=-360, maxValue=360,
      fieldMinValue=-360, fieldMaxValue=360,
      columnAttach3=('right', 'both', 'left'),
      columnOffset3=(6, 0, 0))
   relativeOpt = cmds.checkBoxGrp(
      label='',
      numberOfCheckBoxes=1,
      label1='Relative',
      annotation="""When checked, add to or subtract from current seted values
   of X, Y or Z in 'Custom axis orientation.'""")

   cmds.separator(height=10, style='in')

   applyFor = cmds.checkBoxGrp(
      label='Apply for:',
      numberOfCheckBoxes=3,
      vertical=True,
      columnAttach2=('right', 'left'),
      columnOffset2=(6, 2),
      labelArray3=('Move', 'Rotate', 'Scale'),
      enable2=False)      # disable Rotate for the time being
   cmds.setParent(mainContainer)

   # BUTTONS SECTION
   form = cmds.formLayout(numberOfDivisions=100)

   def clickCmd(buttonValue) :
      degToRad(xDeg, yDeg, zDeg, relativeOpt, applyFor)
   applyButton = cmds.button(
      l='Apply',
      height=26,
      c=clickCmd)

   closeCmd = 'cmds.deleteUI("%s", window=True)' % caoid
   closeButton = cmds.button(
      l='Close',
      height=26,
      c=closeCmd)

   cmds.formLayout(
      form, edit=True,
      attachForm=(
         (applyButton, 'bottom', 0),
         (applyButton, 'left', 0),
         (closeButton, 'bottom', 0),
         (closeButton, 'right', 0)),
      attachPosition=(
         (applyButton, 'right', 2, 50),
         (closeButton, 'left', 2, 50)))

   cmds.showWindow(caoid)


def degToRad(xDeg, yDeg, zDeg, relativeOpt, applyFor) :
   """
      This function sets degree values and converts them to radians
      within 'Custom axis orientation'.
   """
   
   # Retrieve degrees data from floatSliderGrp
   xDegVal = cmds.floatSliderGrp(xDeg, query=True, value=True)
   yDegVal = cmds.floatSliderGrp(yDeg, query=True, value=True)
   zDegVal = cmds.floatSliderGrp(zDeg, query=True, value=True)
   
   # Convert data to radians
   xRadVal = math.radians(xDegVal)
   yRadVal = math.radians(yDegVal)
   zRadVal = math.radians(zDegVal)
   
   # Find out what boxes were checked and assign those states to variables
   relativeState = cmds.checkBoxGrp(relativeOpt, query=True, value1=True)                  # Relative checkbox
   moveState = cmds.checkBoxGrp(applyFor, query=True, value1=True)            # Move checkbox
   rotateState = cmds.checkBoxGrp(applyFor, query=True, value2=True)         # Rotate checkbox
   scaleState = cmds.checkBoxGrp(applyFor, query=True, value3=True)         # Scale checkbox
   
   # Execute
   if moveState == True :
      # If Relative checkbox - Checked
      if relativeState == True :
         # Retrieve current radian values from Move 'Custom axis orientation'
         curMoveVal = cmds.manipMoveContext('Move', query=True, orientAxes=True)
         # Add new values to current ones
         xRadMoveVal = xRadVal + curMoveVal[0]
         yRadMoveVal = yRadVal + curMoveVal[1]
         zRadMoveVal = zRadVal + curMoveVal[2]
         cmds.manipMoveContext('Move', e=True, mode=6, oa=(xRadMoveVal, yRadMoveVal, zRadMoveVal))
         cmds.setToolTo('moveSuperContext')
      # If Relative checkbox - Unchecked
      else :   
         cmds.manipMoveContext('Move', e=True, mode=6, oa=(xRadVal, yRadVal, zRadVal))
         cmds.setToolTo('moveSuperContext')
   
   if rotateState == True :
      pass   # future code for rotate [RotateSuperContext]
   
   if scaleState == True :
      # If Relative checkbox - Checked
      if relativeState == True :
         # Retrieve current radian values from Scale 'Custom axis orientation'
         curScaleVal = cmds.manipScaleContext('Scale', query=True, orientAxes=True)
         # Add new values to current ones
         xRadScaleVal = xRadVal + curScaleVal[0]
         yRadScaleVal = yRadVal + curScaleVal[1]
         zRadScaleVal = zRadVal + curScaleVal[2]
         cmds.manipScaleContext('Scale', e=True, mode=6, oa=(xRadScaleVal, yRadScaleVal, zRadScaleVal))
         cmds.setToolTo('scaleSuperContext')
      # If Relative checkbox - Unchecked
      else :   
         cmds.manipScaleContext('Scale', e=True, mode=6, oa=(xRadVal, yRadVal, zRadVal))
         cmds.setToolTo('scaleSuperContext')

   
caoidWindow()