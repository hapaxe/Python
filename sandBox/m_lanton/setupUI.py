__author__ = 'm.lanton'
import maya.cmds as mc
import sandBox.m_lanton.ml_utilities as mlutilities
import sandBox.m_lanton.bend as bend
reload(bend)
reload(mlutilities)

widget = {}


# ----------------------------------------------------------------
def ui():
    if mc.window('setup Tool', exists=True):
        mc.deleteUI('setup Tool')


    widget["window"] = mc.window('setup Tool', title="create deformer", iconName='Short Name')

    form = mc.formLayout()
    tabs = mc.tabLayout( innerMarginWidth=5, innerMarginHeight=5)
    mc.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

    #first tab
    tab1 = mc.rowColumnLayout( numberOfColumns=1, columnAlign=(1, 'right'), columnAttach=(2, 'both', 0) )

    bend_options = mc.radioButtonGrp( label='Bounds',
                                   labelArray2=['simple','bounds'],
                                   numberOfRadioButtons=2,
                                   cl3=["left","left","left"],
                                   parent=tab1,
                                   cc='armSym = getSym("arm")' )

    obj1 = mc.button( 'obj 1' , label='Create bendSquash system' , command=('bend.create_bend_squash'))
    #bend.create_bend_squash()

    mc.button( label='Close', command=('cmds.deleteUI(\"' + widget["window"] + '\", window=True)') )

    mc.tabLayout( tabs, edit=True, tabLabel=((tab1, 'Create Deformer')) )

    mc.showWindow( widget["window"] )