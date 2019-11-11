'''
Solution for Problem Set 6
This script scrapes tables from a set of Wikipedia pages and provides
a scatter plot as evidence of which of the two soccer leagues, the Bundesliga
or the Premier League, is more competitive
'''

# Import packages
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

# Start by collecting league tables for seasons 2010-11 through 2018-19 for the Bundesliga

# Create an empty dictionary to store all the columns from the league table
League_table_dict = {'Pos': [], 'Team': [], 'P': [], 'W': [], 'D': [], 'L': [], 'GF': [],
                        'GA': [], 'GD': [], 'Pts': [], 'Year': []}

yr_post = 11

for year in range(2010, 2019):
    time_link = str(year) + '-' + str(yr_post)
    wiki = "https://en.wikipedia.org/wiki/" + str(time_link) +"_Bundesliga"
    header = {'User-Agent': 'Mozilla/5.0'}
    
    req = urllib.request.Request(wiki,headers=header)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    
    # The pages for seasons 2017-18 and 2018-19 are structured slightly differently
    # The if statement below accounts for that

    if(year < 2017):
        table = soup.find_all("table",{"class":"wikitable"})[3]
    else:
        table = soup.find_all("table",{"class":"wikitable"})[4]
    
    i = 1
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if (len(cells) == 9) or (len(cells) == 10):
            League_table_dict['Team'].append(cells[0].findAll(text=True))
            League_table_dict['P'].append(cells[1].findAll(text=True))
            League_table_dict['W'].append(cells[2].find(text=True))
            League_table_dict['D'].append(cells[3].findAll(text=True))
            League_table_dict['L'].append(cells[4].find(text=True))
            League_table_dict['GF'].append(cells[5].find(text=True))
            League_table_dict['GA'].append(cells[6].find(text=True))
            League_table_dict['GD'].append(cells[7].find(text=True))
            League_table_dict['Pts'].append(cells[8].find(text=True))
            League_table_dict['Year'].append(time_link)
            if(i < 19):
                League_table_dict['Pos'].append(i)
                i = i+1
            else:
                i = 1
                League_table_dict['Pos'].append(i)
                i = i+1
    yr_post = yr_post + 1

# Convert the dictionary into a dataframe
BuLi_League_table_df = pd.DataFrame(League_table_dict)

# Clean up the Pts column and compute the average points per game for each time
# I use average points per game since a Bundesliga season has 34 games per team
# while a Premier League season has 38 games per team

BuLi_League_table_df = BuLi_League_table_df.replace('\n','', regex=True)
BuLi_League_table_df['Pts'] = BuLi_League_table_df['Pts'].astype(str).str.replace(",", "").astype(float)
BuLi_League_table_df['Avg.Pts'] = BuLi_League_table_df['Pts']/34

# Carry out the same process for Premier League seasons

League_table_dict = {'Pos': [], 'Team': [], 'P': [], 'W': [], 'D': [], 'L': [], 'GF': [],
                        'GA': [], 'GD': [], 'Pts': [], 'Year': []}
yr_post = 11

for year in range(2010, 2019):
    time_link = str(year) + '-' + str(yr_post)
    wiki = "https://en.wikipedia.org/wiki/" + str(time_link) +"_Premier_League"
    header = {'User-Agent': 'Mozilla/5.0'}
    
    req = urllib.request.Request(wiki,headers=header)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'lxml')
    
    table = soup.find_all("table",{"class":"wikitable"})[3]
    
    i = 1
    for row in table.findAll("tr"):
        cells = row.findAll("td")
        #For each "tr", assign each "td" to a variable.
        if (len(cells) == 9) or (len(cells) == 10):
            League_table_dict['Team'].append(cells[0].findAll(text=True))
            League_table_dict['P'].append(cells[1].findAll(text=True))
            League_table_dict['W'].append(cells[2].find(text=True))
            League_table_dict['D'].append(cells[3].findAll(text=True))
            League_table_dict['L'].append(cells[4].find(text=True))
            League_table_dict['GF'].append(cells[5].find(text=True))
            League_table_dict['GA'].append(cells[6].find(text=True))
            League_table_dict['GD'].append(cells[7].find(text=True))
            League_table_dict['Pts'].append(cells[8].find(text=True))
            League_table_dict['Year'].append(time_link)
            if(i < 21):
                League_table_dict['Pos'].append(i)
                i = i+1
            else:
                i = 1
                League_table_dict['Pos'].append(i)
                i = i+1
    yr_post = yr_post + 1

PL_League_table_df = pd.DataFrame(League_table_dict)

PL_League_table_df = pd.DataFrame(League_table_dict)
PL_League_table_df = PL_League_table_df.replace('\n','', regex=True)
PL_League_table_df['Pts'] = PL_League_table_df['Pts'].astype(str).str.replace(",", "").astype(float)
PL_League_table_df['Avg.Pts'] = PL_League_table_df['Pts']/38

# Plot the average number of points earned by each team in each league per season 

import matplotlib.pyplot as plt
import matplotlib.transforms as transforms

plt.figure()

# I perturb one set of points in order to make it easier to read the graph

offset = lambda p: transforms.ScaledTranslation(p/72.,0, plt.gcf().dpi_scale_trans)
trans = plt.gca().transData

plt.scatter(BuLi_League_table_df['Year'], BuLi_League_table_df['Avg.Pts'], color = 'red',
            label = "Bundesliga", transform=trans+offset(-5))
plt.scatter(PL_League_table_df['Year'], PL_League_table_df['Avg.Pts'],
            color = 'green', label = "Premier League")
plt.legend(loc='upper left')
plt.show()
