from turtle import bgcolor
from unicodedata import category
from unittest.mock import NonCallableMagicMock
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import sqlite3
import unittest
import json
import requests
import re

# Reasearch Question: How does the number of All Stars on an NBA team affect the team's season performace?

# this function will find all of the current active NBA All Stars in the NBA

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
            name = player.find('a').getText()
            player_list.append(name)
    print(player_list)
    print(len(player_list))
    return player_list

# returns a dictionary with the number of AllStars on each NBA team (if there's more than 0)
def count_AllStarTeams(player_list):
    url = "https://basketball.realgm.com/nba/players"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

# this function will gather data about each team from the api  
def scrape_api(url):
    pass
    
# this function will make the connector and cursor to naviagte our database and return them as well
def create_connector_cursor(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    return cur, conn
     
'''
This function will use the collection data to create database with each team, their number of AllStars, 
and their season statistics. This database should be organized by number of All Stars on each team.
'''
def create_database(data):
    #info = json.loads(data)
    pass


# this function will create all of our final visualizations using matplotlib
def generate_graphs():
    pass


# call all of our functions here
def main():
    AllStarList = find_all_AllStars()
    TeamDict = count_allStarNum(AllStarList)

if __name__ == '__main__':
    main()