from bs4 import BeautifulSoup
import requests
import pandas as pd
from re import search 

def get_anime_data(max):
    URLS = []
    amount = 0
    while amount < max:
        URL = 'https://myanimelist.net/topanime.php?type=bypopularity&limit=' + str(amount)
        site = BeautifulSoup(requests.get(URL).text, 'lxml')
        data_stack = site.find_all('h3', class_='hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3')
        for data in data_stack:
            URLS.append(data.find('a').get("href"))
        amount += 50
    print("Found " + str(len(URLS)) + ' animes')
    print('Starting web-scraping')

    amount = 0
    dic_title = []
    dic_description = []
    dic_type = []
    dic_episodes = []
    dic_source = []
    dic_genres = []
    dic_themes = []
    dic_demographic = []
    dic_rating = []

    while amount < len(URLS):
        
        temp_genres = []
        temp_themes = []
        temp_demographic = []

        URL = URLS[amount]
        site = BeautifulSoup(requests.get(URL).text, 'lxml')
        temp_title = site.find('h1', class_='title-name h1_bold_none').text
        temp_description = site.find('p', attrs={"itemprop": "description"}).text
        data_stack = site.find_all('div', class_='spaceit_pad')
        for data in data_stack:
            if search("Type", data.text):
                x = data.find_all('a')
                for dataa in x:
                    temp_type = dataa.text
            if search("Episodes", data.text):
                temp_episodes = data.text.replace('\nEpisodes:\n  ','').replace('\n  ','')
            if search("Source", data.text):
                temp_source = data.text.replace('\nSource:\n  ','').replace('\n  ','')
            if search("Genres", data.text):
                x = data.find_all('a')
                for dataa in x:
                    temp_genres.append(dataa.text)
            if search("Themes", data.text):
                x = data.find_all('a')
                for dataa in x:
                    temp_themes.append(dataa.text)
            if search("Theme", data.text):
                x = data.find_all('a')
                for dataa in x:
                    temp_themes.append(dataa.text)
            if search("Demographic", data.text):
                x = data.find_all('a')
                for dataa in x:
                    temp_demographic.append(dataa.text)
            if search("Rating", data.text):
                temp_rating = data.text.replace('\nRating:\n  ','').replace('\n  ','')
        dic_title.append(temp_title)
        dic_description.append(temp_description)
        dic_type.append(temp_type)
        dic_episodes.append(temp_episodes)
        dic_source.append(temp_source)
        dic_genres.append(str(temp_genres).replace('[','').replace(']',''))
        dic_themes.append(str(temp_themes).replace('[','').replace(']',''))
        dic_demographic.append(str(temp_demographic).replace('[','').replace(']',''))
        dic_rating.append(temp_rating)
        amount += 1
        if amount%10 == 0:
            print("I'm working")

    df = pd.DataFrame({'Title':dic_title,'Description':dic_description,'Type':dic_type,'Episodes':dic_episodes,'Source':dic_source,'Genres':dic_genres,'Themes':dic_themes,'Demographic':dic_demographic,'Rating':dic_rating})
    return df 