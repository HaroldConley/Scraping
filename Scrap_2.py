# Scrap practice 2
import pandas as pd
import requests
from bs4 import BeautifulSoup

name = []       #Creation of empty list of data needed to create a DF
year = []       #
wins = []       #
losses = []     #
ot_losses = []  #
pct_wins = []   #
gf = []         #
ga = []         #
diff = []       #

for page in range(1,7):                                                                 #Loop to search in each one of the 6 pages of the website.
    url = f'https://www.scrapethissite.com/pages/forms/?page_num={page}&per_page=100'   #The url with the data. f'string' allows variable evaluation inside the string.
    r = requests.get(url)                                                               #Request the info to the url.
    soup = BeautifulSoup(r.text, 'html.parser')                                         #Info to html.

    all_teams = soup.find_all(class_='team')        #Create an object with all teams and their data.

    for j in all_teams:
        row = []                                    #Empty list for create a Team row.

        for i in j:                                 #Loop to strip empty elements and then append the 'real' values to the row list.
            if i != '\n':                               #
                row.append(i.text.strip())              #

        row_type = []                               #Empty list for create a clon of row list, but whit the correct type of values.

        for i in row:                                                                   #   Loop to:
            var_split = list(i)                                                             #       Generate a list with every letter/number/simbol of the text value.
            if var_split != [] and var_split[0] == '0':                                     #       Conditional to save the variable according to its type (str, int, float)
                val = float(i)                                                                  #
            elif i.isdigit():                                                                   #
                val = int(i)                                                                    #
            elif var_split != [] and var_split[0] == '-' and var_split[1] == 0:                 #Checking negative numbers
                val = float(i)                                                                  #
            elif var_split != [] and var_split[0] == '-' and var_split[1].isdigit():            #
                val = int(i)                                                                    #
            else:                                                                               #Else, it must be an string
                val = i                                                                         #
            row_type.append(val)        #Append the value (with its correct type) to row_type list.

        name.append(row_type[0])        #Append each value of row_type list to its correct list.
        year.append(row_type[1])            #
        wins.append(row_type[2])            #
        losses.append(row_type[3])          #
        ot_losses.append(row_type[4])       #
        pct_wins.append(row_type[5])        #
        gf.append(row_type[6])              #
        ga.append(row_type[7])              #
        diff.append(row_type[8])            #


teams_dict = {                      #Creation of Teams dictionary
    'Name': name,
    'Year': year,
    'Wins': wins,
    'Losses': losses,
    'Ot-losses': ot_losses,
    '% wins': pct_wins,
    'Gf': gf,
    'Ga': ga,
    'Diff': diff
}


teams_df = pd.DataFrame(teams_dict)     #Creation of teams DF
teams_df = teams_df.set_index('Name')   #Setting names as index
teams_df.to_csv('Teams.csv')            #Exporting the DF to CSV