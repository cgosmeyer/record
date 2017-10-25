"""
Module that creates a script that can record all imports of the
module that this function is called from. 
"""

import os
import subprocess

def strip_imports(script):
    """ Strip out all import statements, including `import as`
    and `from ... import`

    This is ok for a first pass. But will fail if 'import' happens
    to be part of a name of a function or variable.
    Or just build a smarter try-except in return_import_metadata
    so anything not a real import will be ignored.

    What to do with local imports? How will know something is local?
    Scan the package first? (list 'local' for 'built-in')

    Also consider another function that will scan through the
    imports to record their imports. Make that an option?
    """
    # Read the script file
    with open(script, 'r') as f:
        lines = f.readlines()

    # Retain only import lines, but removing commented out imports, relative imports, and the function itself.
    # In addition, remove all leading space.
    stripped_lines = [line.lstrip(' ') for line in lines if 'import' in line \
        and '#' not in line \
        and 'from .' not in line \
        and 'meta_record_imports' not in line \
        and '__' not in line]

    # Change all 'from ... import' statements into 'import' statements
    # so to capture their versions, paths
    for i, line in enumerate(stripped_lines):
        if 'from' in line:
            module = (line.split(' ')[1]).split('.')[0]
            new_line = 'import {}\n'.format(module)
            stripped_lines[i] = new_line

    # Change all 'import as' statements to 'import' statements
    stripped_lines = ['{}\n'.format(line.split(' as ')[0]) if ' as ' in line else line for line in stripped_lines]

    # Change all remaining 'import.module' statements to 'import' statements
    stripped_lines = ['{}\n'.format(line.split('.')[0]) if '.' in line else line for line in stripped_lines]

    # Remove all repeats
    stripped_lines = list(set(stripped_lines))

    return stripped_lines


def meta_record_imports(path_running_script, print_or_log='print', path_logs=''):
    """

    Parameters
    ----------
    path_running_script : str
        Usually just '__file__'.

    Resources
    ---------
    https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
    """
    # Make sure no pre-existing temp_import.py
    if os.path.isfile("temp_import.py"):
        os.remove("temp_import.py")

    # Get the path to the module of this executing function.
    execute_path = os.path.dirname(os.path.realpath(__file__))

    # Read the function return_import_metadata
    with open(os.path.join(execute_path, "return_import_metadata.py"), 'r') as f:
        return_import_metadata = f.readlines()

    # Read the imports from the running script.
    # Returns list of import lines.
    stripped_lines = strip_imports(path_running_script)

    # Create a new temp file at the location of the running script
    # And write all the imports
    with open("temp_import.py", "w") as temp:
        for line in stripped_lines:
            temp.write(line)

        # Write the return_imports function into the new file
        # (it needs to be in the same location as the imports to work,
        #   so importing itself is not an option)
        for line in return_import_metadata:
            temp.write(line)

        # call the return_imports function
        temp.write("module_names, module_paths, module_versions = return_import_metadata()\n")

        if print_or_log == 'print':
            temp.write("print('EXECUTING: {}'.format('" + path_running_script + "'))\n")
            temp.write("print(' ')\n")
            temp.write("print('IMPORTING:')\n")
            temp.write("for n, p, v in zip(module_names, module_paths, module_versions):\n")
            temp.write("    print('MODULE NAME: {}'.format(n))\n")
            temp.write("    print('MODULE PATH: {}'.format(p))\n")
            temp.write("    print('MODULE VERS: {}'.format(v))\n")
            temp.write("    print(' ')\n")
        elif print_or_log == 'log':
            temp.write("import logging\n")
            temp.write("logging.info('EXECUTING: {}'.format('" + path_running_script + "'))\n")
            temp.write("logging.info(' ')\n")
            temp.write("logging.info('IMPORTING:')\n")
            temp.write("for n, p, v in zip(module_names, module_paths, module_versions):\n")
            temp.write("    logging.info('MODULE NAME: {}'.format(n))\n")
            temp.write("    logging.info('MODULE PATH: {}'.format(p))\n")
            temp.write("    logging.info('MODULE VERS: {}'.format(v))\n")
            temp.write("    logging.info(' ')\n")     

    # Write the output to a log file, at the path indicated in `path_logs`
    # by default this could be cwd? 

    # Run the temp file.
    subprocess.call(["python", "temp_import.py"])

    # Remove the temp file
    os.remove("temp_import.py")


