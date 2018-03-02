
from build_system.repo_models.replace_variables import Replacement


class PlaceCmakeFiles:

    def __init__(self, lib_template, exe_template):

        # Read template files
        self.lib_template = open(lib_template).readlines()
        self.exe_template = open(exe_template).readlines()

    def place_for_lib(self, folder_to, variables=None):
        self.place_for(self.lib_template, folder_to, variables)

    def place_for_exe(self, folder_to, variables=None):
        self.place_for(self.exe_template, folder_to, variables)

    @staticmethod
    def place_for(template, folder_to, variables=None):

        # Initialize body for a CMake file
        cmake_body = ''

        # Write template to body and replace variables
        for _line in template:

            # Replace variables in a line
            new_line = Replacement.replace_variables_in_line(_line, variables)

            # Add line to body
            cmake_body += new_line

        # Save CMake file
        cmake_file = open(folder_to + '/CMakeLists.txt', 'w')
        cmake_file.write(cmake_body)
        cmake_file.close()


# cmake_factory = PlaceCmakeFiles(lib_template='CMakeLists_libs_template.cmake',
#                                 exe_template='CMakeLists_exe_template.cmake')
#
# cmake_factory.place_for_lib('D:/Projects/DINS/build_system/tas-group/api')