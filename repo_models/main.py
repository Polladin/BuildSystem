import pathlib
import shutil
import os
import json

from build_system.repo_models.place_cmake_files import PlaceCmakeFiles
from build_system.repo_models.place_source_files import PlaceSourceFiles


ROOT_FOLDER = 'D:/Projects/DINS/build_system/tas-group'
EXE_FOLDERS = ['TAS', 'FAX']


class FolderCreator:

    def __init__(self, root_folder):

        #
        self.root_folder = root_folder

        #
        self.dependency = json.load(open('config/dependency.json'))

        #
        self.folders_list = self.load_folder_structure('config/folders_list.txt')

        #
        self.cmake_factory = PlaceCmakeFiles(lib_template='templates/CMakeLists_libs_template.cmake',
                                             exe_template='templates/CMakeLists_exe_template.cmake')

        #
        self.source_file_factory = PlaceSourceFiles(header_template='templates/header_libs_template.h',
                                                    cpp_template='templates/main_libs_template.cpp',
                                                    main_cpp_template='templates/main_exe_template.cpp')

    @staticmethod
    def load_folder_structure(path_to_config):

        # Read file
        file_with_folders_name = open(path_to_config)

        # Insert folders to list
        folders_list = [_line.strip() for _line in file_with_folders_name.readlines()]

        return folders_list

    def clear_folder(self):
        if os.path.isdir(self.root_folder):
            shutil.rmtree(self.root_folder)

    def create_folders(self):

        include_subdirectory = ''
        target_include_dirs = ''
        linked_libs = ''

        include_main_cpp = ''
        cout_main_cpp = ''

        num = 1

        # Create folder (libs only)
        for _folder_name in [_folder_name.split(':')[0].strip() for _folder_name in self.folders_list]:

            if _folder_name[0] == '#':
                print('Did not processed : ', _folder_name)
                continue

            # Full path
            full_path = self.root_folder + '/' + _folder_name

            # Create folder
            pathlib.Path(full_path).mkdir(parents=True, exist_ok=True)

            # Add dependency file
            dep_file = open(full_path + '/dependency.txt', 'w')
            dep_file.write(self.dependency[_folder_name.lower()])
            dep_file.close()

            # Add CMake file
            self.cmake_factory.place_for_lib(full_path, {'PROJECT_NAME': _folder_name + '_project',
                                                         'LIB_NAME': _folder_name,
                                                         'PROJECT_FOLDER_NAME': _folder_name,
                                                         'TARGET_LINK_LIBRARIES': 'target_link_libraries(' +
                                                                                  _folder_name + ' ' +
                                                                                  self.dependency[_folder_name.lower()].replace(',', '') + ')\n'})

            # Add Source files
            self.source_file_factory.place_for_lib(folder_with_sources=full_path + '/src',
                                                   lib_name=_folder_name,
                                                   variables={'INCLUDES': '',
                                                              'CODE_HEADER': 'int ' + _folder_name + '(int a);',
                                                              'CODE_CPP': '#include "' + _folder_name
                                                                          + '.h";\n\n int ' + _folder_name
                                                                          + '(int a) { return a + ' + str(num) + '; }'})
            num += 1

            include_subdirectory += 'add_subdirectory(${SOURCES_FOR_DEPENDENCY_PROJECTS}/' + _folder_name \
                                    + ' ${IMPORTED_LIB_BY_SOURCES}/' + _folder_name + ')\n'

            target_include_dirs += 'target_include_directories(' + 'TAS' \
                                   + ' PUBLIC ${SOURCES_FOR_DEPENDENCY_PROJECTS}/' \
                                   + _folder_name + '/src)\n'

            linked_libs += _folder_name + ' '

            include_main_cpp += '#include "' + _folder_name + '.h";\n'
            cout_main_cpp += '    std::cout << ' + _folder_name + '(10) << std::endl;\n'

        # TAS
        self.cmake_factory.place_for_exe(self.root_folder + '/TAS',
                                         {'PROJECT_NAME': 'TAS_project',
                                          'INCLUDE_SUBDIRECTORY': include_subdirectory,
                                          'TARGET': 'TAS',
                                          'TARGET_INCLUDE_DIRS': target_include_dirs,
                                          'LINKED_LIBS': linked_libs})

        self.source_file_factory.place_for_exe(folder_with_sources='D:/Projects/DINS/build_system/tas-group/TAS/src',
                                               exe_name='main',
                                               variables={'INCLUDES': '#include<iostream>\n\n' + include_main_cpp,
                                                          'CPP_CODE': cout_main_cpp + '\n    std::cin.get();\n'})

# FolderCreator(ROOT_FOLDER).clear_folder()
FolderCreator(ROOT_FOLDER).create_folders()

