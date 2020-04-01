"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This function accept argument from user regarding operational parameters
"""

import argparse
from config import MIN_NUM_OF_ARG, PASSWORD, HOST_NAME, DB_FILENAME


def parse_args_cli():
    """
    Parsing args from cli input
    :returns
    infinity parameter - boolean, when set to True ill collect data until interrupt
    quiet parameter - boolean, when set to True will suppress driver window popup
    number of readings parameter - int, when not run in infinity mode, determine number of iterations
    localhostname - user's host name, defaults to 'localhost'
    password - user's password to MySQL server, defaults to 'root'
    dbname - name of database, default is 'hs_stats'
    overwrite option - boolean, when set to True will overwrite existing database
    """

    parser = argparse.ArgumentParser(description='Parse parameters for web scraping and creating DB')

    # Run arguments
    parser.add_argument('-i', '--infinity', action='store_true', default=False, help='Use flag for indefinite '
                                                                                     'match collection')
    parser.add_argument('-n', '--number_of_iterations', type=int, default=0, help='When not run with the infinity '
                                                                                  'parameter - determine number of '
                                                                                  'scraping iterations')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Quiet mode. Use flag to \
                                                                                  suppress driver window popup')
    # MySQL and DB arguments
    parser.add_argument('-l', '--localhostname', type=str, default=HOST_NAME,
                        help='Use flag to set user\'s host name, defaults to %s '
                             '(default can be changed in config file)' % HOST_NAME)

    parser.add_argument('-p', '--password', type=str, default=PASSWORD, help='Use flag to set password for MySQL '
                                                                             'server. will use password in config '
                                                                             'file if non was provided')

    parser.add_argument('-d', '--dbname', type=str, default=DB_FILENAME,
                        help='Ues flag to set name of database to create and/or use, default is "%s" '
                             '(default can be changed in config file)' % DB_FILENAME)

    parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='By default script will update \
                                                                            the given database if it already exists. \
                                                                            Use this flag to overwrite it instead')
    args = parser.parse_args()

    summary_of_run_args = bool(args.infinity) + bool(args.number_of_iterations)
    if summary_of_run_args < MIN_NUM_OF_ARG:
        parser.error("Too few arguments provided")
    if args.infinity == bool(args.number_of_iterations):
        parser.error("Invalid input provided.\
        \nPlease, choose exactly one operation mode: Infinity mode (-i) for indefinite data collection or "
                     "specify desired number of iterations (-n <NUMBER>)")
    return [args.infinity, args.number_of_iterations, args.quiet,
            args.localhostname, args.password, args.dbname, args.overwrite]


if __name__ == '__main__':
    parse_args_cli()
