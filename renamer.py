__author__ = 'm.lanton'
import maya.cmds as mc


class renamer():
    
    def __init__(self):
    
        self.current_index = -1
        self.matches = []
        self.search_string = ""

        window_name = "Renamer"

        if mc.window(window_name, q=True, exists=True):
            mc.deleteUI(window_name)

        my_window = mc.window(title="Renamer")
        main_layout = mc.columnLayout(adj=True)


        self.find_box = mc.textFieldButtonGrp( label='Search', adj=2,text='', buttonLabel='Select', bc = self.find ,cw=[1,60])
        self.replace_box = mc.textFieldButtonGrp( label='Replace', adj=2, text='', buttonLabel='Replace', bc=self.replace , cw=[1,60])
        self.prefix_box = mc.textFieldButtonGrp( label='Prefix', adj=2, text='', buttonLabel='Add', bc=self.add_prefix , cw=[1,60])
        self.suffix_box = mc.textFieldButtonGrp( label='Suffix', adj=2,text='', buttonLabel='Add', bc=self.add_suffix , cw=[1,60])

        mc.showWindow(my_window)


    def reset(self,e):
        mc.setAttr('.rotate', 0, 0, 0, type="double3")
        mc.setAttr('.translate', 0, 0, 0, type="double3")
        mc.setAttr('.scale', 1, 1, 1, type="double3")



    def _get_matches(self):
        find_string = mc.textFieldButtonGrp(self.find_box, q=True, text=True)
        matches = mc.ls("*" + find_string  + "*", type="transform")

        return matches

    def replace(self):
        find_string = mc.textFieldButtonGrp(self.find_box, q=True, text=True)
        replace_string = mc.textFieldButtonGrp(self.replace_box, q=True, text=True)
        matches = mc.ls(sl=True)

        for match in matches:

            new_name = match.split("|")[-1].replace(find_string, replace_string)
            print "renamed", match, ">", new_name
            mc.rename(match, new_name)

    def add_prefix(self):
        prefix = mc.textFieldButtonGrp(self.prefix_box, q=True, text=True)
        matches = mc.ls(sl=True)

        for match in matches:
            new_name = prefix +  match.split("|")[-1]
            print "renamed", match, ">", new_name
            mc.rename(match, new_name)

    def add_suffix(self):
        suffix = mc.textFieldButtonGrp(self.suffix_box, q=True, text=True)
        matches = mc.ls(sl=True)

        for match in matches:
            new_name = match.split("|")[-1] + suffix
            print "renamed", match, ">", new_name
            mc.rename(match, new_name)

    def find(self):
        matches = self._get_matches()
        mc.select(matches, r=True)