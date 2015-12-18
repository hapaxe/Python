__author__ = 'e.francois'



import maya.cmds as cmds

''''
def_to_check()
#   IN : rien ou list d'elements a travailler (shapes, meshes) ou str d'element a travailler (shape, mesh)
#   OUT : liste ou str de mesh(es) unique
def_list_transform_mesh()
#   IN : rien ou list ou str de shape(s) dont on veux le transform
#   OUT : liste de meshes
def_compare_shape_name()
#   IN : str d'un mesh
#   OUT : booleen (True si sa shape a le bon nom)
def_unique_name(,)
#   IN : str du mesh ou shape Ã  verifier, str ('unique' / 'existe')
#   OUT : booleen (True si l'objet est unique ou s'il existe)
def_is_shape()
#   IN : str d'un Ã©lÃ©ments a verifier
#   OUT : booleen (True si c'est uns shape)
def_not_unique()
#   IN : rien
#   OUT : list de tous les meshes qui n'ont pas un nom unique
def_rename_mesh()
#   IN : str (element a travailler), liste des geotag a retirer, str du nouveau geotag
#   OUT : renome, enleve les mauvais geotag et rajoute le bon en suffix
'''

def def_to_check(var_items=[]):
    l_meshes=[]
    l_shapes=[]
    if not var_items :
        l_shapes = cmds.ls(type='mesh')
    elif isinstance(var_items, str):
        var_items = [var_items]
    for each in var_items :
        each=each.split('|')[-1]
        if def_unique_name(each,'unique') :
            if cmds.nodeType(each) == 'mesh':
                l_shapes.append(each)
            elif cmds.nodeType(each) == 'transform' :
                l_each_shape = cmds.listRelatives(each, shapes=True, noIntermediate=True)
                if l_each_shape :
                    if cmds.nodeType(l_each_shape) == 'mesh':
                        l_meshes.append(each)
    for each in l_shapes :
        s_mesh = cmds.listRelatives(each, parent = True)[0]
        if def_unique_name(s_mesh,'unique') :
            if not s_mesh in l_meshes :
                l_meshes.append(s_mesh)
    return l_meshes

def def_list_transform_mesh(var_shape=[]):
    l_transform = []
    if not var_shape :
        var_shape = cmds.ls(type='mesh')
    if isinstance(var_shape, str):
        l_transform = cmds.listRelatives(var_shape, parent = True)
    else :
        for shape in var_shape :
            s_transform = cmds.listRelatives(shape, parent = True)[0]
            if not s_transform in l_transform :
                l_transform.append(s_transform)
    return l_transform

def def_compare_shape_name(s_mesh):
    s_wished_name = s_mesh+'Shape'
    s_principal_shape = cmds.listRelatives(s_mesh, shapes=True, noIntermediate=True)[0]
    if s_principal_shape == s_wished_name :
        return True
    else:
        return False

def def_unique_name(s_name_to_check,s_to_do) :
    if s_to_do == 'unique' :
        b_is_unique = len(cmds.ls(s_name_to_check))==1
        if b_is_unique :
            return True
        else :
            return False
    elif s_to_do == 'exist' :
        b_exist = cmds.objExists(s_name_to_check)
        if b_exist :
            return True
        else :
            return False

def def_is_shape(s_to_check) :
    s_type = cmds.nodeType(s_to_check)
    if s_type == 'mesh' :
        return True
    else :
        return False

def def_not_unique():
    l_all_meshes = def_list_transform_mesh()
    l_unique_meshes = def_to_check()
    l_not_unique_meshes = [mesh for mesh in l_all_meshes if mesh not in l_unique_meshes]
    return l_not_unique_meshes

def def_make_it_good(s_mesh):
    s_principal_shape = cmds.listRelatives(s_mesh, shapes=True, noIntermediate=True)[0]
    l_inter_shapes = cmds.listRelatives(s_mesh, shapes=True)
    l_inter_shapes.remove(s_principal_shape)
    s_dream_name = s_mesh + 'Shape'
    if not s_dream_name == s_principal_shape :
        if s_dream_name in l_inter_shapes :
            cmds.rename(s_dream_name,s_dream_name+'#')
        s_principal_shape=cmds.rename(s_principal_shape,s_dream_name)
        if s_principal_shape != s_dream_name :
            cmds.warning('il y a un probleme avec '+s_mesh+'.\n# '+s_principal_shape+'n\'a pas pu etre bien renomee')

def def_rename_mesh(s_to_Check, l_geotag, s_new_geotag) :
    s_geotag=''
    for tag in l_geotag:
        if tag in s_transform :
            s_geotag = tag
    if s_geotag :
        s_name = s_transform.replace(s_geotag,'')
    else :
        s_name = s_transform
    if '__' in s_name :
        s_name = s_name.replace('__','_')
    while s_name[-1] == '_' :
        s_name = s_name[:-1]
    l_splited_name = s_name.split('_')
    for each in l_splited_name :
        i = l_splited_name.index(each)
        if i > 0 :
            l_splited_name[i] = each[0].upper()+each[1:]
    s_name = ''.join(l_splited_name) + s_new_geotag
    if def_unique_name(s_name,'exist') :
        print s_transform, ':', s_name, 'already exist'
    else :
        cmds.rename(s_transform,s_name)

#--------------------------- var --------------------------------

l_geotag = ['MSH', 'geo', 'GEO', 'Geo']
s_new_geotag = '_geo'
l_to_Check = def_to_check(cmds.ls(sl = True, sn= True))

#--------------------------action----------------------------------
'''
print '\n\nne seront pas traite car nom non unique :\n'+'\n'.join(def_not_unique())+'\n\n'

for s_to_Check in l_to_Check :
    def_make_it_good(s_to_Check)
    def_rename_mesh(s_to_Check, l_geotag, s_new_geotag)

'''