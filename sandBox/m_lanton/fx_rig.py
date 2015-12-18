__author__ = 'm.lanton'
import maya.cmds as mc

def fx_alembic_setup(*args):
    #defines selection
    selection = mc.ls(sl=True)
    #query the list of names for enum list attribute
    enum_list = mc.scrollField(enum_field, q=True, tx=True)
    enum_list = eval(enum_list)
    attr_list = ':'.join(enum_list)
    print attr_list

    #check if there is the good number of names given
    if len(selection) != len(enum_list):
        print 'You must enter the same number of names than selected objects'
    else:
        #get cube name
        name = str(str((mc.file(q=True, loc=True)).split('/')[-1]).split('_')[1])

        #create the enum list attribute on the walk_ctrl for the switch
        mc.addAttr('walk_ctrl', at='enum', sn='chooser', enumName=attr_list, k=True, h=False)

        #add the start frame attribute to the walk ctrl and set it
        mc.addAttr('walk_ctrl', at='float', sn='startFrame', nn='Start Frame', k=True, h=False)
        mc.setAttr('walk_ctrl.startFrame', 101)

        #create plusMinusAverage node to calculate the offset to give to the alembic nodes
        plus_min_av = mc.createNode('plusMinusAverage', name=name + '_plusMinusAverage')
        #set the plusMinusAverage
        mc.setAttr(plus_min_av+'.operation', 2)
        mc.setAttr(plus_min_av+'.input1D[2]', 101)
        #connect walk startFrame to plusMinusAverage
        mc.connectAttr('walk_ctrl.startFrame', plus_min_av+'.input1D[0]')

        #exectutes operation for each selected mesh
        for i in range(0, len(selection)):
            node = selection[i]
            #get the shape of the selected mesh
            shape = mc.listRelatives(node, c=True, shapes=True)[0]
            #get the alembicNode connected to that shape
            alembic_node = mc.listConnections(shape+'.inMesh', d=False, s=True)[0]
            #connect the plusMinusAverage to the alembicNode offset
            mc.connectAttr(plus_min_av+'.output1D', alembic_node+'.offset')

            #create the condition node
            cond_node = mc.createNode('condition', name=node+'_condition')
            #connect the enum attribute to the condition node
            mc.connectAttr('walk_ctrl.chooser', cond_node+'.firstTerm')
            #set the condition node
            mc.setAttr(cond_node+'.secondTerm', i)
            mc.setAttr(cond_node+'.operation', 0)
            mc.setAttr(cond_node+'.colorIfTrueR', 1)
            mc.setAttr(cond_node+'.colorIfFalseR', 0)
            #connect the output of the condition node
            mc.connectAttr(cond_node+'.outColorR', node+'.visibility')



def fx_alembic_UI():
    global enum_field
    if mc.window('fx alembic setup', exists=True):
        mc.deleteUI('fx alembic setup')

    #window
    window = mc.window('fx alembic setup', title='fx alembic setup')
    #main layout
    mc.columnLayout(adjustableColumn=True)
    #list field
    enum_field = mc.scrollField(editable=True, wordWrap=True,
                                text='[\'Enter the list of the names you want to appear in the enum attribute\']')
    #setup button
    mc.button(label='Setup', command=fx_alembic_setup)

    mc.showWindow(window)