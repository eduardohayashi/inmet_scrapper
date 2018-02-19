# encoding: utf-8

import base64
import sys
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def run(station):
    '''
    :param station string: 
    :return list
    '''
    if len(station) != 4:
        raise Exception('Estação inválida ou não encontrada')
    
    b64station = encode_b64(station)
    print('[Estação {station} - b64: {b64} - {path}'.format(
        station=station,path=sys.argv[0], b64=b64station))

    today = datetime.today().strftime('%d/%m/%Y')
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.strftime('%d/%m/%Y')

    page_code = load_page(b64=b64station, dtaini=yesterday, dtafim=today)
    data_station = parser_page(page_code.text)

    return data_station

    
def encode_b64(station):
    '''
    :param station string 
    :return binary
    '''
    return base64.b64encode(station.encode('ascii'))


def decode_b64(b64):
    '''
    :param b64 binary
    :return string
    '''
    return b64.decode('ascii')


def load_page(b64, dtaini, dtafim):
    '''
    :param b64 binary
    :param dtaini string
    :param dtafim string
    :return list
    '''
    url = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'+decode_b64(b64);
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.inmet.gov.br',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php'
    }
    data = {"aleaValue": "MDcwOQ==", "aleaNum": "0709", 
        "dtaini": dtaini, "dtafim": dtafim, "submit": "OK"}
    params = {'sessionKey': '', 'format': 'xml', 'platformId': 1}

    # obs: Se a versão de requests for menor que 2.14.2, é necessário 
    # importar json e usar json.dumps() na data
    return requests.post(url, data=data, headers=headers)


def parser_page(html_code):
    '''
    :param html_code string 
    :return list
    '''
    
    soup = BeautifulSoup(html_code, 'html.parser')
    station_data = soup.contents[2].contents[3].contents[1].contents[3].contents[1] \
        .contents[5].contents[3].contents[1].contents[3].contents[1].contents[5].contents[3]

    data_station_list = list()
    station_dict = dict()
    c = 0
    for line in station_data:
        
        if c==0 or c%2==0:
            c = c+1
            continue
        c = c+1

        station_dict['date'] = line.contents[0].contents[0].text
        station_dict['time'] = line.contents[1].contents[0].text
        station_dict['temp_inst'] = line.contents[2].contents[0].text
        station_dict['temp_max'] = line.contents[3].contents[0].text
        station_dict['temp_min'] = line.contents[4].contents[0].text
        station_dict['umid_inst'] = line.contents[5].contents[0].text
        station_dict['umid_max'] = line.contents[6].contents[0].text
        station_dict['umid_min'] = line.contents[7].contents[0].text
        station_dict['dewpoint_inst'] = line.contents[8].contents[0].text
        station_dict['dewpoint_max'] = line.contents[9].contents[0].text
        station_dict['dewpoint_min'] = line.contents[10].contents[0].text
        station_dict['pres_inst'] = line.contents[11].contents[0].text
        station_dict['pres_max'] = line.contents[12].contents[0].text
        station_dict['pres_min'] = line.contents[13].contents[0].text
        station_dict['wind_vel'] = line.contents[14].contents[0].text
        station_dict['wind_dir'] = line.contents[15].contents[0].text
        station_dict['wind_raj'] = line.contents[16].contents[0].text
        station_dict['radiation'] = line.contents[17].contents[0].text
        station_dict['rain'] = line.contents[18].contents[0].text
        
        data_station_list.append(station_dict)
        station_dict = dict()
    
    return data_station_list
        
        



