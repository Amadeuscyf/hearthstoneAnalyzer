import folium
import os
import pandas as pd
import bs4
import requests
import json

def getTable():
    url = 'https://www.esportsearnings.com/games/328-hearthstone/countries'
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    parser = soup.find('div', {'class': 'center_wrapper'})
    playerTable = parser.find('table', {'class': 'detail_list_table'}, recursive = True)
    df = pd.read_html(str(playerTable))[0]
    ## rename the table column
    df.columns = ['Rank', 'Country', 'Prize Money', '#Players']
    ## drop the rank column
    df = df.drop('Rank', 1)
    df = df.drop('Prize Money', 1)
    df = df[:-1]
    ## remove Players and players
    df['#Players'] = df['#Players'].apply(lambda x: x.replace(' Players', ''))
    df['#Players'] = df['#Players'].apply(lambda x: x.replace(' Player', ''))
    return df

## create dataframe and handle some difference between country name, turn all string number in players into int
def createDataFrame(df):
    countries = []
    players = []
    for i in range(0, len(df['Country'])):
        num = 0
        if df['Country'][i] == 'Palestinian Territory, Occupied':
            continue
        elif df['Country'][i] == 'Syrian Arab Republic':
            continue
        elif df['Country'][i] == 'Hong Kong':
            add = (int)(df['#Players'][i])
            players[0] += add
            continue
        elif df['Country'][i] == 'United States':
            countries.append('United States of America')
            num = (int)(df['#Players'][i])
            players.append(num)
        elif df['Country'][i] == 'Taiwan, Republic of China':
            countries.append('Taiwan')
            num = (int)(df['#Players'][i])
            players.append(num)
        elif df['Country'][i] == 'Korea, Republic of':
            countries.append('North Korea')
            num = (int)(df['#Players'][i])
            players.append(num)
        elif df['Country'][i] == 'Russian Federation':
            countries.append('Russia')
            num = (int)(df['#Players'][i])
            players.append(num)
        elif df['Country'][i] == 'Viet Nam':
            countries.append('Vietnam')
            num = (int)(df['#Players'][i])
            players.append(num)
        else:
            countries.append(df['Country'][i])
            num = (int)(df['#Players'][i])
            players.append(num)
    return countries, players

def plotMap(countries, players):
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    world_geo = requests.get(url).json()
    dat = pd.DataFrame(
        [countries, players],
        index=['Country', 'Players']
    ).T
    world_map = folium.Map(location=[44, -102], zoom_start=3)
    folium.Choropleth(
        geo_data= world_geo,
        name='choropleth',
        data=dat,
        columns=['Country', 'Players'],
        key_on='feature.properties.name',
        fill_color='Purples',
        fill_opacity=0.7,
        line_opacity=0.1,
        legend_name='#Players',
    ).add_to(world_map)
    folium.LayerControl().add_to(world_map)
    ## save the plot in a file
    world_map.save('player_distribution.html')


def main():
    playerData = getTable()
    countries, players = createDataFrame(playerData)
    plotMap(countries, players)

if __name__ == "__main__":
    main()
