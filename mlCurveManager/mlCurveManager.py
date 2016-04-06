__author__ = 'Martin'
import maya.cmds as mc
# import sys
# import os
import ml_json_utilities as json

PROJECT_PATH = 'E:/development/Python/'
ROOT_PATH = 'sandBox/m_lanton/'

widgets = dict()


# ----------------------------------------------------------------
def curve_manager_ui():
    # initialize values
    widgets['curve_type'] = 'circle'
    widgets['curve_name'] = 'ctrl'
    widgets['orientation'] = [0, 0, 0]
    widgets['mirror'] = [0, 0, 0]

    if mc.window('CurveManager_Window', exists=True):
        mc.deleteUI('CurveManager_Window', window=True)
    if mc.dockControl('CurveManager', exists=True):
        mc.deleteUI('CurveManager')

    # --- Create window-------------------------------------------------------------------------------------------------
    widgets['window'] = mc.window('CurveManager_Window')
    # formlayout and tabs
    widgets['form'] = mc.formLayout()
    widgets['tabs'] = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    mc.formLayout(widgets['form'], edit=True, attachForm=((widgets['tabs'], 'top', 0),
                                                          (widgets['tabs'], 'left', 0),
                                                          (widgets['tabs'], 'bottom', 0),
                                                          (widgets['tabs'], 'right', 0)))

    # creation tab------------------------------------------------------------------------------------------------------
    widgets['creation_layout'] = mc.rowColumnLayout(parent=widgets['tabs'], w=300)
    # creation options
    # line 1 : name/curve_name
    widgets['nameField'] = mc.textFieldGrp('ui_nameField', label=' Name', text='', columnAlign2=['left', 'left'],
                                           columnWidth2=[75, 225])
    # line 2 : list/curve_type
    widgets['curve_list'] = mc.optionMenuGrp('ui_curve_list', label=' Curve', columnAlign2=['left', 'left'],
                                             columnWidth2=[75, 225], adjustableColumn2=2,
                                             parent=widgets['creation_layout'])
    # line 3 : orientation
    widgets['orientation_menu'] = mc.radioButtonGrp('ui_orientation_menu', label=' Orientation',
                                                    labelArray3=['X', 'Y', 'Z'], select=2, numberOfRadioButtons=3,
                                                    columnWidth4=[75, 75, 75, 75],
                                                    columnAlign4=['left', 'left', 'left', 'left'])
    # line 4 : mirroring
    widgets['mirror_menu'] = mc.checkBoxGrp('ui_mirror_menu', label=' Mirror', numberOfCheckBoxes=3, label1='X',
                                            label2='Y', label3='Z', columnWidth4=[75, 75, 75, 75],
                                            columnAlign4=['left', 'left', 'left', 'left'])
    # line 5 : creation button
    widgets['creation_button'] = mc.button(label='Creation')
    # line 6 : remove shape option (edition mode only)
    widgets['remove_shape'] = mc.checkBoxGrp('remove_shape', label=' Remove Shape', numberOfCheckBoxes=1,
                                             columnWidth2=[75, 75], columnAlign2=['left', 'left'])
    # line 7 : edition button
    widgets['edition_button'] = mc.button(label='Edition')

    # managing_layout tab-----------------------------------------------------------------------------------------------
    widgets['managing_layout'] = mc.rowColumnLayout(numberOfColumns=2, parent=widgets['tabs'])

    mc.tabLayout(widgets['tabs'], edit=True, tabLabel=((widgets['creation_layout'], 'creation/edition'),
                                                       (widgets['managing_layout'], 'managing')))

    widgets['allowedAreas'] = ['right', 'left']
    widgets['dock'] = mc.dockControl('CurveManager',
                                     area='left', content=widgets['window'], allowedArea=widgets['allowedAreas'], w=320)

    mc.showWindow(widgets['dock'])


# ----------------------------------------------------------------
def get_curve():
    # get selection
    selection = mc.ls(sl=True)
    # get the name of the curve
    curve_type = selection[0]
    # get the name of the curve
    curve_shape_name = mc.listRelatives(curve_type, s=True)[0]

    # get the degree, spans and calculate the numbers of CV of the curve
    curve_degree = mc.getAttr(curve_shape_name + '.degree')
    curve_span = mc.getAttr(curve_shape_name + '.spans')
    cv_number = curve_degree + curve_span

    # create a curveInfo node and connect it to the curve
    curve_info = mc.createNode('curveInfo', n=curve_type + '_curveInfo')  # curveInfo node creation
    mc.connectAttr(curve_type + '.worldSpace', curve_info + '.inputCurve')

    # get the knots of the curve
    knots = mc.getAttr(curve_info+'.knots')[0]

    # create an empty list for the coordinates of the points of the curve
    points = list()
    # fill the list of points coordinates
    for i in range(0, cv_number):
        point = mc.getAttr(curve_info+'.controlPoints['+str(i)+']')
        points.append(point[0])

    curve_dict = {'degree': curve_degree, 'points': points, 'knots': knots}

    json.save_to_json(curve_dict, PROJECT_PATH+ROOT_PATH+'curve_dictionaries'+curve_type+'.json')



# ----------------------------------------------------------------
def create_curve(curve_type='circle', name='ctrl'):
    curve_dict = json.load_from_json(PROJECT_PATH+ROOT_PATH+'curve_dictionaries'+curve_type+'.json')
    degree = curve_dict['degree']
    points = curve_dict['points']
    knots = curve_dict['knots']
    
    mc.curve(n=name, d=degree, p=points, k=knots)
    return name


# ----------------------------------------------------------------
def curve_placement():
    mirror = get_mirror()
    orientation = get_orientation()
    curve_type = get_curve_type()
    curve_name = get_curve_name()

    selection = mc.ls(sl=True)
    i = 0

    for node in selection:
        # init infos
        curve_name += '_'+str(i)
        translation = mc.xform(node, q=True, translation=True, a=True)
        rotation = mc.xform(node, q=True, rotation=True, a=True)
        rotation = (rotation[0]+orientation[0], rotation[1]+orientation[1], rotation[2]+orientation[2])
        # create the curve
        ctrl = create_curve(curve_type=curve_type, name=curve_name)
        # place the curve
        # scale
        mc.xform(ctrl, scale=mirror)
        mc.makeIdentity(ctrl, s=True, apply=True)
        # translate
        mc.xform(ctrl, translation=translation)
        # rotate
        mc.xform(ctrl, rotation=rotation)

        orig(ctrl)


# ----------------------------------------------------------------
def get_mirror():
    mirror = [1, 1, 1]
    if mc.checkBoxGrp(widgets['mirror_menu'], q=True, enable1=True):
        mirror[0] = -1
    if mc.checkBoxGrp(widgets['mirror_menu'], q=True, enable2=True):
        mirror[1] = -1
    if mc.checkBoxGrp(widgets['mirror_menu'], q=True, enable3=True):
        mirror[2] = -1

    widgets['mirror'] = mirror

    return widgets['mirror']


# ----------------------------------------------------------------
def get_orientation():
    orientation = mc.radioButtonGrp(widgets['orientation_menu'], q=True, select=True)

    if orientation == 1:
        widgets['orientation'] = [0, 0, 90]
    elif orientation == 2:
        widgets['orientation'] = [0, 0, 0]
    else:
        widgets['orientation'] = [90, 0, 0]

    return widgets['orientation']


# ----------------------------------------------------------------
def get_curve_type():
    widgets['curve_type'] = mc.optionMenuGrp(widgets['curve_list'], q=True, value=True)

    return widgets['curve_type']


# ----------------------------------------------------------------
def get_curve_name():
    widgets['curve_name'] = mc.textFieldGrp(widgets['nameField'], q=True, text=True)

    return widgets['curve_name']


# ----------------------------------------------------------------
def orig(node='empty'):
    """
    Cree un group offset orig
    :param node: string : name of the node to offset
    :return: string : name of the orig
    """

    if node == 'empty':
        node = mc.ls(sl=True)[0]
    orig = mc.group(em=True, name=node + '_orig')
    constraint = mc.parentConstraint(node, orig, mo=False)
    mc.delete(constraint)
    mc.parent(node, orig)
    return orig