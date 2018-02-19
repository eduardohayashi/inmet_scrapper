# encoding: utf-8

import pymongo.errors
from pymongo import MongoClient
from inmet_scrapper.settings import CONFIG

def get_config(key):
    '''
    :param key string
    :return string
    '''
    global CONFIG
    return CONFIG[key]


def get_connection():
    '''
    :return MongoClient instance
    '''
    try:
        str_connection = 'mongodb+srv://{username}:{password}@{host}/{database}'.format(host=get_config('host'), \
            username=get_config('username'), password=get_config('password'), \
            database=get_config('database'))

        return MongoClient(str_connection)
    except pymongo.errors.ConfigurationError as e:
        print(e)
        print('[E][get_connection >> Verify connection config @ {e}')



def insert_data(station_code, dataset):
    '''
    :param station_code string
    :param dataset: list/dict
    :return boolean
    '''
    conn = get_connection()

    if conn:
        print('[I][Inserindo dados no database]')
        db = conn[get_config('database')]
        col = db[get_config('collection')]
        
        c = 0
        for row in dataset:
            station_id = station_code
            row['station_id'] = station_code
            date = row['date']
            time =  row['time']
            #del row['date'],  row['time']
            #print(row)
            col.update({'station_id':station_code, 'date':date, 'time': time}, {"$set":row}, upsert=True)
            c = c+1
        
        print('[I][{c} registros incluidos/atualizados]'.format(c=c))
        conn.close()

        return True
    return False
