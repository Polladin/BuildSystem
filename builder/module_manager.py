
from build_system.builder.hg_client import HGClient
from build_system.builder.connect_db_postgress import ConnectionDBPostgres
from build_system.builder.dependecy_manager import DependencyManager

import queue


MAX_ATTEMPTS_TO_GET_PARENT_WITH_BUILT_SRC = 20


class ModuleManager:

    def __init__(self, group_folder, all_modules):

        # Root folder
        self.group_folder = group_folder

        # DB connection
        self.db_conn = ConnectionDBPostgres(host='localhost', db_name='DB_1', user='postgres', password='123')

        # Get list of all modules
        self.all_modules = all_modules

        # Dependency manager
        self.dependency_manager = DependencyManager(self.group_folder, self.all_modules)

    def get_last_compiled_group_repo(self):
        """
        This function returns a list to find .json files with built commits for group repo
        :return: result_commits in format: [[hash_of_commit, [branch_name, nexus_num]], ...]
        """

        # Get current commit
        commit = HGClient().get_current_commit(self.group_folder)

        # Check current build already in DB
        if self.db_conn.is_group_built(commit) is not None:
            raise RuntimeError('Current group commit in Nexus')

        # Get group commits with
        built_group_commits = self._find_last_in_parent_commits(commit)

        # Get compiled components
        return self._get_compiled_components(built_group_commits)

    def _get_compiled_components(self, built_group_commits):

        built_modules_info = {}

        # Get list with compiled modules for each built group commit
        for _group_commit in built_group_commits:
            built_modules_info[_group_commit] \
                = self.db_conn.get_modules_info_by_group_commit(_group_commit, self.all_modules)

        # Get current modules commits
        currents_modules_commits = HGClient().get_current_commits_for_modules(self.group_folder, self.all_modules)

        # Get group build with most same modules
        return self._get_built_modules_info(currents_modules_commits, built_modules_info)

    def _get_built_modules_info(self, currents_modules_commits, built_modules_info):

        # Initialize result
        result_built_module_info = {}

        # For each found built modules info
        for gr_hash, _built_module_info in built_modules_info.items():

            cur_modules_info = self._get_compared_modules(currents_modules_commits, _built_module_info)

            if len(cur_modules_info) > len(result_built_module_info):
                result_built_module_info = cur_modules_info

        return result_built_module_info

    def _get_compared_modules(self, currents_modules_commits, built_module_info):
        """
        :return:    cur_built_modules : number of built modules
                    cur_modules_info in format : {'module_name': {'hash_commit':.., 'branch_name':.., 'nexus_place':..},
                                                  ...}
        """

        # Modules built in current module info
        cur_modules_info = {}

        # Get topologically sorted modules
        sorted_modules = self.dependency_manager.sort()

        # While not all modules tree was checked
        while len(sorted_modules) > 0:

            # Is module was built : add build modules and del it from list of modules
            if sorted_modules[0] in currents_modules_commits \
                    and sorted_modules[0] in built_module_info \
                    and currents_modules_commits[sorted_modules[0]] == built_module_info[sorted_modules[0]][0]:

                cur_modules_info[sorted_modules[0]] = {'hash_commit': built_module_info[sorted_modules[0]][0],
                                                       'branch_name': built_module_info[sorted_modules[0]][1],
                                                       'nexus_place': built_module_info[sorted_modules[0]][2]}

                del sorted_modules[0]

            else:

                # Delete module tree from sorted modules
                self.dependency_manager.del_module_tree(sorted_modules[0], sorted_modules)

        return cur_modules_info

    def _find_last_in_parent_commits(self, current_commit):

        # Max deep to find a commit
        max_attempts = MAX_ATTEMPTS_TO_GET_PARENT_WITH_BUILT_SRC

        # Initialize result
        result_commits = {}

        # Queue for BFS
        parent_commit = queue.Queue()
        parent_commit.put(current_commit)

        # Get previous commits while one of it will be found in DB
        while max_attempts > 0 and not parent_commit.empty():

            # Get next parent commits
            p_commit = parent_commit.get()

            # Is build in nexus add it to result
            nexus_place = self.db_conn.is_group_built(p_commit)

            if nexus_place is not None:
                result_commits[p_commit] = nexus_place
            else:
                # Get parents for a current commit
                for _parent in HGClient().get_parent_commits(self.group_folder, p_commit):
                    parent_commit.put(_parent)

            # Decrease max attempts
            max_attempts -= 1

        return result_commits


# import pprint
#
# all_modules = g_changed_modules = [_module.strip() for _module in open('storage/modules.txt').readline().split(',')]
#
# module_manager = ModuleManager('D:/Projects/DINS/HG_server/tas_group', all_modules)
#
# g_nexus_place = module_manager.get_last_compiled_group_repo()
#
# # for _gr_commit in g_nexus_place:
# #     g_nexus_place[_gr_commit].append(HGClient().get_short_commit(repo_path='D:/Projects/DINS/HG_server/tas_group',
# #                                                                  commit_hash=_gr_commit))
#
# pprint.pprint(g_nexus_place)
# # print(g_nexus_place.keys())
# #
# # modules_info = module_manager.db_conn.get_modules_info_by_group_commit(list(g_nexus_place.keys())[0],
# #                                                                        module_manager.all_modules)
# # pprint.pprint(modules_info)


