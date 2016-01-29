"""Check Student Programming Project

A collection of functions and classes designed to automatize the checks
applied to student's programming assignments to give feed-back on it
to the students and partial evaluation to the teacher.

"""
from checkproject.case import CheckCase
from checkproject.runner import CheckRunner

__version__ = '0.0.1'
__all__ = ['CheckCase', 'CheckRunner']
