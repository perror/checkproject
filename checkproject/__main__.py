# -*- coding: utf-8

"""Main program when called as a command line software"""

def main(args):
    """Main function of the checkproject module"""

    # Parsing the arguments of the command line interface
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('projectdir', help='path to the project top directory')
    parser.add_argument('checkdir', help='path to checks top directory')
    parser.add_argument('-l', '--list-checks', action='store_true',
                        help='list of all the checks found')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='increase output verbosity')

    args = parser.parse_args()

    # Checking the project
    from checkproject.runner import CheckRunner
    check_runner = CheckRunner(args.projectdir, args.checkdir)

    # List all the checks found in the execution order.
    if args.list_checks:
        print('Listing all checks')
        print('------------------')
        for check in check_runner.list():
            print(check + '()')
        sys.exit(0)

    if args.verbosity > 0:
        print("Running the checks...")

    result = check_runner.run()

    print('')
    print('Results summary')
    print('---------------')
    print(result.summary())


# Main function
if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
