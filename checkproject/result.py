# -*- coding: utf-8

"""Check result object used to transfert the results of the checks
from one check to another all along the checks."""

class CheckResult(object):
    """Holder for check result information.

    Check results are automatically managed by the CheckCase class,
    and do not need to be explicitely manipulated by check writers.

    Each instance of CheckResult holds the total number of checks that
    have been run, and collections of errors, warnings and failures
    that occurred among these checks.
    """

    def __init__(self):
        self.scores = {'successes': 0, 'hidden_successes': 0,
                       'warnings': 0, 'hidden_warnings': 0,
                       'errors': 0, 'hidden_errors': 0,
                       'failed': False}

        self.warning_results = []
        self.hidden_warning_results = []
        self.error_results = []
        self.hidden_error_results = []
        self.failure_results = []

    def add_success(self, hidden=False):
        """Record a successful score to the results.

        @param hidden: Hide the result if True, show it otherwise.

        """
        if not hidden:
            self.scores['successes'] += 1
        else:
            self.scores['hidden_successes'] += 1

    def add_warning(self, result=None, hidden=False):
        """Add a warning score and its data to the results.

        @param result: Explanation of the fail.

        @param hidden: Hide the result if True, show it otherwise.

        """
        if not hidden:
            self.scores['warnings'] += 1
            if result is not None:
                self.warning_results.append(result)
        else:
            self.scores['hidden_warnings'] += 1
            if result is not None:
                self.hidden_warning_results.append(result)

    def add_error(self, result=None, hidden=False):
        """Add an error score and its data to the results.

        @param result: Explanation of the fail.

        @param hidden: Hide the result if True, show it otherwise.

        """
        if not hidden:
            self.scores['errors'] += 1
            if result is not None:
                self.error_results.append(result)
        else:
            self.scores['hidden_errors'] += 1
            if result is not None:
                self.hidden_error_results.append(result)

    def add_failure(self, result=None):
        """Add a failure score and its data to the results.

        @param result: Explanation of the fail.

        """
        self.scores['failed'] = True
        if result is not None:
            self.failure_results.append(result)

    def get_successes(self):
        """Returns the number of successes"""
        return self.scores['successes']

    def get_hidden_successes(self):
        """Returns the number of hidden successes"""
        return self.scores['hidden_successes']

    def get_all_successes(self):
        """Returns the number of all successes"""
        return self.scores['successes'] + self.scores['hidden_successes']

    def get_warnings(self):
        """Returns the number of warnings"""
        return self.scores['warnings']

    def get_hidden_warnings(self):
        """Returns the number of hidden warnings"""
        return self.scores['hidden_warnings']

    def get_all_warnings(self):
        """Returns the number of all warnings"""
        return self.scores['warnings'] + self.scores['hidden_warnings']

    def get_errors(self):
        """Returns the number of errors"""
        return self.scores['errors']

    def get_hidden_errors(self):
        """Returns the number of hidden errors"""
        return self.scores['hidden_errors']

    def get_all_errors(self):
        """Returns the number of all errors"""
        return self.scores['errors'] + self.scores['hidden_errors']

    def has_failed(self):
        """Returns True if a failure occured during the checks"""
        return self.scores['failed']

    def full_summary(self):
        """Returns a string with a complete summary of the results"""
        msg = 'Number of successful checks: ' + str(self.get_successes())
        msg += '\nNumbers of successful hidden checks: ' + str(self.get_hidden_successes())
        msg += '\nNumbers of warnings: ' + str(self.get_warnings())
        msg += '\nNumbers of hidden warnings: ' + str(self.get_hidden_warnings())
        msg += '\nNumbers of errors: ' + str(self.get_errors())
        msg += '\nNumbers of hidden errors: ' + str(self.get_hidden_errors())
        msg += '\nChecks failed: ' + str(self.has_failed())

        return msg

    def summary(self):
        """Returns a string with a summary of the results"""
        msg = 'Number of successful checks: ' + str(self.get_successes())
        msg += '\nNumbers of warnings: ' + str(self.get_warnings())
        msg += '\nNumbers of errors: ' + str(self.get_errors())
        msg += '\nChecks failed: ' + str(self.has_failed())

        return msg
