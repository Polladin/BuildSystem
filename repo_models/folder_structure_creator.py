
import json
import os
import shutil
import pathlib

from build_system.repo_models.files_factory import FilesFactory


class FolderStructureCreator:

    def __init__(self, root_folder, file_with_folder_structure):

        # Read file with structure
        self.structure = json.load(open(file_with_folder_structure))

        #
        self.root_folder = root_folder

    def clear_folder(self):
        if os.path.isdir(self.root_folder):
            shutil.rmtree(self.root_folder)

    def place_structure(self):
        self.parse_structure(self.root_folder, self.structure)

    @staticmethod
    def parse_structure(path_to_current_folder, _sub_tree):

        if not isinstance(_sub_tree, type({})):
            raise RuntimeError('Wrong type for subtree')

        # For each folder in tree
        for _folder_name, _sub_tree in _sub_tree.items():

            # Folder path
            new_folder_path = path_to_current_folder + '/' + _folder_name

            # Create new folder
            pathlib.Path(new_folder_path).mkdir(parents=True, exist_ok=True)

            # Is a leaf folder or parent folder (has folder(s) inside)
            is_parent_folder = isinstance(_sub_tree, type({}))

            # Create structure for child folder
            if is_parent_folder:

                # Place files for parent folder


                #
                FolderStructureCreator.parse_structure(new_folder_path, _sub_tree)

            else:

                # Place files for leaf folder


folder_manager = FolderStructureCreator('D:/Projects/DINS/build_system/tas-group2', 'config/folder_structure.json')
folder_manager.place_structure()

