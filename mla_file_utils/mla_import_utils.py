

def import_if_available(modulename):
    """
    Import the module if it is available.
    :param modulename: name of the module to import.
    :type modulename: str

    :return: module
    """

    my_module = None

    if modulename:
        try:
            my_module = __import__(modulename)
        except ImportError:
            my_module = None
        finally:
            return my_module
    else:
        return None


def import_from_application():
    mc = import_if_available('maya.cmds')
    mxs = import_if_available('pymxs')

    if mc:
        application = 'Maya'
        import maya.api.OpenMaya as om2
        return application, mc, om2
    elif mxs:
        application = 'Max'
        import MaxPlus
        return application, mxs, MaxPlus
    else:
        return None, None, None, None


def get_dockable_widget(application):
    if application == 'Maya':
        from maya.app.general.mayaMixin import \
            MayaQWidgetDockableMixin as dockable
    elif application == 'Max':
        from mla_UI_utils.mla_Max_UI_utils import MaxDockableWidget as dockable
    else:
        print 'No dockable found'
        return

    return dockable
