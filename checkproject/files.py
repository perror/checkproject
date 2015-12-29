# -*- coding: utf-8 -*-
"""Handling file checking inside a project"""

class Files(object):
    """Class to scan, store and search in the files and directories found in the
    project.

    This class define a specific format to list the files enclosed in the
    project. Basically this is a list with a tuple for each
    file/directory/link found in the project: C{(path, type[, extra])}

    Where:
      - C{path}: is a string giving the path of the file in project.
      - C{type}: is either C{'f'} (file), C{'d'} (directory), C{'l'} (link)
      - C{extra}: is a free field that may be present or not depending of
        the type of the item.

    For example:
      - C{('src', 'd')} is a directory.
      - C{('src/project.c', 'f')} is a simple file.
      - C{('src/project', 'f', 'executable)} is an executable file.
      - C{('include/module.h', 'l', 'src/module.h')} is a symbolic
        link pointing to 'src/module.h'.

    """

    def __init__(self, project_path):
        self.root = project_path
        self.files = self.scan()

    def scan(self):
        """Scan all the files and directories present in the project

        @return: A list of all the files and directories found in the
        project.

        """
        from checkproject.utils import remove_prefix
        import os

        files = []

        for root, dirnames, filenames, in os.walk(self.root):
            for _file in [os.path.join(root, _f) for _f in filenames]:
                if os.access(_file, os.X_OK):
                    files.append((remove_prefix(_file, self.root), 'f',
                                  'executable'))
                elif os.path.islink(_file):
                    files.append((remove_prefix(_file, self.root), 'l',
                                  os.path.realpath(_file)))
                else:
                    files.append((remove_prefix(_file, self.root), 'f'))

            for _dir in [os.path.join(root, _d) for _d in dirnames]:
                files.append((remove_prefix(_dir, self.root), 'd'))

        return sorted(files)

    def required(self, required_files):
        """Check if all the required files are present in the last scan.

        @param required_files: list of all the required file that must be
        enclosed in the project. Each item of the list must be specified
        in the specific format of this module: '(path, type, extra)'.

        @return: A list of the missing files.
        """
        missing_files = []

        for required_file in required_files:
            for _file in self.files:
                if _file == required_file:
                    break
            else:
                missing_files.append(required_file)

        return missing_files

    def unwanted(self, unwanted_files):
        """Check if given globbing expressions match any file of the last scan.

        @param unwanted_files: list of regular expressions of unwanted files
        in the project. Each item of the list must be specified in the
        specific format of this module: '(path, type, extra)'.

        """
        import fnmatch, re
        unwanted = []

        for unwanted_file in unwanted_files:
            pattern = re.compile(fnmatch.translate(unwanted_file[0]))
            for _file in self.files:
                if re.match(pattern, _file[0]) and (unwanted_file[1:] == _file[1:]):
                    unwanted.append(_file)

        return unwanted

    def diff(self, path=None):
        """Check the content of the project against the one """
        pass
