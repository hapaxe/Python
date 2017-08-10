

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


def import_from_application():
    mc = import_if_available(package='maya.cmds', module='cmds')
    mxs = import_if_available(package='pymxs')

    if mc:
        application = 'Maya'
        import maya.api.OpenMaya as om2
        return application, mc, om2
    elif mxs:
        application = 'Max'
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
