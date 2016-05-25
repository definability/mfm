from unittest import defaultTestLoader
from .src import test_cases

tests = [defaultTestLoader.loadTestsFromTestCase(test) for test in test_cases]

__all__ = ['tests']

