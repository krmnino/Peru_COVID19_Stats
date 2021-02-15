import datetime
import os
import sys
import time

from ParsingUtility import parse_file
from ParsingUtility import compute_data
from ParsingUtility import update_file
from ParsingUtility import get_raw_image_path
from ParsingUtility import crop_process_image
from ParsingUtility import read_image
from ParsingUtility import check_date
from ParsingUtility import get_raw_image_dimensions
from ParsingUtility import clean_dir
from ExportUtility import list_to_csv
from ExportUtility import export_tweets_to_file
from ExportUtility import update_git_repo_win32
from ExportUtility import update_git_repo_linux
from ExportUtility import GraphData
from ExportUtility import plot_loader
from TwitterUtility import load_auth
from TwitterUtility import fetch_image
from TwitterUtility import sleep_until
from TwitterUtility import send_thread
from TwitterUtility import tweets_generator
from CommandLineUtility import check_data_menu

'''
Structure of parsed_data list after computation
index   contents
0	    Dates
1	    Cases
2	    Deaths
3	    Tests
4       Recovered
5       Hospitalized
6   	Days
7   	New Cases
8	    % Cases
9   	New Deaths
10	    % Deaths
11      New Recovered
12      % Recovered
13      New Hospitalized  
14      % Hospitalized
15	    New Tests
16	    % Tests
17      Mortality Rate
18      Active Cases
19      New Active Cases
20      % Daily Positives
'''

def run(opt_date=datetime.date.today().strftime('%Y-%m-%d')):

    #Include this to Command Line Utility
    success_input_date = check_date(opt_date)
    if(success_input_date == 1):
        print('Invalid input date. Exiting...')
        return 1

    auth_data = load_auth()
    if(auth_data == 1):
        print('Could not load authenticator file. Exiting...')
        return 1

    clean_directory = clean_dir()
    if(clean_directory == 1):
        print('Could not clean raw_images directory. Exiting...')
        return 1   

    # [date, cases, deaths, tests, recovered, hospitalized, cases24h]
    input_data = {\
        'Date' : datetime.datetime.today().strftime('%Y-%m-%d'),
        'Cases' : 0,
        'Deaths' : 0,
        'Tests' : 0,
        'Recovered' : 0,
        'Hospitalized' : 0,
        'Cases24H' : 0
    }

    if(check_data_menu(input_data) == 1):
        print('Discard readings. Exiting...')
        return 1
    
    success_csv_write = update_file(input_data)
    if(success_csv_write == 1):
        print('Could not update CSV file.')
        return 1

    raw_data = parse_file()
    if(raw_data == 1):
        print('Could not parse CSV file.')
        return 1
    
    data = compute_data(raw_data)

    success_full_csv_write = list_to_csv(data)
    if(success_full_csv_write == 1):
        print('Could not export processed data.')

    graph_data = [\
        GraphData(  'scatter',
                    data[0], 
                    [data[1],data[18],data[4],data[2]], 
                    0,
                    'Dias',
                    ['# Casos Confirmados', '# Activos', '# Recuperados', '# Fallecidos'],
                    ['#D8D13B', '#E04646', '#9CD347', '#8C8C8C'],
                    'Casos Confirmados, Activos, Recuperados y Fallecidos de COVID19 en el Peru (acumulado)',
                    20,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'conf_act_rec_dea_cumulative.png',
                    input_data['Date'],
                    False,
                    True,
                    False,
                    -1,
                    0),
        GraphData(  'bar',
                    data[0], 
                    [data[19]], 
                    30,
                    'Dias',
                    ['# de Nuevos Casos Activos'],
                    ['#E04646'],
                    'Nuevos Casos Activos de COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'new_active_cases.png',
                    input_data['Date'],
                    False,
                    True,
                    True,
                    -1,
                    -1),
        GraphData(  'bar',
                    data[0], 
                    [data[11]], 
                    30,
                    'Dias',
                    ['# de Nuevas Recuperaciones'],
                    ['#9CD347'],
                    'Nuevas Recuperaciones del COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'recovered.png',
                    input_data['Date'],
                    False,
                    True,
                    True,
                    -1,
                    -1),
        GraphData(  'bar',
                    data[0], 
                    [data[5]], 
                    30,
                    'Dias',
                    ['# de Hospitalizados'],
                    ['#D8D13B'],
                    'Hospitalizados por COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'hospitalized.png',
                    input_data['Date'],
                    True,
                    True,
                    True,
                    -1,
                    -1),
        GraphData(  'bar',
                    data[0], 
                    [data[9]], 
                    30,
                    'Dias',
                    ['# de Nuevos Fallecimientos'],
                    ['#8C8C8C'],
                    'Nuevos Fallecimientos por COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'new_deaths.png',
                    input_data['Date'],
                    False,
                    True,
                    True,
                    -1,
                    0),
        GraphData(  'scatter',
                    data[0], 
                    [data[17]], 
                    30,
                    'Dias',
                    ['Tasa de Letalidad (* 100%)'],
                    ['#8C8C8C'],
                    'Tasa de Letalidad por COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'case_fatality_rate.png',
                    input_data['Date'],
                    True,
                    False,
                    False,
                    -1,
                    -1),
        GraphData(  'bar',
                    data[0], 
                    [data[15]], 
                    30,
                    'Dias',
                    ['# de Nuevas Pruebas'],
                    ['#5B90F3'],
                    'Nuevas Pruebas de COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'new_tests.png',
                    input_data['Date'],
                    False,
                    True,
                    True,
                    -1,
                    0),
        GraphData(  'scatter',
                    data[0], 
                    [data[20]], 
                    30,
                    'Dias',
                    ['Positividad Diaria (* 100%)'],
                    ['#5B90F3'],
                    'Positividad Diaria de COVID19 en el Peru (ultimos 30 dias)',
                    25,
                    input_data['Date'] + ' | Elaborado por Kurt Manrique-Nino (@krm_nino) | Datos del Ministerio de Salud del Peru (@Minsa_Peru)',
                    'perc_daily_positive_tests.png',
                    input_data['Date'],
                    True,
                    False,
                    False,
                    1,
                    0)
    ]

    plot_loader(graph_data)

    images = [[graph_data[i].filename for i in range(0, 4)], [graph_data[i].filename for i in range(4, 8)]]
    tweets = tweets_generator(data, images, input_data['Cases24H'])

    success_send_thread = send_thread(auth_data, tweets)
    if(success_send_thread == 1):
        print('Could not authenticate session and send tweets.')
        return 1
    
    success_tweets_export = export_tweets_to_file(tweets)
    if(success_tweets_export == 1):
        print('Could not reach tweets.dat')
        return 1

    clean_directory = clean_dir()
    if(clean_directory == 1):
        print('Could not clean raw_images directory. Exiting...')
        return 1

    if(sys.platform == 'win32'):
        update_git_repo_win32(input_data['Date'])
    else:
        update_git_repo_linux(input_data['Date'])

#####################################################################################################################

run()