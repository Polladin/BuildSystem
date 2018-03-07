
import json
import os
import shutil
import pathlib

from build_system.builder.cmd_executor import SysCommandExecutor


class HGClient:

    def __init__(self):

        pass

    def clone_all(self, root_folder, path_to_hg, modules):

        for _module in modules:
            self.clone(root_folder, path_to_hg + '/' + _module)

    def clone(self, root_folder, path_to_hg):

        cmd = 'hg clone ' + path_to_hg

        output, err = SysCommandExecutor.exec(cmd=cmd,
                                              work_dir=root_folder,
                                              print_to_console=False)

        # Error
        if err != '':
            print('Error : ', err)
            return False

        print(output)
        return True


# HGClient().clone('D:/Projects/DINS/build_system/tas_group3', 'D:/Projects/DINS/HG_server' + '/common')

if os.path.isdir('D:/Projects/DINS/build_system/tas_group3'):
    shutil.rmtree('D:/Projects/DINS/build_system/tas_group3')

pathlib.Path('D:/Projects/DINS/build_system/tas_group3').mkdir(parents=True, exist_ok=True)

structure = json.load(open('../repo_models/config/folder_structure.json'))
modules = list(structure.keys())

HGClient().clone_all('D:/Projects/DINS/build_system/tas_group3', 'D:/Projects/DINS/HG_server', modules)

