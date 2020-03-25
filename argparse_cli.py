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
    if len(sys.argv) < MIN_NUM_OF_ARG:  # TODO: The function ran without any input, this shouldn't happen
        parser.error("too few arguments")
    return [args.infinity, args.number_of_iterations, args.quiet]


# TODO: in Hs_Stats you are calling this function 3 times. you need to call it once and than parse the return not
#  call it three times and take one argument from each function call (see how I did in HS_Stats now)
def check_args():
    """Checking infinity, etc"""  # TODO: Need a better explanation of what the function does and returns (see above)
    arguments = parse_args_cli()
    if arguments[0]:
        if arguments[1]:
            print('Invalid input provided!\nPlease choose operation mode: Infinity mode (-i) for indefinite data '
                  'collection or specify desired number of iterations (-n <NUMBER>)')
            raise ValueError  # TODO: Handle this error in try/except, its incorrect to raise the error and ignore it
        # arguments[1] = math.inf  # TODO: Why? the infinity argument is True or False, this isn't needed
    return arguments


if __name__ == '__main__':
    check_args()
