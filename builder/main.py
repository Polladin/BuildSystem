
import os
import shutil

from build_system.builder.hg_client import HGClient
from build_system.builder.module_manager import ModuleManager
from build_system.builder.generate_cmake import GenerateSolutions
from build_system.builder.cmd_executor import SysCommandExecutor

GROUP_REPO = 'D:/Projects/DINS/HG_server/tas_group'


class Builder:

    def __init__(self, root_folder, group_repo_url):

        # Root folder
        self.root_folder = root_folder

        # URL for group repo
        self.group_repo_url = group_repo_url

        # Group folder name
        self.group_folder_name = GROUP_REPO.split('/')[-1].strip()

    def load(self, need_clone=True, del_build_folder=True):

        # Clone projects
        if need_clone:
            if os.path.isdir(self.root_folder + self.group_repo_url.split('/')[-1].strip()):
                shutil.rmtree(self.root_folder + self.group_repo_url.split('/')[-1].strip())

            HGClient().clone(self.root_folder, self.group_repo_url)

        # Get built modules
        all_modules = [_module.strip() for _module in open('storage/modules.txt').readline().split(',')]
        module_manager = ModuleManager(self.root_folder, all_modules)
        g_nexus_place = module_manager.get_last_compiled_group_repo()

        # Load 3d parties and built modules

        # Get changed modules
        changed_modules = list(set(all_modules).difference(g_nexus_place.keys()))

        print('Changed modules:')
        print(changed_modules)

        # Generating solution
        GenerateSolutions.run(src_folder=self.root_folder,
                              with_sources=changed_modules,
                              del_previous_build_folder=del_build_folder)

    def build(self):

        # Build
        build_cmd = ['cmake', '--build', '.', '--target', 'ALL_BUILD', '--config', 'Debug']
        output, err = SysCommandExecutor.exec(cmd=build_cmd,
                                              work_dir=self.root_folder + '/build',
                                              print_to_console=True,
                                              shell=True)

        if "Build FAILED" in output:
            print('------------------ COMPILE ERROR ----------------------')
            raise RuntimeError('Compile failed')

        if "Build succeeded" not in output:
            raise RuntimeError('Compilation is not succeed')

        # Test

        pass

    def publish(self):

        # Publish

        pass


builder = Builder('D:/Projects/DINS/HG_server/tas_group_test', 'D:/Projects/DINS/HG_server/tas_group')
builder.load(need_clone=False,
             del_build_folder=True)
builder.build()
