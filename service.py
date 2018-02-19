
# encoding: utf-8 

import os
import sys
import argparse
import json
from datetime import datetime
from inmet_scrapper import crawler_inmet as crawler
from inmet_scrapper import mongodb as datahub


parser = argparse.ArgumentParser(
    description='''Scrapper de dados de estações automáticas do INMET 
- Instituto Nacional de Meteorologia - http://www.inmet.gov.br/sonabra/
    ''',
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-v", "--verbose", action='store_true', dest='verbose', help="Verbose mode", default=False)
parser.add_argument("-c", "--station", dest='station', help="""Especifica o código da estação, \
com 4 caracteres\n ex: ./getDadosInmetjs -c A701""")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if __name__ == "__main__":

    print('[I][{dt:%Y%m%d%H%M}][PID.{pid}] Inicio - {path}'.format(dt=datetime.now(), pid=os.getpid(), path=sys.argv[0]))

    # Crawler/parser
    station_data = crawler.run(args.station)
    
    # Datahub - MongoDb
    data_insert = datahub.insert_data(args.station, station_data)

    sys.exit(0)
