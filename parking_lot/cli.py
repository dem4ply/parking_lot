# -*- coding: utf-8 -*-
import logging
import sys
from argparse import ArgumentParser

from parking_lot.parking_lot_api import app, parking_lot_db


logger_formarter = '%(levelname)s %(name)s %(asctime)s %(message)s'


parser = ArgumentParser(
    description="parging lot", fromfile_prefix_chars='@'
)

parser.add_argument(
    "--log_level", dest="log_level", default="INFO",
    help="nivel de log",)

parser.add_argument(
    "--daily_fee", dest="daily_fee", default=20, type=int,
    help="set the daily fee",)

parser.add_argument(
    "--hourly_fee", dest="hourly_fee", default=1, type=int,
    help="set the hourly fee",)

sub_parsers = parser.add_subparsers(
    dest='command', help='sub-command help')

parser_server = sub_parsers.add_parser('runserver', help='run flask server',)
parser_server.add_argument(
    '--port', '-p', required=False, type=int, help='The port to bind to.',
    default=8000)


def main():
    """Console script for parking_lot."""
    args = parser.parse_args()
    logging.basicConfig(
        level=args.log_level, format=logger_formarter, force=True)

    if args.command == 'runserver':
        port = args.port
        parking_lot_db.hourly_fee = args.hourly_fee
        parking_lot_db.daily_fee = args.daily_fee
        app.run("0.0.0.0", port=port)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
