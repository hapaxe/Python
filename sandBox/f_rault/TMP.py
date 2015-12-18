# --- Simple Renamer
import maya.cmds as mc

prefix = ''
suffix = '_jnt'

search = ''
replace = ''


cSelection = mc.ls(sl= True )

for item in cSelection:
    # - Get base name
    if '|' in item:
        name = item.split('|')[-1]
    else:
        name = item

    # - Search and Replace
    if search:
        name = name.replace( search, replace )
    # - Prefix
    if prefix:
        name = prefix + name
    # - Suffix
    if suffix:
        name = name + suffix

    # - Cancel if new name already exist in scene
    if mc.objExists( name ):
        print name +' already exist. '+ item +" wasn't rename"
        continue

    # - Rename
    mc.rename( item, name )
