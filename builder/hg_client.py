
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

        if err != '':
            print('Error : ', err)
            return False

        print(output)
        return True

    def get_current_commit(self, repo_path):

        cmd = 'hg --debug id -i'

        output, err = SysCommandExecutor.exec(cmd=cmd,
                                              work_dir=repo_path,
                                              print_to_console=False)

        if err != '':
            raise RuntimeError('Error : ', err)

        return output.strip().strip('+')

    def get_current_commits_for_modules(self, root_folder, modules):

        models_commits = {}

        for _module_name in modules:
            models_commits[_module_name] = self.get_current_commit(root_folder + '/' + _module_name)

        return models_commits

    def get_parent_commits(self, repo_path, current_commit):

        cmd = 'hg --debug log --rev "' + current_commit + '"'

        output, err = SysCommandExecutor.exec(cmd=cmd,
                                              work_dir=repo_path,
                                              print_to_console=False)

        if err != '':
            print('Error : ', err)
            return False

        # Get parents
        parents = []

        for _line in output.split('\n'):

            # pprint.pprint(_line[:len('parent:')])
            # print(_line)

            if _line[:len('parent:')] == 'parent:' and int(_line.split(':')[1].strip()) > 0:
                parents.append(_line.split(':')[2].strip())

        return parents

    def get_current_branch(self, repo_path):

        cmd = 'hg branch'

        output, err = SysCommandExecutor.exec(cmd=cmd,
                                              work_dir=repo_path,
                                              print_to_console=False)

        if err != '':
            raise RuntimeError('Error :', err)

        return output.strip()

    def get_short_commit(self, repo_path, commit_hash):

        cmd = ['hg', 'log', '-l100', '--debug']

        output, err = SysCommandExecutor.exec(cmd=cmd,
                                              work_dir=repo_path,
                                              print_to_console=False)

        if err != '':
            raise RuntimeError('Error :', err)

        short_commit = ''
        for _line in output.split():
            if _line.find(commit_hash) != -1:
                short_commit = _line
                break

        return short_commit.split(':')[0]

# HGClient().clone('D:/Projects/DINS/build_system/tas_group3', 'D:/Projects/DINS/HG_server' + '/common')

# if os.path.isdir('D:/Projects/DINS/build_system/tas_group3'):
#     shutil.rmtree('D:/Projects/DINS/build_system/tas_group3')
#
# pathlib.Path('D:/Projects/DINS/build_system/tas_group3').mkdir(parents=True, exist_ok=True)
#
# structure = json.load(open('../repo_models/config/folder_structure.json'))
# modules = list(structure.keys())
#
# HGClient().clone_all('D:/Projects/DINS/build_system/tas_group3', 'D:/Projects/DINS/HG_server', modules)

