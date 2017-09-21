"""
Module that creates a script that can record all imports of the
module that this function is called from. 
"""

import os

def strip_imports(script):
    """ Strip out all import statements, including `import as`
    and `from ... import`
    """
    # Read the script file
    with open(script, 'r') as f:
        lines = f.readlines()

    # Retain only import lines, but removing commented out imports and relative imports.
    # In addition, remove all leading space.
    stripped_lines = [line.lstrip(' ') for line in lines if 'import' in line and '#' not in line and 'from .' not in line]

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


def meta_record_imports(path_running_script, path_logs):
    """

    Resources
    ---------
    https://stackoverflow.com/questions/5137497/find-current-directory-and-files-directory
    """
    # Get the path to the module of this executing function.
    execute_path = os.path.dirname(os.path.realpath(__file__))

    # Read the function return_import_metadata
    with open(os.path.join(execute_path, "return_import_metedata.py"), 'r') as f:
        return_import_metadata = f.readlines()

    # Read the imports from the running script.
    # Returns list of import lines.
    stripped_lines = strip_imports()

    # Create a new temp file at the location of the running script
    # And write all the imports
    with open("temp_import.py", "w") as temp:
        for line in stripped_lines:
            temp.write(line)

        # Write the return_imports function into the new file
        # (it needs to be in the same location as the imports to work,
        #   so importing itself is not an option)
        for line in return_meta_data:
            temp.write(line)

        # call the return_imports function
        temp.write("module_names, module_paths, module_versions = return_import_metadata()\n")
        temp.write("print(module_names)\n")
        temp.write("print(module_paths)\n")
        temp.write("print(module_versions)\n")

    # Write the output to a log file, at the path indicated in `path_logs`
    # by default this could be cwd? 

    # remove the temp file
    #os.remove("temp_import.py")


