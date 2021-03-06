import maya.cmds as mc


def rename(obj_list=[], side='', main_name='', digits='##', suffix=''):
    """

    :param obj_list:
    :type obj_list: list

    :param side:
    :type side: str

    :param main_name:
    :type main_name: str

    :param digits:
    :type digits: str

    :param suffix:
    :type suffix: str

    :return:
    """
    inc_nbr = 0

    obj_new_names = list()

    for obj in obj_list:
        inc_nbr += 1
        increm = create_increment(inc_nbr, len(digits))

        name = '%s_%s_%s_%s' % (side, main_name, increm, suffix)
        while mc.objExists(name):
            inc_nbr += 1
            increm = create_increment(inc_nbr, len(digits))
            name = '%s_%s_%s_%s' % (side, main_name, increm, suffix)

        obj_new_names.append(name)

    return obj_new_names


def get_opposite_name(obj):
    """
    Get the name of the opposite object (same name, on the other side).

    :param obj: Name of the object which you want to find the opposite
    :type obj: str

    :return: name of the opposite object
    :rtype: str
    """

    if obj.startswith('l_'):
        opposite_name = obj.replace('l_', 'r_')
    elif obj.startswith('r_'):
        opposite_name = obj.replace('r_', 'l_')
    elif obj.startswith('L_'):
        opposite_name = obj.replace('L_', 'R_')
    elif obj.startswith('R_'):
        opposite_name = obj.replace('R_', 'L_')
    elif obj.startswith('left_'):
        opposite_name = obj.replace('left_', 'right_')
    elif obj.startswith('right_'):
        opposite_name = obj.replace('right_', 'left_')
    elif obj.startswith('LEFT_'):
        opposite_name = obj.replace('LEFT_', 'RIGHT_')
    elif obj.startswith('RIGHT_'):
        opposite_name = obj.replace('RIGHT_', 'LEFT_')
    elif '_l_' in obj:
        opposite_name = obj.replace('_l_', '_r_')
    elif '_r_' in obj:
        opposite_name = obj.replace('_r_', '_l_')
    elif '_L_' in obj:
        opposite_name = obj.replace('_L_', '_R_')
    elif '_R_' in obj:
        opposite_name = obj.replace('_R_', '_L_')
    elif '_left_' in obj:
        opposite_name = obj.replace('_left_', '_right_')
    elif '_right_' in obj:
        opposite_name = obj.replace('_right_', '_left_')
    elif '_LEFT_' in obj:
        opposite_name = obj.replace('_LEFT_', '_RIGHT_')
    elif '_RIGHT_' in obj:
        opposite_name = obj.replace('_RIGHT_', '_LEFT_')
    else:
        opposite_name = obj

    return opposite_name


def create_increment(number=0, digits=2):
    """
    Convert hash characters (##) into a number of digits :
    ex: create_increment(number=24, digits=4) = '0024'
        create_increment(number=753, digits=4) = '0753'
        create_increment(number=2, digits=2) = '02'
    
    :param number: number to convert into digits
    :type number: int, str
    
    :param digits: str too convert to digits
    :type digits: int

    :return: incremented number
    :rtype: str
    """
    if type(number) == str:
        number = int(number)

    return format(number, '0%sd' % digits)
