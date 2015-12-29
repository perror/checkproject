# Checking project files and directories

from checkproject.case import CheckCase
from checkproject.files import Files

class CheckProjectFiles(CheckCase):
    """Checking the content of the projet."""

    def check_required(self):
        files = Files(self.project_path)

        # Check required files
        print("* Missing files:")

        required_files = [('include', 'd'),
                          ('include/module.h', 'f'),
                          ('Makefile', 'f'),
                          ('src', 'd'),
                          ('src/Makefile', 'f'),
                          ('src/module.c', 'f'),
                          ('src/project.c', 'f'),
                          ('src/project.h', 'f')]

        missing = files.required(required_files)

        if missing:
            print(missing)
        else:
            print('All the required files were found!')
        print('')

        self.failure((missing == []), '');

    def check_unwanted(self):
        """Checking if the project has unwanted files."""
        # Check unwanted files
        print("* Unwanted files:")

        files = Files(self.project_path)
        unwanted_files = [('*', 'f', 'executable'), ('*~', 'f'),
                          ('.*', 'f'),('_*', 'd'), ('._*', 'd')]
        unwanted = files.unwanted(unwanted_files)

        if unwanted:
            print(unwanted)
            # Recording the errors
            for item in unwanted:
                self.error(False)
        else:
            print('No unwanted file found!')
            self.error(True)
        print('')

 
