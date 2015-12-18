'''
Module permettant d'installer des pre/post callbacks lors des save wip / pub /.. depuis le scene manager de Maya

Possible defintions ::

    def pre_save(**kwargs):
        pass

    def post_save(**kwargs):
        pass

    def pre_save_wip(**kwargs):
        pass

    def post_save_wip(**kwargs):
        pass

    def pre_save_to_check(**kwargs):
        pass

    def post_save_to_check(**kwargs):
        pass

    def pre_save_publish(**kwargs):
        pass

    def post_save_publish(**kwargs):
        pass
'''
import pprint

def pre_save(**kwargs):
    pprint.pprint(kwargs)

def post_save(**kwargs):
    pprint.pprint(kwargs)

def pre_save_wip(**kwargs):
    pprint.pprint(kwargs)

def post_save_wip(**kwargs):
    pprint.pprint(kwargs)

def pre_save_to_check(**kwargs):
    pprint.pprint(kwargs)

def post_save_to_check(**kwargs):
    pprint.pprint(kwargs)

def pre_save_publish(**kwargs):
    pprint.pprint(kwargs)

def post_save_publish(**kwargs):
    pprint.pprint(kwargs)