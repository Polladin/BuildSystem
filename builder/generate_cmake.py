
import os
import shutil
import time

from build_system.builder.cmd_executor import SysCommandExecutor


class GenerateSolutions:

    @staticmethod
    def run(src_folder, with_sources, del_previous_build_folder=False):

        if not os.path.exists(src_folder):
            raise RuntimeError('Folder is not exist : ' + src_folder)

        src_folder += '/build'

        # Delete builder folder if needed
        if os.path.exists(src_folder) and del_previous_build_folder:
            shutil.rmtree(src_folder)

        time.sleep(0.5)

        # Create builder folder if it doesn't exist
        if not os.path.exists(src_folder):
            os.makedirs(src_folder)

        time.sleep(0.5)

        # Create a command
        cmd_to_generate = ['cmake',
                           '..',
                           '-G', 'Visual Studio 14 2015 Win64',
                           '-DWITH_SOURCES=' + ';'.join(with_sources)]
        print(cmd_to_generate)

        # Run command
        output, err = SysCommandExecutor.exec(cmd=cmd_to_generate,
                                              work_dir=src_folder,
                                              print_to_console=True)

        if err:
            print('ERRORS:')
            print(err)
            return False

        return True


# GenerateSolutions.run('D:/Projects/DINS/HG_server/tas_group_test', ['common', 'common_libW', 'phoneparser'])
