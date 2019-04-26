import numpy as np
import pandas as pd
import bs4
import requests
import matplotlib.pyplot as plt
from math import pi
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum
import matplotlib.pyplot as plt

#function to obtain archetype, percent of game and win rate information, then use panda to put those data in a table
def getTable(url, index):
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    wrapper = soup.find("div", {"id": "wrapper"}, recursive = True)
    table = wrapper.findAll("table")[index]
    df = pd.read_html(str(table))[0]
    df = df.drop('#', 1)                            #eliminate the index column
    return df

## put all decks id of individual data into a list
def processData(data):
    ids = data['Deck #ID']
    decks = []
    for currId in ids:
        if(currId[0:-6] == ''):
            continue
        decks.append(currId[0:-6])
    return decks

## count number of each archetypes appearing in the individual rank
def getNum(archetype, decks):
    counts = []
    archelist = []
    sumCount = 0
    for arche in archetype:
        archelist.append(arche)
        count = 0
        for deck in decks:
            if deck == arche:
                count += 1
        counts.append(count)
        sumCount += count
    counts.append(len(decks) - sumCount)
    archelist.append('others')
    return archelist, counts

def horizontalBar(archelist, counts):
    # set values in tuples
    temp = list(zip(archelist, counts))
    #sort the values in tuples
    temp.sort(key=lambda tup: tup[1], reverse=False)
    archesort = []
    nums = []
    # get the sorted num
    for pair in temp:
        archesort.append(pair[0])
        nums.append(pair[1])
    y_pos = np.arange(len(archelist))
    # Create horizontal bars
    plt.barh(y_pos, nums)
    # Create names on the y-axis
    plt.yticks(y_pos, archesort)
    plt.show()

# plot the pie chart with given data
def pieChart(archelist,  counts):
    output_file("pie.html")
    sumValue = 0.0
    percentage = []
    for i in counts:
        sumValue += i
    for i in counts:
        percentage.append((i*100)/sumValue)
    ## sort the tuple list by second value
    temp = list(zip(archelist, percentage))
    temp.sort(key=lambda tup: tup[1], reverse=True)
    values = {
        temp[0][0]: temp[0][1],
        temp[1][0]: temp[1][1],
        temp[2][0]: temp[2][1],
        temp[3][0]: temp[3][1],
        temp[4][0]: temp[4][1],
        temp[5][0]: temp[5][1],
        temp[6][0]: temp[6][1],
        temp[7][0]: temp[7][1],
        temp[8][0]: temp[8][1],
        temp[9][0]: temp[9][1],
        temp[10][0]: temp[10][1],
        temp[11][0]: temp[11][1],
        temp[12][0]: temp[12][1],
        temp[13][0]: temp[13][1],
        temp[14][0]: temp[14][1],
        temp[15][0]: temp[15][1],
        temp[16][0]: temp[16][1],
        temp[17][0]: temp[17][1],
        temp[18][0]: temp[18][1],
        temp[19][0]: temp[19][1],
        temp[20][0]: temp[20][1],
    }
    # set colors of pie chart
    colors = Category20c[len(temp)-1]
    colors.append('#cdaef2')
    # set data, angle and color
    data = pd.Series(values).reset_index(name='percent').rename(columns={'index':'decks'})
    data['angle'] = data['percent']/100*2*pi
    data['color'] = colors
    p = figure(plot_width = 700, plot_height = 600, title="Percentage of Hearthstone Archetypes in top 154 winning decks", toolbar_location=None,
            tools="hover", tooltips="@decks: @percent%",  x_range=(-5, 8))
    p.wedge(x=0, y=1, radius=4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='decks', source=data)
    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    show(p, notebook_handle=True)

# main function 
def main():
    url = 'http://metastats.net/decks/winrate/'
    # ovearll archetype win rate, eliminate the index colum
    overallData = getTable(url, 0)   
    archetype = overallData['Archetype']
    # indiviudal archetype win rate, eliminate the last unamed row    
    individualData = getTable(url, 1)
    decks = processData(individualData)
    archelist, nums = getNum(archetype, decks)
    # plot the pie chart
    pieChart(archelist, nums)
    #plot the horizontal bar
    horizontalBar(archelist, nums) 

if __name__ == "__main__":
    main()