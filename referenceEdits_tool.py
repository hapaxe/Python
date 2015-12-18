from maya import cmds
import time

def clean_referenceEdits():
    # List Edited Attributes for Entire Scene
    edited_attributes = cmds.referenceQuery(editAttrs=True, editNodes=True)
    # List All References
    reference_nodes = cmds.ls(references=True)
    # Each Reference
    for reference_node in reference_nodes:
        # Unload Reference
        cmds.file(unloadReference=reference_node)
    # Each Edited Attribute
    for edited_attribute in edited_attributes:
        # Split around .
        splitted_path = edited_attribute.split('.')
        # If its an attribute
        if len(splitted_path)==2:
            # If that attribute starts with 'mi'
            if splitted_path[1][:2] == 'mi':
                # Remove Edit
                cmds.referenceEdit(edited_attribute, removeEdits=True, editCommand='setAttr', successfulEdits=True, failedEdits=True)
    return
    # Each Reference
    for reference_node in reference_nodes:
        # Reload Reference
        cmds.file(loadReference=reference_node, prompt=False)

start_time = time.time()
clean_referenceEdits()
print("--- %s seconds ---" % time.time() - start_time)