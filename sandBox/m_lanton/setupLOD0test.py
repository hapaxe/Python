__author__ = 'm.lanton'
import maya.cmds as mc
import sys
sys.path.append("P:/Stella_Serie/scripts/anima_to_cube")
sys.path.append(r"\\netapp\shared_workflow\Workflow\C_pipe\API\tube")
sys.path.append(r"\\netapp\shared_workflow\Workflow\C_pipe\API\scene_manager")
from core import *
import math as math

def zero_out(var):
    '''
    Cree un group offset zeroOut
    :param var:
    :return:
    '''
    zero_out = mc.group(em=True, name=var[:-5] + '_zeroOut')
    constraint = mc.parentConstraint(var, zero_out)
    mc.delete(constraint)
    mc.parent(var, zero_out)
    return zero_out

def create_rig_element(in_name, in_type, in_parent=None, in_radius=1, in_color=None):
    '''
    Cree des controleurs, change leurs radius, leurs couleurs, cree des groupes et les parentes
    :param in_name:
    :param in_type:
    :param in_parent:
    :param in_radius:
    :param in_color:
    :return:
    '''
    # --- Creation d'objet
    # Grp group
    if in_type == 'grp':
        element = mc.group(em=True, name=in_name)
        # Parent
        if in_parent:
            mc.parent(element, in_parent)
    # Ctrl curve
    elif in_type == 'ctrl':
        element = mc.circle(name=in_name, normal=(0, 1, 0), sections=8, radius=in_radius)[0]
        if in_color:
            mc.setAttr(element + "Shape.overrideEnabled", 1)
            mc.setAttr(element + "Shape.overrideColor", in_color)

        element_grp = mc.group(em=True, name=element[:-5] + '_zeroOut')
        mc.parent(element, element_grp)
        # Parent
        if in_parent:
            mc.parent(element_grp, in_parent)
    else:
        print 'no type corresponding found'
        return

    return element

def rig_set():
    '''
    Build un rig set
    :return:
    '''
    # Liste toutes les nurbsCurves dans le RIG group
    controls_shapes = mc.listRelatives("RIG", allDescendents=True, type="nurbsCurve")

    # Remonte le parent des shapes
    controls = mc.listRelatives(controls_shapes, parent=True)

    # Fait un set de selection
    mc.sets(controls, n="RIG_SET")

def geometry_set():
    """
    Build un Geometry Set
    :return:
    """
    # Scan les transforms qu'il y a dans l'anima_name
    geometry = mc.listRelatives("GEO", allDescendents=True, type="transform")

    content = mc.ls(geometry, dag=True, type="transform")

    # Liste vide qui contriendras les geometries
    geo_set_to_add = []
    # pour chaques transforms dans geometry
    for stuff in content:
        # Regarde si il y a une shape dans les enfants, si oui, l'ajoute a la liste
        if mc.listRelatives(stuff, children=True, shapes=True):
            geo_set_to_add.append(stuff)

    # Fait un set de selection
    mc.sets(geo_set_to_add, n="GEOMETRY_SET")

def add_cube_tag_manual(node_to_tag):
    """
    Add cube tag attributs, but without informations
    :rtype : object
    :param node_to_tag:
    :return:
    """
    # cube type
    mc.addAttr(node_to_tag, longName="cube_type", dataType="string")
    # cube name
    mc.addAttr(node_to_tag, longName="cube_name", dataType="string")
    # cube_task
    mc.addAttr(node_to_tag, longName="cube_task", dataType="string")
    # cube version
    mc.addAttr(node_to_tag, longName="cube_version", dataType="string")

def create_rig():
    '''
    Create a rig like a setupLOD0, and add attributs without informations
    :param in_asset:
    :return:
    '''

    in_asset = mc.ls(sl=True)[0]
    # --------------------
    #------ BUILD UN RIG
    # Li la boundingbox du group "anima_name"
    bbox = mc.exactWorldBoundingBox(in_asset, ignoreInvisible=True)

    # calculate ctrl size
    bbox_size = [0, 0]
    bbox_size[0] = bbox[3] - bbox[0]
    bbox_size[1] = bbox[5] - bbox[2]

    bbox_size.sort()

    walk_size = bbox_size[1] * 0.8
    master_size = bbox_size[1] * 0.95


    #calculate bbox center
    bbox_center = [0, 0, 0]
    bbox_center[0] = (bbox[0] + bbox[3]) / 2
    bbox_center[1] = (bbox[1] + bbox[4]) / 2
    bbox_center[2] = (bbox[2] + bbox[5]) / 2


    #calculate distance of bbox center to world center
    hypot = math.hypot(bbox_center[0], bbox_center[1])
    distance = math.hypot(hypot, bbox_center[2])

    # Creation du rig
    root_grp = create_rig_element(in_name=in_asset + "_RIG", in_type='grp')
    geo_grp = create_rig_element(in_name="GEO", in_type='grp', in_parent=root_grp)
    rig_grp = create_rig_element(in_name="RIG", in_type='grp', in_parent=root_grp)
    to_attach_grp = create_rig_element(in_name="TO_ATTACH", in_type='grp', in_parent=rig_grp)
    master_ctrl = create_rig_element(in_name="master_ctrl", in_type='ctrl', in_parent=to_attach_grp,
                                     in_radius=master_size, in_color=13)
    walk_ctrl = create_rig_element(in_name="walk_ctrl", in_type='ctrl', in_parent=master_ctrl, in_radius=walk_size,
                                   in_color=6)

    helper_ctrl = 'helper_ctrl'

    #if distance of bbox center to world center is more than 80% of bbox radius :
    if distance > bbox_size[1] * 0.8:
        mc.circle(name=helper_ctrl, normal=(0, 1, 0), sections=8, radius=bbox_size[1] * 0.65)[0]
        mc.xform(helper_ctrl, t=[bbox_center[0], bbox[1], bbox_center[2]])
        of = zero_out(helper_ctrl)
        mc.parent(of, walk_ctrl)

    # Set le geo group en drawing override : reference
    mc.setAttr("GEO.overrideEnabled", 1)
    mc.setAttr("GEO.overrideDisplayType", 2)

    # Parent anima_name au geo grp
    mc.parent(in_asset, geo_grp)

    # Netois l'hystorique des crontols
    mc.delete(master_ctrl, ch=True)
    mc.delete(walk_ctrl, ch=True)

    if mc.objExists(helper_ctrl):
        mc.parentConstraint(helper_ctrl, geo_grp, mo=True)
        mc.scaleConstraint(helper_ctrl, geo_grp, mo=True)

        # Netois l'hystorique du crontol
        mc.delete(helper_ctrl, ch=True)
    else:
        # Contraint le geo grp au walk ctrl
        mc.parentConstraint(walk_ctrl, geo_grp, mo=True)
        mc.scaleConstraint(walk_ctrl, geo_grp, mo=True)

    try:
        # Build a geometry set
        geometry_set()
    except:
        pass

    # Build a rig set
    rig_set()

    #--------------------
    #------ Ajoute des tags
    # nom de l'objet a tagger
    node = in_asset + "_RIG"

    # Add tags without informations
    add_cube_tag_manual(node_to_tag=node)
