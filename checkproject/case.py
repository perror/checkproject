# -*- coding: utf-8
# Checkcase class implementation.

"""Checkcase class implementation.

There is three kinds of ways to fail a check:
 - Warning: Generate a warning message but do not count as an error.
 - Error: Generate an error message and count as an error.
 - Failure: Generate a failure message and stop the run of the checks.

"""

class Failure(Exception):
    """Failure exception is used to stop the execution of the checks."""


class CheckCase(object):
    """A class whose instance are single check cases.

    By default the code of the checks should be placed in methods
    starting with 'check_' in order to be executed. If required, the
    user can override a 'setup()' and a 'teardown()' method that are
    executed, respectively, before and after each checking method.

    Checks are conducted through three types of check methods, namely:

     - 'C{warning()}' to notify the student of a potential risk or a
       bad habit that should be cared about.

     - 'C{error()}' to notify that an error has been found in the
       student's program.

     - 'C{failure()}' to notify that the checking process has been
       interrupted because a failure has been found in the program
       (important files are missing, build does not succeed, ...).

    """

    def __init__(self, project_path):
        self.project_path = project_path
        self.result = None

    def description(self):
        """Returns a one-line description of the check, or None if no
        description has been provided.

        The default implementation of this method returns the first
        line of the specified check method's docstring.

        """
        doc = self.__doc__
        return doc and doc.split("\n")[0].strip() or None

    def setup(self):
        "Hook method for setting up the check fixture before starting it."
        pass

    def teardown(self):
        "Hook method for deconstructing the check fixture after finishing it."
        pass

    # The three types of checks: Warning, Error and Failure.
    # A Failure will immediately stop the checks and return.
    def warning(self, expr, result=None, hidden=False):
        """A warning is something that may be notified to the students as a
        potential error or a side-effect of a potential error. But,
        this is not really an error. It might also be the result of a
        check that may have false-positive. In this last case, you may
        report it to the student or leave it hidden to be read later
        on by the student's supervisor.

        @param expr: A logical expression performing the check and
        returning True (check passed) or False (check failed).

        @param result: Data-structure handling the report when the
        check fail.

        @param hidden: Tell if the result of the check will be
        available for the student or for his supervisor only.

        """
        if not expr:
            self.result.add_warning(result, hidden)
        else:
            self.result.add_success(hidden)

    def error(self, expr, result=None, hidden=False):
        """An error is something that is bad with no doubt, it may be reported
        to the student or reported in the final report while marking
        the code.

        @param expr: A logical expression performing the check and
        returning True (check passed) or False (check failed).

        @param result: Data-structure handling the report when the
        check fail.

        @param hidden: Tell if the result of the check will be
        available for the student or for his supervisor only.

        """
        if not expr:
            self.result.add_error(result, hidden)
        else:
            self.result.add_success(hidden)

    def failure(self, expr, result=None):
        """A failure is something that breaks enough the software to stop the
        checks and return immediately. It may be a problem with the
        build phase or an error admittedly to be so bad that it has to
        be fixed before trying to mark the code again. Note that a
        failure cannot be hidden to the student as it has to be fixed
        immediately.

        @param expr: A logical expression performing the check and
        returning True (check passed) or False (check failed).

        @param result: Data-structure handling the report when the
        check fail.

        """
        if not expr:
            self.result.add_failure(result)
            raise Failure('warning: check failed!')
        else:
            self.result.add_success()

    def list(self, pattern='check_.*'):
        """List all the checks discovered in the order of execution.

        @return: A list of all the checks ordered as for executing it.

        """
        # Get all the methods starting with 'pattern'
        import re
        return [check for check in dir(self)
                if re.compile(pattern).search(check)]

    def run(self, result=None, pattern='check_.*'):
        """Run all the methods of the class starting with 'check_*'.
        And, enclosing it between a call to the 'setup()' method at
        start and a call to the 'teardown()' method upon termination.

        @param result: Data-structure to store the result of all the checks.
        """
        # Initialize the 'result' object
        from checkproject.result import CheckResult
        if result is None:
            self.result = CheckResult()
        else:
            self.result = result

        # Get all the methods starting with 'pattern'
        import re
        checks = [check for check in dir(self.__class__)
                  if re.compile(pattern).search(check)]

        # Scanning all the checks in this CheckCase
        for method in checks:
            check_method = getattr(self, method)
            self.setup()
            try:
                check_method()
            except Failure:
                break
            finally:
                self.teardown()

        return self.result
