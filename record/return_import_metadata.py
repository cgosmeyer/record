import sys


# try this subprocess.call(['conda', 'list'])


def return_import_metadata():
    """

    Returns 
    -------
    module_names : list of strings
        The names of the imported modules.
    module_paths : list of strings
        The paths to the modules' installed location in the running 
        environment.
    module_versions : list of strings
        List of the modules' version numbers.

    References
    ----------
    https://stackoverflow.com/questions/4858100/how-to-list-imported-modules
    """
    module_names = list(set(sys.modules) & set(globals()))
    module_classes = [sys.modules[name] for name in module_names]
    module_paths = []
    module_versions = []

    for module in module_classes:
        try:
            module_paths.append(module.__path__[0])
        except:
            module_paths.append('built-in')
            
        try:
            module_versions.append(module.__version__)
        except:
            module_versions.append(None)

    return module_names, module_paths, module_versions 
