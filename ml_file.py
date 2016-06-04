__author__ = 'v.moriceau'

import os
import glob
import json
import stat
import shutil
import logging
from collections import OrderedDict


class FileSystem(object):
    """
    Classe pour centraliser la manipulation des fichiers.
    """

    @staticmethod
    def find_in_upper_folders(search_root, filename):
        # Conform Path
        search_root = os.path.realpath(search_root)
        # Search for
        found_filepath = glob.glob(os.path.join(search_root, filename))
        # If found
        if found_filepath:
            # Return
            return found_filepath[0]
        # Not found, go up, recurse
        return FileSystem.find_in_upper_folders(os.path.dirname(search_root), filename)

    @staticmethod
    def mkdir(dirpath):
        '''Creates Directory Tree if not exists'''
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

    @staticmethod
    def load_from_json(filename):
        """
        Charge le contenu d'un fichier json dans un objet python
        :param filename:str
        :return:object
        """
        # Parse
        filename = FileSystem.normpath(filename)
        # If Exists
        if filename:
            # Verbose
            logging.info('Load from %s' % filename)
            # Open file
            with open(filename, 'r') as file_json:
                # Load and return
                return json.load(file_json, object_pairs_hook=OrderedDict)

    @staticmethod
    def save_to_json(python_object, filename):
        """
        Dumpe dans un fichier json un objet python
        :param python_object:object
        :param filename:str
        """
        # Normpath
        filename = FileSystem.normpath(filename, False, True)
        # Verbose
        logging.info('Save to   %s' % filename)
        # Make Folder if doesn't exists
        FileSystem.mkdir(os.path.dirname(filename))
        # Open File
        with open(filename, 'w+') as file_json :
            # Scan
            json.dump(python_object, file_json, sort_keys=True, indent=4, separators=(',', ': '))

    @staticmethod
    def copy_file(path_source, path_destination):
        """
        Copie un fichier en creant l'arborescence et/ou un fichier vide si besoin
        :param path_source: str
        :param path_destination:str
        :return:-1 si fichier vide cree
        """
        # Si la source est differente de la destination
        if path_source is not path_destination:
            # Si la source existe
            if os.path.isfile(path_source):
                # Si le chemin n'existe pas
                if not os.path.exists(os.path.dirname(path_destination)):
                    # Creer
                    os.makedirs(os.path.dirname(path_destination))
                # Verbose
                logging.info('Copying %s' % os.path.normpath(path_source))
                logging.info('     -> %s' % os.path.normpath(path_destination))
                # Try
                try:
                    # Delete if destination exists
                    FileSystem.delete_if_exists(path_destination)
                    # Copy
                    shutil.copy(path_source, path_destination)
                    # Set Readonly
                    os.chmod(path_destination, stat.S_IREAD)
                    # Succes
                    return True
                # Error
                except:
                    # Verbose
                    logging.warn('Error Copying file !')
                    # Failure
                    return False
            # Si la source n'exsite pas
            else:
                # Verbose
                logging.info('Source File doesnt exists %s' % path_source)
                logging.info('Creating Empty File       %s' % path_destination)
                # Try
                try:
                    # Creer un fichier vide
                    with open(path_destination, 'w+'):pass
                    # Return
                    return True
                # Error
                except:
                    # Verbose
                    logging.warn('Error Creating file !')
                    # Failure
                    return False
        # Failure
        return False

    @staticmethod
    def delete_if_exists(filepath, silent=False):
        """
        :param filepath:
        :return:
        """
        # If file exists
        if os.path.isfile(filepath):
            # Remove Attributes
            os.chmod(filepath, stat.S_IWRITE)
            # Remove File
            os.remove(filepath)
            # Verbose
            logging.info('Removed %s' % filepath)
            # Return
            return True
        # Return
        return False

    @staticmethod
    def normpath(filepath, must_exist=True, parse_env_vars=True):
        # Norm
        filepath = os.path.normpath(filepath)
        # If parse env vars
        if parse_env_vars:
            # Parse
            filepath = os.path.expandvars(filepath)
        # Make Slashes for Maya Compatibility
        filepath = filepath.replace('\\', '/')
        # If Must Exist
        if must_exist:
            # Check Exist
            if os.path.isfile(filepath) or os.path.isdir(filepath):
                # Return
                return filepath
        # If not Must Exist
        else:
            # Return
            return filepath

    @staticmethod
    def compress_env_vars(filepath, var_names=[]):
        # Normpath
        filepath = FileSystem.normpath(filepath, must_exist=False, parse_env_vars=False)
        # Each Env var
        for env_var_name, env_var_values in os.environ.items():
            # If Name given or no name given
            if env_var_name in var_names or var_names == []:
                # Split and normalize
                splitted_values = [FileSystem.normpath(env_path, must_exist=False, parse_env_vars=False) for env_path in env_var_values.split(";")]
                # Only one value possible
                if len(splitted_values) == 1:
                    # Replace in filepath
                    filepath = filepath.replace(splitted_values[0], '$' + env_var_name)
        # Return
        return filepath