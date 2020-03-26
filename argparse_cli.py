"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Marria Padalko

This function accept argument from user regarding operational parameters
"""

import sys
import argparse

MIN_NUM_OF_ARG = 2


def parse_args_cli():
    """
    Parsing args from cli input
    :returns
    infinity parameter - boolean, when set to True ill collect data until interrupt
    quiet parameter - boolean, when set to True will suppress driver window popup
    number of readings parameter - int, when not run in infinity mode, determine number of iterations
    """
    parser = argparse.ArgumentParser(description="Parse 3 parameters")
    parser.add_argument('-i', '--infinity', action='store_true', default=False, help='Set to True for indefinite '
                                                                                     'match collection')
    parser.add_argument('-n', '--number_of_iterations', type=int, default=0, help='When not run with the infinity '
                                                                                  'parameter - determine number of '
                                                                                  'scraping iterations')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Quiet mode. When set to True - '
                                                                                  'suppress driver window popup')
    args = parser.parse_args()
    if len(sys.argv) < MIN_NUM_OF_ARG:
        parser.error("Too few arguments")
    if args.infinity == bool(args.number_of_iterations):
        parser.error("Invalid input provided.\
        \nPlease choose exactly one operation mode: \
        Infinity mode (-i) for indefinite data collection or specify desired number of iterations (-n <NUMBER>)")
    print(args.infinity, args.number_of_iterations, args.quiet)
    return [args.infinity, args.number_of_iterations, args.quiet]


if __name__ == '__main__':
    parse_args_cli()
