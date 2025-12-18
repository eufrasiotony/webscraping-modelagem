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
nextmatches = []
for codpais in codpaises:

        if codpais in [304, 91, 852, 391, 388, 305, 914, 201, 19, 270, 542,
                       10, 329, 278, 163, 428, 512, 197, 85, 148, 291, 9, 155,
                       26, 385, 366, 48, 99, 8, 47, 22, 322, 14, 393, 12, 353,
                       376, 17, 97, 33, 158, 78, 102, 18, 367, 1, 252, 7, 30,
                       122, 938, 365, 437, 11, 368, 66, 31, 279, 386, 790, 35,
                       389, 130, 44, 77, 21, 152, 23, 24, 32, 25, 485, 46, 254,
                       131]:
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

            if team['nextopponent'] == '[]' or team['nextopponent'] == []:
                continue
            nextmatche = {
                            'hometeam': team['team']['uid'],
                            'homeid': team['team']['mediumname'],
                            'nextid': team['nextopponent']['team']['uid'],
                            'teamnext': team['nextopponent']['team']['mediumname']
            }

            nextmatches.append(nextmatche)

newteamsData = []

for element in teamsData:
    if element not in newteamsData:
        newteamsData.append(element)

newnextmatches = []
for element in nextmatches:
    if element not in newnextmatches:
        newnextmatches.append(element)

newnextmatches = pd.DataFrame(newnextmatches)
newnextmatches.to_csv('nextgames.csv', index=False)

