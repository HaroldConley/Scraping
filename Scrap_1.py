# Scrap practice

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.scrapethissite.com/pages/simple/'    #The url with the data.
r = requests.get(url)                                   #Request the info to the url.
text = BeautifulSoup(r.text, 'html.parser')             #Info to html.

def list_creator (class_type):
    c0 = text.find_all(class_=class_type)   #A list with all class_type elements in the URL, but not in a proper format.
    result_list = []                        #Empty list
    for i in c0:                            #Loop to create a list of class_type elements, in a proper format.
        result_list.append(i.text.strip())  #Strip eliminate all the spaces.
    return result_list

countries = list_creator('country-name')
capitals = list_creator('country-capital')
pop = list_creator('country-population')    #Data as string.
area = list_creator('country-area')         #Data as string.

pop_float = []                  #Convert data to int.
for i in pop:                   #
    pop_float.append(int(i))    #Convert data to int.


area_float = []                  #Convert data to float.
for i in area:                   #
    area_float.append(float(i))  #Convert data to float.


data = {                        #Create a dictionary called 'data'.
    'Country': countries,
    'Capital': capitals,
    'Population': pop_float,
    'Area [km2]': area_float
}

Country_info = pd.DataFrame(data)                   #Create a DataFrame from 'data' dictionary.
Country_info = Country_info.set_index('Country')    #Set country name as Index.
country_pop = Country_info.sort_values('Population', ascending=True)    #Dataframe sorted by Population.
print('\nTen countries with less population: ')
print(country_pop.Population.iloc[0:10])
print('\nTen countries with more population: ')
print(country_pop.Population.iloc[-10:])