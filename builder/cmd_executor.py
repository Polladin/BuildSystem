
import subprocess
import sys


class SysCommandExecutor:

    @staticmethod
    def exec(cmd, work_dir, encoding='utf-8', print_to_console=True, shell=True):

        # Init output log
        output = ''
        err = ''

        # Run the CMD
        process = subprocess.Popen(cmd,
                                   cwd=work_dir,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=shell,
                                   universal_newlines=True)

        # for stdout_line in iter(process.stdout.readline, ""):
        #     print(stdout_line.rstrip())

        # output = process.stdout.readlines()
        # err = process.stderr.readlines()

        # Poll process for new output until finished
        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            output += nextline
            if print_to_console:
                sys.stdout.write(nextline)
                sys.stdout.flush()

        # output, err = process.communicate()
        err = process.communicate()[1]

        # # Print output from subprocess to stdout
        # while process.poll() is None:
        #     line = process.stdout.readline().strip()
        #     line_err = process.stderr.readline().strip()
        #
        #     if len(line) > 0:
        #         decoded_line = line.decode(encoding, "ignore") + '\n'
        #         if print_to_console:
        #             sys.stdout.write(decoded_line)
        #         output += decoded_line
        #
        #     if len(line_err) > 0:
        #         decoded_line = line_err.decode(encoding, "ignore") + '\n'
        #         if print_to_console:
        #             sys.stdout.write(decoded_line)
        #         err += decoded_line

        return output, err


