import sys
import os

import maya.cmds as mc

sys.path.append("P:/Stella_Serie/scripts/anima_to_cube")

global asset_name


"""result = mc.promptDialog(
        title='name of the json',
        message='Type the name you want to give to you json',    
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

if result == 'OK':
    input_name = mc.promptDialog(query=True, text=True)

else :
    Anulation = mc.confirmDialog(
    title='Confirm', 
    message='You have to type a name', 
    button=['Yes'], 
    defaultButton='Yes')
"""
# read .json
asset_dicts = load_from_json(ROOT_PATH + '/scans/scan.json')
# Dictionnaire des transforms
transform_dicts = {}


#def debug vars
i = 0
g = 0
n = 0
o = 0
p = 0


# every node in scene
for node in mc.ls( type='transform', l=True):

    node_short_name = node.split('|')[-1]
    print node_short_name
    node_parent = node.split('|')
    del node_parent[-1]
    node_parent = ('|').join(node_parent)
    print node_parent



    # if assembly-------------------------------------------------------------
    if mc.objExists(node + ".definition") == True :
        o += 1
        try :
            # get transform
            node_translation = mc.xform(node, q=True, t=True)
            node_rotation = mc.xform(node, q = True, ro=True)
            node_scale = mc.xform(node, q=True, r=True, scale=True)

            # get definition path
            definition_path = mc.getAttr(node + '.definition')

            # edit path
            definition_path = definition_path.replace("$ANIMA_PROJECT_ROOT", "I:/Stella_Serie/livraisons/IN/20141021")
            definition_path = definition_path.replace("/", "\\")
            
            asset_name = 'void'

        except :
            print('Can\'t get path due to multiple objects matching name')

        # check if file exists-------------------------------------------------------------
        if os.path.isfile(definition_path) :
            
            definition_path = definition_path.split('\\')
            del definition_path[-1]
            del definition_path[-1]
            del definition_path[-1]
            definition_path = ('\\').join(definition_path)
                
            # every Asset of asset_dicts-------------------------------------------------------------
            for asset_dict in asset_dicts.values():



                # if geometry key contains given path-------------------------------------------------------------
                if definition_path in asset_dict['Geometry']:


                    # Asset Name
                    asset_name = asset_dict['Name']
                    # return geo path
                    geo_path = asset_dict['Geometry']

                    # name of the new group
                    groupe_name = node_short_name + '_group'
                    
                    
                    # get matrix
                    try :
                        matrix = mc.getAttr(node + '.matrix')
                    except :
                        print('Can\'t get matrix')

                    # if location specific-------------------------------------------------------------
                    """is_location_specific = ('locationSpecific' in geo_path)
                    if is_location_specific:"""

                    # delete
                    #mc.delete(node)
                    try :
                        mc.setAttr(node + '.visibility', 0)
                    except :
                        print 'can\'t hide ' + node

                        # Import
                    try :
                        imported_item = mc.file(geo_path, i=True, gr=True, gn=groupe_name)
                        mc.parent( groupe_name, node_parent )
                        i += 1
                    except :
                        print(node + ' HAS NOT been imported')
                        n += 1

                    try :
                        # Replace
                        mc.xform(groupe_name, t=node_translation)
                        mc.xform(groupe_name, ro=node_rotation)
                        mc.xform(groupe_name, s=node_scale)
                    except :
                        print 'can\'t replace asset'
                        p += 1

                    # New dict 
                    """new_dict = {'Name':asset_name, 'Matrix':matrix, 'Group Name':groupe_name, 'Imported':is_location_specific}
                    # Add to transform_dict
                    transform_dicts[asset_name] = new_dict"""
                                                            
            if asset_name == 'void' :
                print node + 'DOES NOT have a geometry'

i = str(i)
g = str(g)
n = str(n)
o = str(o)
p = str(p)
print i + ' elements have been imported'
print g + ' elements do NOT have geometry'
print n + ' elements have NOT been imported'
print o + ' assembly are presents in the selection'
print p + ' have NOT been replaced'
 
# Nouveau json
#save_to_json(transform_dicts, ROOT_PATH + '/scans/locations/' + input_name + '.json')