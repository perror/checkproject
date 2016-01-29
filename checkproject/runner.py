"""Runner to discover, run and collect the results of all the checks."""

def import_module(module_path):
    """Import a Python file as a module in the current context.

    @param module_path: Path to the Python file.

    @return: A reference to the module once loaded.

    """
    import os
    import sys

    module_filename = module_path.split(os.sep)[-1]
    if int(sys.version[0]) >= 3:
        if int(sys.version[2]) >= 5:
            # Running a Python 3.5+ version
            from importlib.util import spec_from_file_location, module_from_spec
            spec = spec_from_file_location(module_filename, module_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

        else:
            # Running a Python <= 3.4 version
            from importlib.machinery import SourceFileLoader
            module = SourceFileLoader(module_filename, module_path).load_module()
    else:
        # Running a Python 2 version
        import imp
        module = imp.load_source(module_filename, module_path)

    return module

class CheckRunner(object):
    """A class to discover all the checks, run it sequentially and collect
    all the results.

    """

    def __init__(self, project_dir, checks_dir):
        """Initialize the default runner class.

        @param project_dir: Root directory where to find the source
        files of the tested project.

        @param checks_dir: Root directory where to find are all the
        checks.

        """
        self.project_dir = project_dir
        self.checks_dir = checks_dir
        self.checks = None

    def discover(self, pattern='check_*.py', top_dir=None):
        """Discover all the checks in the directory 'top_dir' with all methods
        matching the given pattern 'pattern' and update the list of checks.

        @param pattern: Prefix pattern of the methods for all
        checks.

        """
        from checkproject.utils import remove_prefix
        import os
        import fnmatch

        if top_dir is None:
            top_dir = self.checks_dir

        # List of all the check files detected
        check_paths = []

        # Scanning all files and subdirectories in breadth-first
        for path, _, files in os.walk(os.path.abspath(top_dir)):
            for filename in fnmatch.filter(files, pattern):
                check_paths.append(remove_prefix(os.path.join(path, filename),
                                                 self.checks_dir))
        # Initialize self.checks
        if self.checks is None:
            self.checks = []
        # Update self.checks
        self.checks = sorted(set(self.checks + check_paths))

    def list(self, pattern='Check*'):
        """List all the checks discovered in the order of execution.

        @return: A list of all the checks ordered as for executing it.

        """
        import os
        import re

        # Initializing self.checks if needed
        if self.checks is None:
            self.discover()

        # Initializing return value
        checks = []

        # Scanning all the modules
        for check_module in self.checks:
            module_path = os.path.join(self.checks_dir, check_module)
            module_name = module_path.split(os.sep)[-1].split('.')[0]
            module = import_module(module_path)

            # Extract all the 'Check' classes
            classes = [cls for cls in dir(module)
                       if re.compile(pattern).search(cls) and cls is not 'CheckCase']

            for class_name in classes:
                cls = getattr(module, class_name)
                check = cls(self.project_dir)
                checks += [module_name + '.' + cls.__name__ + '.' + m
                           for m in check.list()]

        return checks


    def run(self, pattern='Check*'):
        """Execute the checks and collect all the results"""
        import os
        import re

        # Initializing self.checks if needed
        if self.checks is None:
            self.discover()

        # Initializing return value
        result = None

        # Scanning all the modules
        for check_module in self.checks:
            module_path = os.path.join(self.checks_dir, check_module)
            module = import_module(module_path)

            # Extract all the 'Check' classes
            classes = [cls for cls in dir(module)
                       if re.compile(pattern).search(cls) and cls is not 'CheckCase']

            for class_name in classes:
                cls = getattr(module, class_name)
                check = cls(self.project_dir)
                result = check.run(result)

        return result
