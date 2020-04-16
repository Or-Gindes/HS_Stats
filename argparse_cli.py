"""
ITC Data-Mining Project
By: Or Gindes, Dor Sklar, Mariia Padalko

This function accepts argument from user regarding operational parameters
"""

import argparse
from config import HOST_NAME, DB_FILENAME


def parse_args_cli():
    """
    Parsing args from cli input
    :returns
    number of readings parameter - positive int, when not run in infinity mode, determine number of iterations
    quiet parameter - boolean, when set to True will suppress driver window popup
    hostname - user's host name, defaults to 'localhost'
    password - user's password to MySQL server
    dbname - name of database, default is 'hs_stats'
    overwrite option - boolean, when set to True will overwrite existing database
    infinity - will be set to True, is number of iterations is not given
    """

    parser = argparse.ArgumentParser(description='Parse parameters for web scraping and creating DB')

    # Run arguments
    parser.add_argument('-n', '--number_of_iterations', type=int, default=0, help='Determines the number of '
                                                                                  'scraping iterations. If not given, '
                                                                                  'the parser will iterate infinite'
                                                                                  'number of times')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Quiet mode. Use flag to \
                                                                                  suppress driver window popup')
    # MySQL and DB arguments
    parser.add_argument('-l', '--hostname', type=str, default=HOST_NAME,
                        help='Use flag to set user\'s host name, defaults to %s '
                             '(default can be changed in config file)' % HOST_NAME)

    parser.add_argument('-p', '--password', type=str, help='Password for MySQL server')
    parser.add_argument('-d', '--dbname', type=str, default=DB_FILENAME,
                        help='Use flag to set name of database to create and/or use, default is "%s" '
                             '(default can be changed in config file)' % DB_FILENAME)

    parser.add_argument('-o', '--overwrite', action='store_true', default=False, help='By default script will update \
                                                                            the given database if it already exists. \
                                                                            Use this flag to overwrite it instead')
    args = parser.parse_args()
    infinity = not bool(args.number_of_iterations)

    if not args.password:
        parser.error('Invalid input.\nPlease, provide password for MySQL')
    return args, infinity


if __name__ == '__main__':
    parse_args_cli()

