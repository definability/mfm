from argparse import ArgumentParser
from cProfile import Profile
from pstats import Stats
from unittest import TestSuite, TextTestRunner

from tests import tests


if __name__ == '__main__':

    profile = None

    parser = ArgumentParser(description='Testing arguments')
    parser.add_argument('-p', '--profile', action='store_true',
                        help='Gather and show profiler information')
    args = parser.parse_args()

    if args.profile:
        profile = Profile()
        profile.enable()

    exit_status = not TextTestRunner().run(TestSuite(tests)).wasSuccessful()

    if args.profile:
        profile.disable()
        Stats(profile).sort_stats('cumulative').print_stats()

    exit(exit_status)
