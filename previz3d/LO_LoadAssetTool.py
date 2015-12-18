import maya.cmds as cmds

def LO_LoadAssetTool():
    cmds.loadPlugin('R:/rd/libs/python/asset_importer/asset_importer_maya.py')
    cmds.tube2_asset_importer()