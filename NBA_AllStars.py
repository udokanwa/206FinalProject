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
import csv
from distutils.filelist import findall
import matplotlib.pyplot as plt

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
def scrape_api_create_database(db_filename, cur, conn):

    #create connection and cursor to create database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    url = "https://api-nba-v1.p.rapidapi.com/standings"

    querystring1 = {"league":"standard","season":"2021"}
    querystring2 = {"league":"standard","season":"2020"}
    querystring3 = {"league":"standard","season":"2019"}
    querystring4 = {"league":"standard","season":"2018"}

    headers = {
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	"X-RapidAPI-Key": "13de0c56camsh01cfb982e13cb52p16fd63jsn251a208fbe5f"
    }

    response1 = requests.request("GET", url, headers=headers, params=querystring1)
    response2 = requests.request("GET", url, headers=headers, params=querystring2)
    response3 = requests.request("GET", url, headers=headers, params=querystring4)
    response4 = requests.request("GET", url, headers=headers, params=querystring4)

    info1 = json.loads(response1.text)
    info2 = json.loads(response2.text)
    info3 = json.loads(response3.text)
    info4 = json.loads(response4.text)
    ids = []
    teamnames= []
    conferences = []
    c_wins = []
    c_losses = []
    league_W_percs = []
    league_L_percs = []
    season = []
    for team in info1["response"]: 
        id = team["team"].get("id")
        teamname = team["team"].get("name")
        conference = team["conference"].get("name")
        c_win = team["conference"].get("win")
        c_loss = team["conference"].get("loss")
        league_W_perc = float(team["win"].get("percentage"))
        league_L_perc = float(team["loss"].get("percentage"))
        ids.append(id)
        teamnames.append(teamname)
        conferences.append(conference)
        c_wins.append(c_win)
        c_losses.append(c_loss)
        league_W_percs.append(league_W_perc)
        league_L_percs.append(league_L_perc)
        season.append(2021)
    
    for team in info2["response"]: 
        id = team["team"].get("id")
        teamname = team["team"].get("name")
        conference = team["conference"].get("name")
        c_win = team["conference"].get("win")
        c_loss = team["conference"].get("loss")
        league_W_perc = float(team["win"].get("percentage"))
        league_L_perc = float(team["loss"].get("percentage"))
        ids.append(id)
        teamnames.append(teamname)
        conferences.append(conference)
        c_wins.append(c_win)
        c_losses.append(c_loss)
        league_W_percs.append(league_W_perc)
        league_L_percs.append(league_L_perc)
        season.append(2020)
    
    for team in info3["response"]: 
        id = team["team"].get("id")
        teamname = team["team"].get("name")
        conference = team["conference"].get("name")
        c_win = team["conference"].get("win")
        c_loss = team["conference"].get("loss")
        league_W_perc = float(team["win"].get("percentage"))
        league_L_perc = float(team["loss"].get("percentage"))
        ids.append(id)
        teamnames.append(teamname)
        conferences.append(conference)
        c_wins.append(c_win)
        c_losses.append(c_loss)
        league_W_percs.append(league_W_perc)
        league_L_percs.append(league_L_perc)
        season.append(2019)
    
    for team in info4["response"]: 
        id = team["team"].get("id")
        teamname = team["team"].get("name")
        conference = team["conference"].get("name")
        c_win = team["conference"].get("win")
        c_loss = team["conference"].get("loss")
        league_W_perc = float(team["win"].get("percentage"))
        league_L_perc = float(team["loss"].get("percentage"))
        ids.append(id)
        teamnames.append(teamname)
        conferences.append(conference)
        c_wins.append(c_win)
        c_losses.append(c_loss)
        league_W_percs.append(league_W_perc)
        league_L_percs.append(league_L_perc)
        season.append(2018)

    cur.execute("DROP TABLE IF EXISTS Teams")
    cur.execute("CREATE TABLE Teams (id INTEGER, teamname TEXT, conference TEXT, c_win INTEGER, c_loss INTEGER, league_W_perc FLOAT, league_L_perc FLOAT, season INTEGER)")
    for i in range(len(ids)):
        cur.execute("INSERT INTO Teams (id, teamname, conference, c_win, c_loss, league_W_perc, league_L_perc, season) VALUES (?,?,?,?,?,?,?,?)",(ids[i], teamnames[i], conferences[i], c_wins[i], c_losses[i], league_W_percs[i], league_L_percs[i], season[i]))
    conn.commit()
    
     
'''
This function will create a database from the web scraping results for all star players
'''
def create_database(cur, conn):
    find = find_all_AllStars()
    allstarsdic = count_AllStarTeams(find)
    dic = {k: v for k, v in sorted(allstarsdic.items(), key=lambda item: item[1])}
    a = list(dic.keys())
    b = list(dic.values())
    cur.execute("DROP TABLE IF EXISTS allStars")
    cur.execute("CREATE TABLE allStars (name TEXT, num_allstarplayers INTEGER)")
    for i in range(len(dic.keys())):
        cur.execute("INSERT INTO allStars (name, num_allstarplayers) VALUES (?,?)",(a[i], b[i]))
    conn.commit()


'''
PHASE 2: PROCESSING THE DATA
'''

# This function uses JOIN to select the win/loss counts from each team by number of all stars that they have
def calcuate_WLRatio(cur,conn):
    tups = []
    cur.execute("SELECT allStars.name, allStars.num_allstarplayers, Teams.c_win, Teams.c_loss, Teams.season FROM Teams INNER JOIN allStars ON Teams.teamname=allStars.name")
    info = cur.fetchall()
    new = []
    for(a,b,c,d,g) in info:
        e = float("{:.2f}".format(float(c/52)))
        f = float("{:.2f}".format(float(d/52)))
        new.append((a,b,e,f,g))
    print(new)
    return new

# This function takes the list of tuples of W/L ratios and writes the calculated data into a CSV file
def create_CSV(csv_filename, new):
    path = os.path.dirname(os.path.abspath(__file__))
    path2 = path+'/'+csv_filename
    with open(path2, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Team Name", "Number of All Star Players", "Percentage of Conference Wins", "Percentage of Conference Losses", "Season"])
        for (a,b,e,f,g) in new:
            writer.writerow([a,b,e,f,g])

def findLeagueInfo(conn,cur):
    tups = []
    cur.execute("SELECT allStars.name, allStars.num_allstarplayers, Teams.league_W_perc, Teams.league_L_perc FROM Teams INNER JOIN allStars ON Teams.teamname=allStars.name")
    info = cur.fetchall()
    return info

# this function will create a boxplot of percentage conference wins for teams with different numbers of all star players
def boxplot_w(ratio):
    wins = []
    allstars = []
    for (name, num_allstar, w_ratio, l_ratio) in ratio:
        wins.append(w_ratio)
        allstars.append(num_allstar)

    plt.scatter(allstars, wins)
    plt.title("Number of All Star Players on a Team Versus its Percentage for Wins at Conference Level")
    plt.xlabel("Number of All Star Players on a Team")
    plt.ylabel("Percentage for Wins at Conference Level")
    plt.show()
    plt.clf()  

# this function will create a boxplot of percentage conference losses for teams with different numbers of all star players
def boxplot_l(ratio):
    losses = []
    allstars = []
    for (name, num_allstar, w_ratio, l_ratio) in ratio:
        losses.append(l_ratio)
        allstars.append(num_allstar)

    plt.scatter(allstars, losses)
    plt.title("Number of All Star Players on a Team Versus its Percentage for Losses at Conference Level")
    plt.xlabel("Number of All Star Players on a Team")
    plt.ylabel("Percentage for Losses at Conference Level")
    plt.show()
    plt.clf()

# this function will create all of our final visualizations using matplotlib
def histogram_w(new):
    wins = []
    allstars = []
    for (name, num_allstar, league_w, league_l) in new:
        wins.append(league_w)
        allstars.append(num_allstar)
    plt.barh(allstars, wins)
    plt.ylabel("Number of All Star Players on a Team")
    plt.xlabel("Percentage of League Games Won")
    plt.title('All Star Players on a Team Versus Percentage of League Games Won')
    plt.tight_layout
    plt.show()
    plt.clf()

def histogram_l(new):
    losses = []
    allstars = []
    for (name, num_allstar, league_w, league_l) in new:
        losses.append(league_l)
        allstars.append(num_allstar)
    plt.barh(allstars, losses)
    plt.ylabel("Number of All Star Players on a Team")
    plt.xlabel("Percentage of League Games Lost")
    plt.title('All Star Players on a Team Versus Percentage of League Games Lost')
    plt.tight_layout
    plt.show()
    plt.clf()



# call all of our functions here
def main():
    AllStarList = find_all_AllStars()
    TeamDict = count_AllStarTeams(AllStarList)
    path = os.path.dirname(os.path.abspath(__file__))
    conn1 = sqlite3.connect(path+'/'+"Teams.db")
    cur1 = conn1.cursor()
    scrape_api_create_database("Teams.db",cur1,conn1)
    conn2 = sqlite3.connect(path+'/'+"allStars.db")
    cur2 = conn2.cursor()
    create_database(cur2, conn2)
    calcuate_WLRatio(cur1,conn1)
    ratio = calcuate_WLRatio(cur1,conn1)
    create_CSV("winLossRatio.csv", ratio)
    boxplot_w(ratio)
    boxplot_l(ratio)
    new = findLeagueInfo(conn1,cur1)
    histogram_w(new)
    histogram_l(new)


if __name__ == '__main__':
    main()