from turtle import bgcolor
from unicodedata import category
from unittest.mock import NonCallableMagicMock
from bs4 import BeautifulSoup
import os
import sqlite3
import unittest
import json
import requests
import unidecode

# Reasearch Question: How does the number of All Stars on an NBA team affect the team's regular season performace?

'''
PHASE 1: GATHERING DATA AND STORING INTO DATABASE
'''
# This function will find all of the current active NBA All Stars in the NBA

def find_all_AllStars():
    url = r"https://en.wikipedia.org/wiki/List_of_NBA_All-Stars"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tag = soup.find_all('table')[1]
    player_list = []
    table = tag.find('tbody')
    for tr in table.find_all('tr'):
        player = tr.find("span")
        if player == None or tr.find('td').get("bgcolor") != "#CFECEC":
            continue
        else:
            name = unidecode.unidecode(player.find('a').getText())
            player_list.append(name)
    # To account for 2 players who are still in the NBA but inactive in the 20-21 season, Marc Gasol and Jeff Teague
    player_list.remove("Marc Gasol")
    player_list.remove("Jeff Teague")
    # 69 Active All-Stars
    return player_list

# returns a dictionary with the number of All Stars on each NBA team (if there's more than 0)
def count_AllStarTeams(player_list):
    url = r"https://basketball.realgm.com/nba/players"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    team_dict = {}
    table = soup.find('tbody')
    for tr in table.find_all('tr'):
        player = tr.find_all('a')[0].getText()
        if player in player_list:
            team = tr.find_all('a')[1].getText()
            if team not in team_dict:
                team_dict[team] = 1
            else:
                team_dict[team] += 1
    print(team_dict)
    return team_dict

# this function will gather data about each team from the api and create a database from it  
def scrape_api_create_database(db_filename):

    #create connection and cursor to create database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    url = "https://api-nba-v1.p.rapidapi.com/standings"

    querystring = {"league":"standard","season":"2021"}

    headers = {
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	"X-RapidAPI-Key": "13de0c56camsh01cfb982e13cb52p16fd63jsn251a208fbe5f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    info = json.loads(response.text)
    count = 0
    while count < 10:
        for team in info["response"]: 
            id = team["team"].get("id")
            teamname = team["team"].get("name")
            conference = team["conference"].get("name")
            C_win = team["conference"].get("win")
            C_loss = team["conference"].get("loss")
            league_W_perc = float(team["win"].get("percentage"))
            league_L_perc = float(team["loss"].get("percentage"))
            count += 1


    
     
'''
This function will use the collection data to create database with each team, their number of AllStars, 
and their season statistics. This database should be organized by number of All Stars on each team.
'''
def create_database(data, team_dict, cur, conn):

    pass

'''
PHASE 2: PROCESSING THE DATA
'''

# This function uses JOIN to select the win/loss counts from each team by number of all stars that they have
def calcuate_WLRatio():
    pass

# This function takes the list of tuples of W/L ratios and writes the calculated data into a CSV file
def create_CSV():
    pass



# call all of our functions here
def main():
    AllStarList = find_all_AllStars()
    TeamDict = count_AllStarTeams(AllStarList)
    scrape_api_create_database("AllStars.db")

if __name__ == '__main__':
    main()