# Scrap 3: Festivals

import requests
from bs4 import BeautifulSoup
import pandas as pd

df_loc = 0 #Index to fill the result DataFrame, row by row.
fest_df = pd.DataFrame(columns=('Name', 'Contact First Name', 'Contact Last Name', 'Street Address', 'City', 'Country', 'Zip', 'Phone', 'Contact Email', 'Website', 'Festival Months'))

for p in range(1,21): #For pages 1 to 20
    page = p
    url = f'https://www.midatlanticarts.org/grants-programs/international-festivals/results/page/{page}/?fest_name&city&zip&country&month&disciplines=ethnicfolk-inspired%2Cjazz'
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}) #header to avoid acces error.
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    links = soup.find_all(class_='link-more') #List with all links of festivals in THAT page.


    for link in range(0,10): #Loop to look the info, link by link.
        df_row = []
        df_row_aux = []
        url_fest = links[link].get('href')
        r = requests.get(url_fest, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}) #Going to the festival link.
        text = r.text
        soup = BeautifulSoup(text, 'html.parser')
        fest_data = soup.find_all('section')
        fest_data = fest_data[0] #Element with the info I need of one festival.

        fest_name = fest_data.find('h3').text #Fill the df_row with Fest name
        df_row_aux.append(fest_name)

        fest_elements = fest_data.find_all('li') #List with other elements
        for i in fest_elements:
            element = i.text #Element to iterate to get every data I need
            while element[0] != ':':
                element = element.lstrip(str(element[0])) #To clean the info before the ':'
            element = element.lstrip(str(element[0])) #To clear the ':'
            element = element.lstrip(str(element[0])) #To clear the white space before the info.
            df_row_aux.append(element)


        fest_date = fest_data.find('p').text #Fill the df_row with Fest date
        while fest_date[0] != ':':
            fest_date = fest_date.lstrip(str(fest_date[0]))  # To clean the info before the ':'
        fest_date = fest_date.lstrip(str(fest_date[0]))  # To clear the ':'
        fest_date = fest_date.lstrip(str(fest_date[0]))  # To clear the white space before the info.
        df_row_aux.append(fest_date)

        first_name = ''
        last_name = ''
        if df_row_aux[1] != '': #If statement to separate the full_name in First and Last name, checking if both names exist.
            full_name = df_row_aux[1]
            while full_name[0] != ' ':
                first_name = first_name + str(full_name[0]) #Get First name
                full_name = full_name.lstrip(str(full_name[0]))
                if full_name == '':
                    break
            if full_name == '':
                last_name = ''
            else:
                full_name = full_name.lstrip(str(full_name[0])) #Clean empty space
                last_name = full_name #Get last name

        df_row.append(df_row_aux[0]) #Filling final df_row with Fest name.
        df_row.append(first_name) #Fill df_row with first...
        df_row.append((last_name)) #... and last name.
        for i in range(2,len(df_row_aux)): #Filling the df_row with other data.
            df_row.append(df_row_aux[i])

        fest_df.loc[df_loc] = df_row #Fill fest_df with one row.
        df_loc = df_loc + 1


#For page 21. It's a little different (only change is number of links in the page) because it has only 7 links, no 10 like other pages.
page = 21
url = f'https://www.midatlanticarts.org/grants-programs/international-festivals/results/page/{page}/?fest_name&city&zip&country&month&disciplines=ethnicfolk-inspired%2Cjazz'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}) #header to avoid acces error.
text = r.text
soup = BeautifulSoup(text, 'html.parser')
links = soup.find_all(class_='link-more') #List with all links of festivals in THAT page.


for link in range(0,7):
    df_row = []
    df_row_aux = []
    url_fest = links[link].get('href')
    r = requests.get(url_fest, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'}) #Going to the festival link.
    text = r.text
    soup = BeautifulSoup(text, 'html.parser')
    fest_data = soup.find_all('section')
    fest_data = fest_data[0] #Element with the info I need

    fest_name = fest_data.find('h3').text #Fill the df_row with Fest name
    df_row_aux.append(fest_name)

    fest_elements = fest_data.find_all('li') #List with other elements
    for i in fest_elements:
        element = i.text #Element to iterate to get every data I need
        while element[0] != ':':
            element = element.lstrip(str(element[0])) #To clean the info before the ':'
        element = element.lstrip(str(element[0])) #To clear the ':'
        element = element.lstrip(str(element[0])) #To clear the white space before the info.
        df_row_aux.append(element)


    fest_date = fest_data.find('p').text #Fill the df_row with Fest date
    while fest_date[0] != ':':
        fest_date = fest_date.lstrip(str(fest_date[0]))  # To clean the info before the ':'
    fest_date = fest_date.lstrip(str(fest_date[0]))  # To clear the ':'
    fest_date = fest_date.lstrip(str(fest_date[0]))  # To clear the white space before the info.
    df_row_aux.append(fest_date)

    first_name = ''
    last_name = ''
    if df_row_aux[1] != '':
        full_name = df_row_aux[1]
        while full_name[0] != ' ':
            first_name = first_name + str(full_name[0]) #Get First name
            full_name = full_name.lstrip(str(full_name[0]))
        full_name = full_name.lstrip(str(full_name[0])) #Clean empty space
        last_name = full_name #Get last name

    df_row.append(df_row_aux[0]) #Filling final df_row
    df_row.append(first_name)
    df_row.append((last_name))
    for i in range(2,len(df_row_aux)):
        df_row.append(df_row_aux[i])

    fest_df.loc[df_loc] = df_row #Fill fest_df
    df_loc = df_loc + 1

print(fest_df.shape)
fest_df.to_excel('Jazz_Festival.xlsx')
