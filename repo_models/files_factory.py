import json
import pprint

from build_system.repo_models.replace_variables import Replacement


class PlaceFile:

    def __init__(self, template, prefix=''):

        # Read template
        self.template = open(template).readlines()

        self.prefix = prefix

    def place_cmake(self, file_path, vars):
        self.place_with_name(file_path, vars, 'CMakeLists.txt')

    def place_with_name(self, file_path, vars, file_name):

        Replacement.place_file(template_lines=self.template,
                               variables=vars,
                               file_path=file_path + self.prefix + '/' + file_name)


class FilesFactory:

    @staticmethod
    def get_cmake_parent_factory():
        return PlaceFile(template='templates/CMakeLists_parent_template.cmake')

    @staticmethod
    def get_cmake_lib_factory():
        return PlaceFile(template='templates/CMakeLists_libs_template.cmake')

    @staticmethod
    def get_cmake_exe_factory():
        return PlaceFile(template='templates/CMakeLists_exe_template.cmake')

    @staticmethod
    def get_lib_header_factory():
        return PlaceFile(template='templates/header_libs_template.h',
                         prefix='/headers')

    @staticmethod
    def get_lib_main_factory():
        return PlaceFile(template='templates/main_libs_template.cpp',
                         prefix='/src')

    @staticmethod
    def get_exe_main_factory():
        return PlaceFile(template='templates/main_exe_template.cpp',
                         prefix='/src')


class FillFolder:

    TYPE_PARENT_FOLDER = 'parent'
    TYPE_LIB = 'lib'
    TYPE_EXE = 'exe'
    TYPE_LIBEXE = 'libexe'

    def __init__(self):

        # Initialize file factories
        self.cmake_parent_factory = FilesFactory.get_cmake_parent_factory()
        self.cmake_lib_factory = FilesFactory.get_cmake_lib_factory()
        self.cmake_exe_factory = FilesFactory.get_cmake_exe_factory()
        self.lib_header_factory = FilesFactory.get_lib_header_factory()
        self.lib_main_factory = FilesFactory.get_lib_main_factory()
        self.exe_main_factory = FilesFactory.get_exe_main_factory()

        # Dependencies
        self.dependency = self.load_dependencies_from_json('config/dependency.json')

    @staticmethod
    def load_dependencies_from_json(json_file):

        json_dep = json.load(open(json_file))

        dependency = {}

        # Create map with structure:
        #   {
        #       'lib_name': 'lib_1 lib_2 ...'
        #       ...
        #   }
        for _lib_name, _lib_dep in json_dep.items():
            dependency[_lib_name.lower()] = _lib_dep.lower().replace(',', '')

        return dependency

    def place_files(self, folder_path, folder_type, subfolders_list=None, root_project=None,
                    include_folders_with_source=None):

        # Parent folder
        if folder_type == FillFolder.TYPE_PARENT_FOLDER:
            self.place_for_parent_folder(folder_path, subfolders_list)

        # Lib folder
        elif folder_type == FillFolder.TYPE_LIB:
            self.place_for_lib(folder_path, root_project)

        # Exe folder
        elif folder_type == FillFolder.TYPE_EXE:
            self.place_for_exe(folder_path, include_folders_with_source)

        # LibExe folder
        elif folder_type == FillFolder.TYPE_LIBEXE:
            self.place_for_libexe(folder_path)

    def place_for_parent_folder(self, folder_path, subfolders_list):

        # Project name
        project_name = folder_path.split('/')[-1].strip()

        # Cmake subdirectories
        cmake_add_subdirectory = ''
        for _subfolder_name in subfolders_list:
            cmake_add_subdirectory += 'add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/' + _subfolder_name + ')\n'

        # Place CMake file
        self.cmake_parent_factory.place_cmake(file_path=folder_path,
                                              vars={'PROJECT_NAME': project_name + '_project',
                                                    'SUBDIRECTORIES': cmake_add_subdirectory})
        pass

    def place_for_lib(self, folder_path, root_project):

        # Project name
        project_name = folder_path.split('/')[-1].strip()

        # Lib dependency
        link_libs = 'target_link_libraries(' + project_name + ' ' + self.dependency[project_name.lower()] + ')\n'

        # Folder in VS to contain a projects
        project_folder = 'set_property(TARGET ' + project_name + ' PROPERTY FOLDER ' + root_project + ')\n'

        # Place CMake file
        self.cmake_lib_factory.place_cmake(file_path=folder_path,
                                           vars={'PROJECT_NAME': project_name + '_project',
                                                 'LIB_NAME': project_name,
                                                 'TARGET_LINK_LIBRARIES': link_libs,
                                                 'PROJECT_FOLDER_NAME': project_folder})

        # Place header file
        self.lib_header_factory.place_with_name(file_path=folder_path,
                                                file_name=project_name + '.h',
                                                vars={'INCLUDES': '#include <string>;\n\n',
                                                      'CODE_HEADER': 'std::string ' + project_name + '(int a);'})

        # Initialize cpp body
        cpp_body = '#include "' + project_name + '.h"\n\n'
        cpp_body += 'int ' + project_name + ' (int a) { return std::to_string(a) + "_' + project_name + '"; }\n'

        # Place cpp file
        self.lib_main_factory.place_with_name(file_path=folder_path,
                                              file_name=project_name + '.cpp',
                                              vars={'CODE_CPP': cpp_body})

    def place_for_exe(self, folder_path, include_folders_with_source):

        # Project name
        project_name = folder_path.split('/')[-1].strip()

        # Lib dependency
        link_libs = 'target_link_libraries(' + project_name + ' ' + self.dependency[project_name] + ')\n'

        # Add projects by source
        include_subdirectory = ''
        include_directory = ''
        include_main_cpp = '#include<iostream>\n\n'
        cout_main_cpp = ''

        for _folder_with_src in include_folders_with_source:

            # Projects included by source
            include_subdirectory += 'target_include_directories(' + project_name \
                                    + ' PUBLIC ${SOURCES_FOR_DEPENDENCY_PROJECTS}/' \
                                    + _folder_with_src + '/src)\n'

            # Include folders with headers
            include_directory += 'add_subdirectory(${SOURCES_FOR_DEPENDENCY_PROJECTS}/' + project_name \
                                 + ' ${IMPORTED_LIB_BY_SOURCES}/' + project_name + '/headers)\n'

            include_main_cpp += '#include "' + project_name + '.h";\n'
            cout_main_cpp += '    std::cout << ' + project_name + '(10) << std::endl;\n'

        # Place CMake file
        self.cmake_exe_factory.place_cmake(file_path=folder_path,
                                           vars={'PROJECT_NAME': project_name + '_project',
                                                 'TARGET': project_name,
                                                 'LINKED_LIBS': link_libs,
                                                 'INCLUDE_SUBDIRECTORY': include_subdirectory,
                                                 'TARGET_INCLUDE_DIRS': include_directory})
        # Place cpp file
        cpp_body = cout_main_cpp + '\n    std::cin.get();\n'

        self.lib_main_factory.place_with_name(file_path=folder_path,
                                              file_name=project_name + '.cpp',
                                              vars={'INCLUDES': include_main_cpp,
                                                    'CODE_CPP': cpp_body})

    def place_for_libexe(self, folder_path):
        pass


# fill_obj = FillFolder()
# pprint.pprint(fill_obj.dependency)

