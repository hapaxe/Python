__author__ = 'f.scaduto'


def create_empty_grp_and_parent(group_list, props_name, destination_grp):
    '''
    Create empty group and parent
    :param group_list:
    :param props_name:
    :param destination_grp:
    :return:
    '''
    for grp in group_list:
        # Create an empty grp
        empty_grp = cmds.group(name=props_name+grp, empty=True)
        # Parent group
        cmds.parent(empty_grp, destination_grp)

def create_hierarchy_empty_grp(props_name):
    '''
    Create hierarchy with empty groups
    :param props_name:
    :return:
    '''
    # Set varables for grp in references
    rig_grp = "*:rigGrp"
    geo_grp = "*:GEO"
    # Set lists
    rig_grp_list = ['_Ctrl_Grp', '_Rig_Grp']
    geo_grp_list = ['_Geo_Grp']

    create_empty_grp_and_parent(group_list=rig_grp_list, props_name=props_name, destination_grp=rig_grp)
    create_empty_grp_and_parent(group_list=geo_grp_list, props_name=props_name, destination_grp=geo_grp)

def run_script():
    '''
    run script, open a prompt dialogue to add a name
    :return:
    '''
    pD_state = cmds.promptDialog(title="Enter name",cancelButton="Cancel",defaultButton="OK",button=["OK", "Cancel"],message="Enter Name:",dismissString="Cancel")
    pD_name = cmds.promptDialog(query=1,text=1)

    if pD_state == 'Cancel':
        print '\nScript canceled'
        return
    else:
        create_hierarchy_empty_grp(props_name = pD_name)
