
import json
import tempfile
import os

from build_system.builder.hg_client import HGClient
from build_system.builder.connect_db_postgress import ConnectionDBPostgres
from build_system.builder.nexus_manager import NexusManager


class PublishManager:

    def __init__(self, root_folder):

        self.root_folder = root_folder
        self.db_conn = ConnectionDBPostgres(host='localhost', db_name='DB_1', user='postgres', password='123')
        self.nexus = NexusManager()

    def publish(self, changed_modules, loaded_modules):

        # Allocate next nexus version for changed modules
        modules_info = self.new_modules_version(changed_modules)

        # Put changed modules into nexus
        self.publish_build(modules_info, 'win64')
        self.publish_build(modules_info, 'lnx64')

        # Create info for all (compiled and loaded modules)
        all_modules_info = {**modules_info, **loaded_modules}

        # Create group repo info
        group_repo_info = self.new_group_repo_version()

        # Put all modules info into nexus
        self.publish_group(group_repo_info, all_modules_info)

        # Put into DB place info for all modules and group repo
        self.update_db(all_modules_info, group_repo_info)

    def new_modules_version(self, changed_modules):
        """
        :param changed_modules: list with folders for changed modules
        :param loaded_modules: pre compiled modules in format :
                                [[module_name, hash_commit, branch_name, nexus_place], ...]
        :return: returns modules info in format:
                            {
                                'module_name' : {
                                            'hash_commit' : ...,
                                            'branch_name': ...,
                                            'nexus_place': ...
                                        },
                                ...
                            }
        """

        modules_info = {}

        # Fill for changed modules
        for _module in changed_modules:
            changed_branch_name = HGClient().get_current_branch(self.root_folder + '/' + _module)
            changed_nexus_place = self.db_conn.allocate_nexus_place(module_name=_module,
                                                                    branch_name=changed_branch_name)
            modules_info[_module] = {'hash_commit': HGClient().get_current_commit(self.root_folder + '/' + _module),
                                     'branch_name': changed_branch_name,
                                     'nexus_place': changed_nexus_place}
        return modules_info

    def new_group_repo_version(self):

        # Fill for a group repo
        group_repo_branch_name = HGClient().get_current_branch(self.root_folder)
        group_repo_nexus_place = self.db_conn.allocate_nexus_place(module_name='group_repo',
                                                                   branch_name=group_repo_branch_name)

        group_repo_info = {'hash_commit': HGClient().get_current_commit(self.root_folder),
                           'branch_name': group_repo_branch_name,
                           'nexus_place': group_repo_nexus_place}

        return group_repo_info

    def publish_build(self, modules_json, platform):

        # Publish modules into nexus
        for _module, _module_info in modules_json.items():
            self.nexus.upload_module(path_to_file=self.root_folder + '/' + _module + '/CMakeLists.txt',
                                     modula_name=_module,
                                     module_info=_module_info,
                                     subfolder=platform)

    def publish_group(self, group_repo_info, all_modules_info):

        build_version = open('storage/build_ver.json', 'w')
        json.dump(all_modules_info, build_version, indent=2)
        build_version.close()

        # Publish json with modules into group repo
        self.nexus.upload_module(path_to_file=build_version.name, #'storage/build_ver.json',
                                 modula_name='group_repo',
                                 module_info=group_repo_info,
                                 subfolder='')

    def update_db(self, modules_json, group_repo_info):

        # Insert into group repo
        self.db_conn.add_group_build(group_repo_info)

        # Insert modules
        for _module, _module_info in modules_json.items():
            self.db_conn.add_module_build(_module, _module_info, group_repo_info['hash_commit'])


# builder = PublishManager('D:/Projects/DINS/HG_server/tas_group')
#
# # Get changed modules
# g_changed_modules = [_module.strip() for _module in open('storage/modules.txt').readline().split(',')]
#
# builder.publish(g_changed_modules, {})

