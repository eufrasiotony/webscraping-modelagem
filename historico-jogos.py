import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

url = 'https://s5.sir.sportradar.com/bet365/en/1'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
script = soup.find_all('script')[0].text.strip()[69:-133]

datas = json.loads(script)

paises = datas['fetchedData']['config_tree_mini/41/0/1']['data']

codpaises = []

for pais in paises:
    for pai in pais['realcategories']:
        codpaises.append(pai['_id'])

teamsData = []

# não consegui superar erros consecutivos para esses países e optei por não usar dados históricos dos mesmos

for codpais in codpaises:

        if codpais in [304, 91, 852, 391, 388, 305, 914, 201, 19, 270, 542, 376, 500,
                       10, 329, 278, 163, 428, 512, 197, 85, 148, 291, 9, 155, 26,
                       385, 366, 296, 34, 351, 956, 102, 367, 938, 67, 339, 352,
                       393, 392, 805, 303, 540, 847, 951, 387, 310, 886, 421, 803,
                       485, 254, 824, 86, 299, 131]:
            continue

        url = f'https://s5.sir.sportradar.com/bet365/en/1/category/{codpais}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.find_all('script')[0].text.strip()[69:-133]

        datas = json.loads(script)


        campeonatos = datas['fetchedData'][f'config_tree_mini/41/0/1/{codpais}']['data']

        codcamps = []

        for camps in campeonatos:
            for camp in camps['realcategories']:
                for cam in camp['tournaments']:
                    codcamps.append(cam['currentseason'])


        principalcamp = codcamps[0]
        print(codpais)

        if codpais == 5:
            principalcamp = 83706
        url = f'https://s5.sir.sportradar.com/bet365/en/1/season/{principalcamp}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.find_all('script')[0].text.strip()[69:-133]

        datas = json.loads(script)

        teams = datas['fetchedData'][f'stats_formtable/{principalcamp}']['data']['teams']


        for team in teams:
            for match in team['form']['total']:
                teamsData.append(match['matchid'])
            for match in team['form']['away']:
                teamsData.append(match['matchid'])
            for match in team['form']['home']:
                teamsData.append(match['matchid'])


newteamsData = []
for element in teamsData:
    if element not in newteamsData:
        newteamsData.append(element)

print('OS IDPARTIDAS FORAM GERADOS')

stats_final = []

for partida in newteamsData:
    url = f'https://s5.sir.sportradar.com/bet365/en/1/season/84048/gamecast/{partida}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[0].text.strip()[69:-133]

    datas = json.loads(script)

    if partida == 33251599:
        continue

    homeid = datas['fetchedData'][f'stats_match_get/{partida}']['data']['teams']['home']['uid']


    hometeam = datas['fetchedData'][f'stats_match_get/{partida}']['data']['teams']['home']['mediumname']
    scorehome = datas['fetchedData'][f'stats_match_get/{partida}']['data']['result']['home']
    awayid = datas['fetchedData'][f'stats_match_get/{partida}']['data']['teams']['away']['uid']
    awayteam = datas['fetchedData'][f'stats_match_get/{partida}']['data']['teams']['away']['mediumname']
    scoreaway = datas['fetchedData'][f'stats_match_get/{partida}']['data']['result']['away']



    stats = datas['parsedData']['matchStatistics'][f'{partida}']['statistics']['values']

# crio as variáveis dependentes dos modelos estatisticos 

    if len(stats) != 12:
        continue

    flag_gol0 = 0
    flag_gol0 = 1


    gols = scorehome + scoreaway

    if gols >= 1:
        flag_gol0 = 1
    else:
        flag_gol0 = 0
    if gols >= 2:
        flag_gol1 = 1
    else:
        flag_gol1 = 0

# seleciono as variáveis dos jogos

    match_stats = {
        'homeid': homeid,
        'hometeam': hometeam,
        'scorehome': scorehome,
        'awayid': awayid,
        'awayteam': awayteam,
        'scoreaway': scoreaway,
        'gols': gols,
        'flag_gol0': flag_gol0,

        'idpartida': partida
    }

    for stat in stats:
        match stat['name']:
            case 'Ball possession':
                match_stats['ball_possession_home'] = stat['value']['home']
                match_stats['ball_possession_away'] = stat['value']['away']
            case 'Goal attempts':
                match_stats['goalattempts_home'] = stat['value']['home']
                match_stats['goalattempts_away'] = stat['value']['away']
            case 'Shots on target':
                match_stats['shots_on_target_home'] = stat['value']['home']
                match_stats['shots_on_target_away'] = stat['value']['away']
            case 'Shots off target':
                match_stats['shots_off_target_home'] = stat['value']['home']
                match_stats['shots_off_target_away'] = stat['value']['away']
            case 'Corner kicks':
                match_stats['corner_kicks_home'] = stat['value']['home']
                match_stats['corner_kicks_away'] = stat['value']['away']
            case 'Free kicks':
                match_stats['free_kicks_home'] = stat['value']['home']
                match_stats['free_kicks_away'] = stat['value']['away']
            case 'Goal kicks':
                match_stats['goal_kicks_home'] = stat['value']['home']
                match_stats['goal_kicks_away'] = stat['value']['away']
            case 'Throw-ins':
                match_stats['throw_ins_home'] = stat['value']['home']
                match_stats['throw_ins_away'] = stat['value']['away']
            case 'Yellow cards':
                match_stats['yellow_cards_home'] = stat['value']['home']
                match_stats['yellow_cards_away'] = stat['value']['away']
            case 'Saves':
                match_stats['saves_home'] = stat['value']['home']
                match_stats['saves_away'] = stat['value']['away']
            case 'Fouls':
                match_stats['fouls_home'] = stat['value']['home']
                match_stats['fouls_away'] = stat['value']['away']

    stats_final.append(match_stats)

stats_final = pd.DataFrame(stats_final)
stats_final.to_csv('historico-jogos.csv', index=False)

