# Scrap 4

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time

df_loc = 0  # Index to fill the result DataFrame, row by row.
coin_df = pd.DataFrame(columns=('Shortcode', 'Name'))  # DF to be fill.

for page in range(1, 6):
    url = f'https://coinmarketcap.com/?page={page}'
    agent = UserAgent().random  # Use to generate a random header, different each time.
    headers = {'User-Agent': f'{agent}'}
    r = requests.get(url, headers)  # header to avoid access error.
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')

    # Entring step by step in HTML tree to get the coin name and code
    if soup.find(class_='h7vnx2-1 bFzXgL'):
        var = soup.find(class_='h7vnx2-1 bFzXgL')
        var = var.find('tbody')  # body with all currencies

        var = var.find_all('tr')  # list with all 'tr' tags. Each tr has info of one coin
    else:
        print('Sin clase: ')
        print(soup.prettify())

    for i in var:  # Go throw 'tr' list
        if i.find(class_='sc-16r8icm-0 escjiH'):  # First search
            aux = i.find(class_='sc-16r8icm-0 escjiH')
            aux = aux.find('a')
            coin_name = aux.find('p').string
            coin_code = aux.find(class_="sc-1eb5slv-0 gGIpIK coin-item-symbol").string

            aux_route = i.find('a')
            aux_route = aux_route.get('href')
            coin_url = f'https://coinmarketcap.com/{aux_route}'  # Specific coin_url
            agent = UserAgent().random
            headers = {'User-Agent': f'{agent}'}
            r_coin = requests.get(coin_url, headers)
            text = r_coin.text
            soup = BeautifulSoup(text, 'html.parser')

            var = soup.find('body')
            if var.find(class_='sc-16r8icm-0 gpRPnR nameHeader'):
                var = var.find(class_='sc-16r8icm-0 gpRPnR nameHeader')
                image64 = var.find('img')['src']  # route to image 64x64
                image200 = str(image64).replace('64x64', '200x200')  # url of image in 200x200

                img_data = requests.get(image200).content
                image_name = coin_name.lower() + '-' + coin_code.lower()
                with open(f'{image_name}.png', 'wb') as handler:  # Saving image
                    handler.write(img_data)

        elif i.find(class_="cmc-link"):  # Second search. The page change the class_ to avoid scrapping.
            aux = i.find(class_="cmc-link")
            aux = aux.find_all('span')
            coin_name = aux[1].string
            coin_code = aux[2].string

            aux_route = i.find(class_="cmc-link")
            aux_route = aux_route.get('href')
            coin_url = f'https://coinmarketcap.com/{aux_route}'  # coin_url
            agent = UserAgent().random
            headers = {'User-Agent': f'{agent}'}
            r_coin = requests.get(coin_url, headers)
            text = r_coin.text
            soup = BeautifulSoup(text, 'html.parser')

            var = soup.find('body')
            if var.find(class_="sc-1etv19d-2 fMHov"):
                var = var.find(class_="sc-1etv19d-2 fMHov")
                image64 = var['src']  # route to image 64x64
                image200 = str(image64).replace('64x64', '200x200')  # url of image in 200x200

                img_data = requests.get(image200).content
                image_name = coin_name.lower() + '-' + coin_code.lower()

                with open(f'{image_name}.png', 'wb') as handler:
                    handler.write(img_data)

        df_row = [coin_code, coin_name]
        coin_df.loc[df_loc] = df_row  # Fill fest_df, row by row, one row each time.
        df_loc = df_loc + 1

    time.sleep(10)  # Waiting time. Otherwise, the web collapse.

print(coin_df.shape)  # Check info.
coin_df.to_excel('coinmarketcap-collect-data 1 a 5.xlsx')  # Export to Excel.
