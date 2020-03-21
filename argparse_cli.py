import argparse
import math


def parse_args_cli():
    """Parsing args from cli input"""
    parser = argparse.ArgumentParser(description="Parse 3 parameters")
    parser.add_argument('-i', '--infinity', action='store_true', default=False, \
                        help='Set to True for indefinite value collection')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode. \
                        When set to True - suppress driver window popup', default=False)
    parser.add_argument('--number_of_readings', '-n', type=int, default=1, help='Only relevant when INFINITE is set \
                        to False - determine number of scraping iterations')
    args = parser.parse_args()
    return [args.infinity, args.number_of_readings, args.quiet]


def check_args():
    """Checking infinity, etc"""
    triple = parse_args_cli()
    if triple[0]:
        if triple[1]:
            print('Either infinity either number, not both :)\n-i -n <NUMBER> yelds invalid input. Choose only 1 of them')
            raise ValueError
        triple[1] = math.inf
    return triple


if __name__ == '__main__':
     check_args()


# Click : unsuccesful
# import click  # 7.1.1 version
#
#
# @click.command()
# @click.option('--infinity', '-i', is_flag=True,
#               help='Do you want parse till infinity?:)')
# @click.option('--number_of_feed_readings', '-n', default=1, prompt=True, type=int,
#               help='Number?:)')
# @click.option('--quiet', '-q', is_flag=True,
#               help='Do you want quiet mode?')
# def clickcli(infinity, number_of_feed_readings, quiet):
#     """Processing arguments from cli"""
#     click.echo('Inf: {}, num: {} and quiet: {}'.format(infinity, number_of_feed_readings, quiet))
#     inf, num, qui = infinity, number_of_feed_readings, quiet
#     return [inf, num, qui]
#
#
# if __name__ == "__main__":
#     clickcli()