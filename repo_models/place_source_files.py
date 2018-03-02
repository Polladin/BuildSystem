import os
import pathlib

from build_system.repo_models.replace_variables import Replacement


class PlaceSourceFiles:

    def __init__(self, header_template, cpp_template, main_cpp_template):

        # Read template files
        self.header_template = open(header_template).readlines()
        self.cpp_template = open(cpp_template).readlines()

        # Read main file's template
        self.main_cpp_template = open(main_cpp_template).readlines()

    def place_for_lib(self, folder_with_sources, lib_name, variables=None, need_to_clear=False):

        # Make a folder if not exist
        if not os.path.isdir(folder_with_sources):
            pathlib.Path(folder_with_sources).mkdir(parents=True, exist_ok=True)

        # Place header files
        Replacement.place_file(template_lines=self.header_template,
                               variables=variables,
                               file_path=folder_with_sources + '/' + lib_name + '.h')

        # Place cpp files
        Replacement.place_file(template_lines=self.cpp_template,
                               variables=variables,
                               file_path=folder_with_sources + '/' + lib_name + '.cpp')

    def place_for_exe(self, folder_with_sources, exe_name, variables=None, need_to_clear=False):

        # Make a folder if not exist
        if not os.path.isdir(folder_with_sources):
            pathlib.Path(folder_with_sources).mkdir(parents=True, exist_ok=True)

        # Place cpp files
        Replacement.place_file(template_lines=self.main_cpp_template,
                               variables=variables,
                               file_path=folder_with_sources + '/' + exe_name + '.cpp')


# source_file_factory = PlaceSourceFiles(header_template='header_libs_template.h',
#                                        cpp_template='main_libs_template.cpp')
#
# source_file_factory.place_for_lib(folder_with_sources='D:/Projects/DINS/build_system/tas-group/api/src',
#                                   lib_name='api',
#                                   variables={'INCLUDES': '',
#                                              'CODE_HEADER': 'int api(int a);',
#                                              'CODE_CPP': '#include "api.h";\n\n int api(int a) { return a * 2; }'})
#
# source_file_factory.place_for_exe(folder_with_sources='D:/Projects/DINS/build_system/tas-group/TAS/src',
#                                   exe_name='tas',
#                                   variables={'INCLUDES': '#include "api.h";\n#include<iostream>',
#                                              'CODE_CPP': 'std::cout << api(10) << std::endl;'})

