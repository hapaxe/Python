#----------------------------------------------------------------------
# functions fileInfo
# Author : felixlechA.com | f.rault
# Date   : March 2015
# Ver    : 1.0
#----------------------------------------------------------------------
import os
import webbrowser
import maya.cmds as mc

#----------------------------------------------------------------------
def get_BasePath( add_directory = list(), add_file= '' ):
    '''
    Return the path of the base maya module

    :param add_directory: Add a list of directory after the basePath
    :type add_directory: list

    :param add_file: Add a file at the end
    :type add_file: string

    :return: compelete path
    :rtype: string
    '''
    # - Get the base path as list
    path_base= os.path.split( os.path.realpath(__file__))[0].split('\\')[:-2]

    # - Add extra directory
    if add_directory:
        path_base.extend( add_directory )

    # - Build complete path
    path= ''
    for item in path_base:
        path += item + '/'

    # - Add file at the end
    if add_file:
        path += add_file

    return path

#---------------------------------------------------------------------
def get_available_plugins():
    '''
    Get all available plugins

    :return: List of available Plugin
    :rtype: list
    '''
    # --- Get Plugin Directory
    plugins_path= os.environ['MAYA_PLUG_IN_PATH'].split(';')

    # --- Get plugin
    plugin_list= list()
    for path in plugins_path:
        if os.path.exists( path ):
            for plug_file in os.listdir( path ):
                if plug_file.endswith('.mll' ) or plug_file.endswith( '.py'):
                    plugin_list.append( plug_file.split('.')[0]  )

    return plugin_list

#----------------------------------------------------------------------
def load_plugin( plugins= list() ):
    '''
    Check if the needed plugin already load. if not loaded, load and autoload check for the plugin

    :param plugins: List of plugin name to load
    :type plugins: list
    '''
    # --- Get the available plugin
    plugins_available= get_available_plugins()

    # --- Load Plugin
    log= '\n--- load Plugins ---'
    for plugin in plugins:
        # - Check if plugin is available
        if not plugin in plugins_available:
            log += '\n ! %s is not available' %plugin
            continue

        # - Load plugin
        if not mc.pluginInfo( plugin, q=True, l=True):
            mc.loadPlugin( plugin )
            log += '\n . %s is already loaded' %plugin
        else:
            log += '\n + %s is loaded' %plugin

        # - autoLoad plugin
        if not mc.pluginInfo( plugin, query=True, autoload=True ):
            mc.pluginInfo( plugin, edit=True, autoload=True )

    print log + '\n'

#----------------------------------------------------------------------
def openWebPage( path ):
    '''
    Open a given path in webBrowser

    :param path: The path to open in webBrowser
    :type path: string
    :return: none
    '''
    webbrowser.open( path )