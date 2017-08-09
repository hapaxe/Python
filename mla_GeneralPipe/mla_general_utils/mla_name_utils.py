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

    for obj in obj_list:
        inc_nbr += 1
        increm = create_increment(inc_nbr, len(digits))

        name = '%s_%s_%s_%s' % (side, main_name, increm, suffix)
        while mc.objExists(name):
            inc_nbr += 1
            increm = create_increment(inc_nbr, len(digits))
            name = '%s_%s_%s_%s' % (side, main_name, increm, suffix)

        mc.rename(obj, name)

def create_increment(number=0, digits=2):
    """
    Convert hash characters (##) into a number of digits :
    ex: create_increment(number=24, digits=4) = '0024'
        create_increment(number=753, digits=4) = '0753'
        create_increment(number=2, digits=2) = '02'
    
    :param number: number to convert into digits
    :type number: int
    
    :param digits: str too convert to digits
    :type digits: int
    :return: 
    """
    return format(number, '0%sd' % digits)
