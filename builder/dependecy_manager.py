
import copy


class DependencyManager:

    DEPENDENCY_FILENAME = 'dependency.txt'

    def __init__(self, root_folder, module_names):

        self.root_folder = root_folder
        self.module_names = module_names

        #
        self.dependencies = self.read_dependencies()
        self.invert_dependencies = self._invert_dependency(self.dependencies)

    def read_dependencies(self):

        # Initialize result map
        modules_dependencies = {}

        # For each module read dependency file
        for _module in self.module_names:

            # Read from file to list [module_1, ...]
            modules_dependencies[_module] = [_module.strip()
                                             for _module in open(self.root_folder + '/' + _module + '/' +
                                                                 self.DEPENDENCY_FILENAME).readline().split(',')]

            # If a file was empty clear dependency for this module
            if modules_dependencies[_module][0] == '':
                modules_dependencies[_module] = []

        return modules_dependencies

    def sort(self):

        # Initialize result
        sorted_modules = []

        work_modules_dependencies = copy.deepcopy(self.dependencies)

        # Get modules with no dependencies
        no_dep_modules = [_module for _module in work_modules_dependencies
                          if work_modules_dependencies[_module] == []]

        for _module in no_dep_modules:
            del work_modules_dependencies[_module]

        while len(no_dep_modules) > 0:

            # Get module from no_dep_modules
            curr_module = no_dep_modules[0]
            del no_dep_modules[0]

            # Add to result
            sorted_modules.append(curr_module)

            # Remove current node from other modules
            for _next_module in self.invert_dependencies[curr_module]:
                work_modules_dependencies[_next_module].remove(curr_module)

            # Get new modules with no dependencies in work_modules_dependencies
            new_no_dep_modules = [_module for _module in work_modules_dependencies
                                  if work_modules_dependencies[_module] == []]

            for _module in new_no_dep_modules:
                del work_modules_dependencies[_module]
                no_dep_modules.append(_module)

        if len(work_modules_dependencies) > 0:
            raise RuntimeError('Cycle in module dependencies. ' + str(work_modules_dependencies))

        return sorted_modules

    def del_module_tree(self, module_name, list_of_modules):

        # Initialize queue
        module_to_del_queue = [module_name]

        while len(module_to_del_queue) > 0:

            # Add to queue new modules dependent by this module
            module_to_del_queue.extend(self.invert_dependencies[module_to_del_queue[0]])

            # Delete from list of modules
            if module_to_del_queue[0] in list_of_modules:
                list_of_modules.remove(module_to_del_queue[0])

            # Delete from queue
            del module_to_del_queue[0]

    @staticmethod
    def _invert_dependency(modules_dependencies):
        # Create list with modules in format:
        #  M1 ->  M2
        #     \-> M3
        # input_dep['M2'] = ['M1']; input_dep['M3'] = ['M1']

        input_dep = {}

        #
        for _module in modules_dependencies:
            input_dep[_module] = []

        #
        for _module, _module_deps in modules_dependencies.items():

            for _module_in_deps in _module_deps:
                input_dep[_module_in_deps].append(_module)

        return input_dep


# # Get modules
# g_modules = [_module.strip() for _module in open('storage/modules.txt').readline().split(',')]
#
# dep_manager = DependencyManager('D:/Projects/DINS/HG_server/tas_group', g_modules)
# sorted_modules = dep_manager.sort()
#
# print(sorted_modules)
#
# dep_manager.del_module_tree('common_lib', sorted_modules)
# print(sorted_modules)

