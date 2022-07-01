import requests
import pandas as pd

url = 'https://v3.football.api-sports.io/leagues'
API_key = 'd7844ef5e66e21f4ecc1ff774a9e0e97'
headers = {
  'x-rapidapi-key': API_key
  }
r = requests.get(url, headers=headers)
text = r.json()
leagues = text['response']

leagues_df = pd.DataFrame(columns=('League_id', 'League_Name', 'Year', 'Top_Scorer', 'Age', 'Goals'))  # DF to be fill.
df_loc = 0
for i in leagues:
  for j in i['seasons']:
    if j['coverage']['top_scorers']: #To fill the DF only with leagues with top scorers
      l_id = i['league']['id']
      l_name = i['league']['name']
      l_year = j['year']
      url = f'https://v3.football.api-sports.io/players/topscorers?season={l_year}&league={l_id}' #URL to ask for top scorer of a league and season
      r = requests.get(url, headers=headers)
      text = r.json()
      top_score = text['response']
      for k in top_score:
        player = k['player']['name']
        age = k['player']['age']
        goals = k['statistics'][0]['goals']['total']
        row = [l_id, l_name, l_year, player, age, goals]
        leagues_df.loc[df_loc] = row
        df_loc = df_loc + 1
print(leagues_df)
leagues_df.to_excel('leagues.xlsx')  # Export to Excel.