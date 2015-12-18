'''
__author__ = 'f.scaduto'
__version__ = 'V002'
'''

import maya.cmds as cmds
import sys

class tagTool():
    '''
    Tool to create cstr and locator for animation
    '''
    def __init__( self ):
        '''
        init Class
        '''
        pass

    def UI( self ):
        '''
        Create tag tool window
        :return:
        '''
        if cmds.window("tagToolWin", ex=True):
            cmds.deleteUI("tagToolWin", window=True)

        cmds.window("tagToolWin", wh=(300, 100), t="Tag Tool Stella Serie", s=False)

        cmds.columnLayout(adj=True)

        cmds.separator(w=270, height=5, style='in' )
        cmds.separator( style='none', height=5 )
        #cmds.rowColumnLayout( numberOfColumns=1, columnWidth=[(1, 135), (2, 135)])
        cmds.button(l="Create Locator", c=self.createLocator)
        #cmds.button(l="Create Set", c=self.NewSet)

        #cmds.setParent('..')

        cmds.separator(w=270, height=5, style='in' )
        cmds.separator( style='none', height=5 )
        cmds.text(l="Select parent then child")
        cmds.text(l="And click on Parent Constraint")
        cmds.separator( style='none', height=10 )
        cmds.button(l="Parent Constraint", c=self.constrain)
        cmds.separator(w=270, height=10, style='in' )
        cmds.separator( style='none', height=5 )

        cmds.text(l=" /!\  Optional  /!\ ")
        cmds.text(l="Add attribute on a existing constraint\nOr select an object / selection Set")
        cmds.text(l="And click on Add attribute")
        cmds.separator( style='none', height=10 )
        cmds.button(l="Add attribute", c=self.ajoutAttr)
        cmds.separator(w=270, height=10, style='in' )

        cmds.separator( style='none', height=5 )
        cmds.text(l="Select tagged object for verification")
        cmds.separator( style='none', height=10 )
        cmds.button(l="Select to check", c=self.selectObjConst)
        cmds.separator( style='none', height=10 )
        cmds.text(l="Click on Clean All to clean the scene")
        cmds.text(l="")
        cmds.separator( style='none', height=10 )
        cmds.button(l="Clean All", c=self.popup)
        cmds.separator( style='none', height=3 )
        cmds.separator(w=270, height=5, style='in' )

        cmds.showWindow("tagToolWin")


    def addPrefix(self, each):
        '''
        Add a prefix
        :param each:
        :return:
        '''
        prefix = "cubeCrea_"
        new_name = prefix + each.split("|")[-1]
        cmds.rename(each, new_name)

    def ajoutTag(self, *args):
        '''
        Add attribute with a category flag
        :return:
        '''
        newAttributName = 'CubeCreative'

        cmds.addAttr( longName=newAttributName, dataType = "string", keyable=False, hidden=True )

    def createLocator(self, *args):
        '''
        Create locator with a tag
        :return:
        '''
        newLoc = cmds.spaceLocator(n="cubeCrea_loc")
        cmds.select(newLoc)

        self.ajoutTag()
        sys.stderr.write("Locator Tagged created.\n")

    def constrain(self, *args):
        '''
        Create Parent contraint with a tag
        :return:
        '''
        cons_parent = cmds.parentConstraint(mo=True, n="cubeCreative_parentConstraint#", weight = 1)

        cmds.select (cons_parent)

        selection = cmds.ls(sl=True)
        for each in selection:
            test = cmds.listAttr(each)
            if "CubeCreative" in test:
                cmds.select (clear=True)
            else:
                self.ajoutTag()
                cmds.pickWalk( direction='up' )
                sys.stderr.write("New attribute has been added.\n")

    def selectObjConst(self, *args):
        '''
        Select object with a taged constraint
        :return:
        '''
        # Prepare return
        _return = []
        # List node with Attribute
        CubeCreative = cmds.ls("*.CubeCreative")
        # Clear Selection
        cmds.select (clear=True)
        # For each node
        for each in CubeCreative:
            # Recover object name
            _objName = each.split('.')[0]
            # Add to return
            _return.append(_objName)
            # Add to selection
            cmds.select(_objName, noExpand=True, add=True)
        # Returns the list
        return _return

    def ajoutAttr(self, *args):
        '''
        Add attribut on selected object
        :return:
        '''
        # Locals
        newAttributName = 'CubeCreative'
        prefix = "cubeCrea_"
        newList = []
        # Recover selection
        selection = cmds.ls(sl=True)
        # Deselect all
        cmds.select (clear=True)
        # For each elements
        for each in selection:
            # Attributs
            test = cmds.listAttr(each)
            # If allready added
            if newAttributName in test:
                # Add to newList
                newList.append(each)
                # Verbose
                sys.stderr.write("Attribute already exists on : %s\n" % each)
            # Else
            else:
                # Select current element
                cmds.select (each, r=True, noExpand=True)
                # Apply Attribut
                self.ajoutTag()
                # Rename Element
                new_name = prefix + each.split("|")[-1]
                cmds.rename(each, new_name)
                # Add a newList
                newList.append(new_name)
                # Verbose
                sys.stderr.write("New attribute has been added to : %s\n" % each)
        # Clear Selection
        cmds.select (clear=True)
        # Restore Selection
        for item in newList:
            cmds.select (item, add=True, noExpand=True)

    def killTmpTweenMachine(self):
        '''
        if tmXML1 exist, he is killed.
        :return:
        '''
        if cmds.objExists('tmXML1'):
            cmds.delete('tmXML1')
            print("tmXML1 deleted !")
        else:
            print("tmXML1 does not exists.")

    def bake(self, selectedObj):
        '''
        Bake object with a taged constraint
        :param selectedObj:
        :return:
        '''
        # Recover playback options
        startFrame = cmds.playbackOptions(q=True,minTime=True)
        endFrame = cmds.playbackOptions(q=True,maxTime=True)
        # Clear Selection
        cmds.select (clear=True)
        # List constraint in the scene
        _constraints = cmds.ls(type='constraint')
        # For each node
        for each in selectedObj:
            # If it's a constraint
            if each in _constraints:
                # Select constraint
                cmds.select (each, r=True, noExpand=True)
                # Select parents
                objectsToBake = cmds.pickWalk( direction='up' )
                # Bake
                cmds.bakeResults( objectsToBake, t=(startFrame,endFrame), simulation=True, shape=True )
        # For each node
        for each in selectedObj:
            # If object exists
            if selectedObj:
                # Delete Object
                cmds.delete(each)

    def killDisplayLayer(self):
        '''
        Kill display layers
        :return:
        '''
        listDisplayLayer = cmds.ls("*", typ='displayLayer')

        listDoNotTouch = []
        newElement = 'defaultLayer'
        listDoNotTouch.append(newElement)

        newListDisplayLayer=[]

        #Compare the two lists, and take out the new element in newListDisplayLayer list.
        for each in listDisplayLayer:
            if not each in listDoNotTouch:
                newListDisplayLayer.append(each)

        #Select and delete objects of the list
        for each in newListDisplayLayer:
            cmds.select(each, noExpand=True)
            cmds.delete(each)
            cmds.select(clear=True)

    def killMotionTrails(self):
        '''
        kill MotionTrails
        :return:
        '''
        # If motionsTrails exist, they are deleted.
        if cmds.objExists("motionTrail*"):
                motionTrailShapes = cmds.ls("motionTrail*Shape*")
                selectMotionTrailShapes = cmds.select(motionTrailShapes)
                pickWalkSelection = cmds.pickWalk(direction='up')
                cmds.delete(pickWalkSelection)
                print("MotionTrail(s) have been deleted.\n")

        else:
            print("MotionTrail(s) does not exist.\n")

    def unlockCam(self):
        '''
        Unload CamRef, Unlock file and Reload CamRef
        :return:
        '''
        camRef = 'CAM_aRN'
        # Unlock CAM_aRN and kill popUp error (prompt flag)
        cmds.file(unloadReference=camRef)
        cmds.setAttr(camRef+'.locked',0)
        cmds.file(loadReference=camRef, prompt=False)
        sys.stderr.write("%s is succefully Unlocked ! \n" % camRef)

    def clean(self):
        '''
        Clean the scene, delete tmp null, bake all tagged constraints and delete all stuff tagged
        :return:
        '''
        cubeObj = self.selectObjConst()
        self.killTmpTweenMachine()
        self.killDisplayLayer()
        self.killMotionTrails()
        self.bake(cubeObj)
        sys.stderr.write("Good Job ! All is Clean !\n")

    def popup(self, *args):
        '''
        Confirmation dialog when we click on Clean button
        :return:
        '''
        result = cmds.confirmDialog( title='Confirmation', message='Are you sure?', button=['Yes','No'], defaultButton='Yes', cancelButton='Yes', dismissString='No' )

        if result == 'Yes':
            self.clean()

        if result == 'No':
            pass

    def NewSet(self, *args):
        '''
        Prompt dialog when we click on Create Set button, and if OK create a new set with entered name
        :return:
        '''

        selection = cmds.ls( sl= True)

        if not selection:
            print '\n > Selection is empty'
            return

        pD_state = cmds.promptDialog(title="New Set",cancelButton="Cancel",defaultButton="OK",button=["OK", "Cancel"],message="Enter Name:",dismissString="Cancel")
        pD_name = cmds.promptDialog(query=1,text=1)

        if pD_state == 'Cancel':
            print '\nSet creation canceled'
            return
        else:
            fullName = "cubeCrea_"+pD_name
            newSet = cmds.sets( selection, n=fullName )
            newAttributName = 'CubeCreative'

            cmds.addAttr( newSet, longName=newAttributName, dataType = "string", keyable=False, hidden=True )
            print '\nSet succeffuly created and new attribute has been added to : ' + fullName
