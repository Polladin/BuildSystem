
import pycurl
import os
from urllib import request


class NexusManager:

    def __init__(self):

        self.nexus_url = 'http://192.168.56.101:8081/repository/repo_4'

    def upload_file(self, filepath, filename, version, nexus_repo):

        data = open(filepath, 'rb')
        url_post = self.nexus_url + '/' + nexus_repo + '/' + filename + '/' + version + '/' + \
                        filename + '-' + version + '.' + filepath.split('.')[-1].strip()

        c = pycurl.Curl()
        c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.URL, url_post)

        c.setopt(pycurl.PUT, 1)
        c.setopt(c.READDATA, data)
        c.setopt(c.INFILESIZE, os.path.getsize(filepath))
        c.setopt(pycurl.USERPWD, "admin:admin123")
        c.setopt(pycurl.CUSTOMREQUEST, "PUT")

        c.perform()
        c.close()

    def download_file(self, nexus_repo, module_name, branch_name, subfolder, nexsus_place, to_folder):

        download_url = 'http://192.168.56.101:8081/repository/repo_4/' + nexus_repo + '/' + module_name + \
                       '/' + branch_name + '/' + subfolder + '/' + module_name + '/' + str(nexsus_place) + \
                       '/' + module_name + '-' + str(nexsus_place) + '.txt'

        request.urlretrieve(download_url, to_folder)

    def upload_module(self, path_to_file, modula_name, module_info, subfolder):
        """
        :param subfolder: type of a files, example [headers, lib_centos64, lib_win64]
        :param module_info: in format {'hash_commit' : ...,
                                       'branch_name': ...,
                                       'nexus_place': ...}
        """

        self.upload_file(filepath=path_to_file, filename=modula_name, version=str(module_info['nexus_place']),
                         nexus_repo='test_6/' + modula_name + '/' + module_info['branch_name'] + '/' + subfolder)

    def upload_3d_parties(self, path_to_file, lib_name, subfolder, file_name, version):

        self.upload_file(filepath=path_to_file, filename=file_name, version=version,
                         nexus_repo='3d_parties_test_1/' + lib_name + '/' + subfolder)

    def download_module(self, module_name, module_info, subfolder, to_folder):

        self.download_file('test_6', module_name, module_info['branch_name'], subfolder, module_info['nexus_place'],
                           to_folder + '/' + module_name + '.txt')


module_info = {'hash_commit': '13cb2e0122c198cd7f8b3ca3c417ff48dffcd691', 'branch_name': 'default', 'nexus_place': 30}
NexusManager().download_module('phoneparser', module_info, 'lnx64', 'D:/libs/boost_program_options/')

# NexusManager().upload_3d_parties(path_to_file='D:/libs/boost_program_options/program_options_headers.zip',
#                                  lib_name='boost',
#                                  subfolder='headers',
#                                  file_name='program_options',
#                                  version='1_64')

# NexusManager().upload_3d_parties(path_to_file='D:/libs/boost_program_options/program_options_win.zip',
#                                  lib_name='boost',
#                                  subfolder='lib_win64',
#                                  file_name='program_options',
#                                  version='1_64')

# NexusManager().upload_file(filepath='D:/linux.png', #'storage/group_build_ver.json', # 'storage/group_build_ver.json', #
#                            filename='file11',
#                            version='2.5',
#                            nexus_repo='test')

