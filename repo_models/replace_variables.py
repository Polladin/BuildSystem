import os


class Replacement:

    @staticmethod
    def replace_variables_in_line(line, variables):

        # Does a line has any variables to replace
        if line.count('%') <= 1:
            return line

        # Find all variables
        vars_positions = [pos for pos, ch in enumerate(line) if ch == '%']

        # Number of chars '%' should be even
        if len(vars_positions) % 2 != 0:
            raise RuntimeError('A line has odd % :', vars_positions, line)

        # Get variables name
        vars_name = []

        for i in range(int(len(vars_positions) / 2)):
            vars_name.append(line[vars_positions[2 * i]:vars_positions[2 * i + 1] + 1])

        for _var_name in vars_name:

            # A variable should be in a variables list
            if _var_name.strip('%') not in variables:
                raise RuntimeError('Variable :', _var_name, ': should be in variables')

            # Replace
            line = line.replace(_var_name, variables[_var_name.strip('%')])

        return line

    @staticmethod
    def place_file(template_lines, variables, file_path):

        # Initialize body
        body = ''

        # Write template to body and replace variables
        for _line in template_lines:

            # Replace variables in a line
            new_line = Replacement.replace_variables_in_line(_line, variables)

            # Add line to body
            body += new_line

        # Save a file
        folder = file_path[:file_path.rfind('/')]
        if not os.path.exists(folder):
            os.makedirs(folder)

        new_file = open(file_path, 'w')
        new_file.write(body)
        new_file.close()

