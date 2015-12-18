import maya.cmds as mc

scriptNodes = mc.ls(type='script')
# Keep the sceneConfigurationScriptNode node
if 'sceneConfigurationScriptNode' in scriptNodes:
    scriptNodes.remove('sceneConfigurationScriptNode')
# Remove useless
if scriptNodes:
    mc.delete( scriptNodes )


hyperViewNodes = mc.ls(type=['hyperLayout', 'hyperView'])
# Keep the hyperGraphLayout and hyperGraphInfo nodes
if 'hyperGraphLayout' in hyperViewNodes:
    hyperViewNodes.remove('hyperGraphLayout')
if 'hyperGraphInfo' in hyperViewNodes:
    hyperViewNodes.remove('hyperGraphInfo')
# Remove useless
if hyperViewNodes:
    mc.delete( hyperViewNodes )
