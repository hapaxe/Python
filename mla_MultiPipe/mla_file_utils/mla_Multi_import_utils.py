

def import_if_available(package, module=None):
    """
    Import the module if it is available.
    :param modulename: name of the module to import.
    :type modulename: str

    :return: module
    """

    my_module = None

    if package:
        try:
            my_module = __import__(package, globals(), locals(), [module], 0)
        except ImportError:
            my_module = None
        finally:
            return my_module
    else:
        return None


def get_application():
    mc = import_if_available(package='maya.cmds', module='cmds')
    mxs = import_if_available(package='pymxs')

    if mc:
        return 'Maya'
    elif mxs:
        return 'Max'
    else:
        return None


def import_from_application():
    application = get_application()

    if application == 'Maya':
        import maya.cmds as mc
        import maya.api.OpenMaya as om2
        return application, mc, om2
    elif application == 'Max':
        import pymxs as mxs
        import MaxPlus
        return application, mxs, MaxPlus
    else:
        return None, None, None


def get_dockable_widget(application):
    if application == 'Maya':
        from maya.app.general.mayaMixin import MayaQWidgetDockableMixin as dockable
    elif application == 'Max':
        from mla_MaxPipe.mla_UI_utils.mla_Max_UI_utils import MaxDockableWidget as dockable
    else:
        print 'No dockable found'
        return

    return dockable
