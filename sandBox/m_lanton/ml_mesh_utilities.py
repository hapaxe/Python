__author__ = 'm.lanton'
import maya.cmds as mc
import sandBox.m_lanton.ml_3D_vector_utilities as vector
import math as math
reload(vector)


# ----------------------------------------------------------------------------------------------------------------------
def get_sel_vertices():
    """
    :return selected_vertices: list of the selected vertices
    """

    sel_vertices = [obj for obj in mc.ls(sl=True, fl=True) if 'vtx' in obj]

    sel_vertices_idx = [obj.split('[')[-1].split(']')[0] for obj in sel_vertices]

    return sel_vertices_idx


# ----------------------------------------------------------------------------------------------------------------------
def get_sel_mesh():
    """
    :return:
    """
    # --- If vertices are selected, create sel_mesh list from selected vertices
    if mc.polyEvaluate(vertexComponent=True)>0:
        sel_vtx = mc.ls(sl=True, fl=True)
        sel_mesh = list()
        for obj in sel_vtx:
            if obj.split('.')[0] not in sel_mesh:
                sel_mesh.append(obj.split('.')[0])
            else:
                pass
    # --- Else, get selected transforms which have a shape
    else:
        sel_mesh = [obj for obj in mc.ls(sl=True, et='transform') if len(mc.listRelatives(obj, c=True, s=True, typ='mesh'))>0]

    return sel_mesh


# ----------------------------------------------------------------------------------------------------------------------
def build_difference_table(tolerance=4):
    """
    Create a table of difference between old and new mesh.
    :return difference_table: table of difference between old and new mesh (dict)
    """

    # --- Get selected meshes
    sel_mesh = get_sel_mesh()
    print len(sel_mesh)

    # --- Create empty lists for position number
    old_vtx_pos = list()
    new_vtx_pos = list()
    moved_vtx = dict()

    # --- Check if there is exactly 2 mesh selected
    if len(sel_mesh) != 2:
        print 'You must select exactly 2 meshes.'
    else:
        # --- Get number of vertices for both mesh
        old_vtx_num = mc.polyEvaluate(sel_mesh[0], vertex=True)
        new_vtx_num = mc.polyEvaluate(sel_mesh[1], vertex=True)
        old_edge_num = mc.polyEvaluate(sel_mesh[0], edge=True)
        new_edge_num = mc.polyEvaluate(sel_mesh[1], edge=True)
        old_face_num = mc.polyEvaluate(sel_mesh[0], face=True)
        new_face_num = mc.polyEvaluate(sel_mesh[1], face=True)

        # --- Check if both mesh have the same number of vertices
        if old_vtx_num != new_vtx_num or old_edge_num != new_edge_num or old_face_num != new_face_num:
            print 'old and new must have the same topology.'
        else:
            # --- Build mesh tables
            old_vtx_pos = build_mesh_table(sel_mesh[0], tolerance)
            new_vtx_pos = build_mesh_table(sel_mesh[1], tolerance)
            for i in range(0, old_vtx_num):
                # --- If vtx pos is different beyond tolerance, add it to list
                i_vtx_vector = vector.vector_difference(old_vtx_pos[i], new_vtx_pos[i])
                i_vtx_vector = vector.vector_round(i_vtx_vector, tolerance)
                i_vtx_vector_length = vector.vector_length(i_vtx_vector)
                i_vtx_vector_length = round(i_vtx_vector_length, tolerance)
                if i_vtx_vector_length > (1.00/(math.pow(10, tolerance))):
                    moved_vtx[i] = i_vtx_vector

    difference_table = {'old_vtx_pos': old_vtx_pos, 'new_vtx_pos': new_vtx_pos, 'moved_vtx': moved_vtx}

    return difference_table


# ----------------------------------------------------------------------------------------------------------------------
def build_mesh_table(mesh, tolerance=4):
    """
    Build a table containing position of every vertex at its id.
    :param mesh: mesh to build vtx table for (string)
    :param tolerance: number of digits in float to round (int)
    :return vtx_table: table of vertices position for the given mesh (list)
    """

    vtx_num = mc.polyEvaluate(mesh, vertex=True)

    vtx_pos = list()

    for i in range(0, vtx_num):
        # --- Round old vtx and add it to list
        i_vtx_pos = mc.xform('%s.vtx[%s]' % (mesh, i), q=True, r=True, t=True)
        i_vtx_pos = vector.vector_round(i_vtx_pos, tolerance)
        vtx_pos.append(i_vtx_pos)

    return vtx_pos

# ----------------------------------------------------------------------------------------------------------------------
def bake_mesh_modif(difference_table, sel_vertices, tolerance=4):
    """
    Apply vertices modification from old/new mesh to selected meshes.
    :param difference_table: table of difference between old and new mesh (dict)
    :param vtx_table: list of vertices to update (list)
    :return:
    """

    mesh_list = get_sel_mesh()

    if mc.polyEvaluate(vertexComponent=True)>0:
        sel_vertices = get_sel_vertices()
    elif len(sel_vertices)>0:
        sel_vertices = sel_vertices
    else:
        sel_vertices = []
        for i in range(0, mc.polyEvaluate(mesh_list[0], vertex=True)):
            sel_vertices.append(i)



    for mesh in mesh_list:
        for key in difference_table['moved_vtx'].keys():
            if str(key) in sel_vertices:
                mc.xform('%s.vtx[%s]' % (mesh, key), r=True, t=difference_table['moved_vtx'][key])


# ----------------------------------------------------------------------------------------------------------------------
def select_modified_vtx(difference_table):
    """
    Select moved vertices (between old and new mesh) on current selected mesh
    :param difference_table: table of difference between old and new mesh (dict)
    """

    selection = mc.ls(sl=True, et='transform')[0]

    moved_vtx = list()

    for key in difference_table['moved_vtx'].keys():
        moved_vtx.append('%s.vtx[%s]' % (selection, key))

    mc.select(moved_vtx)