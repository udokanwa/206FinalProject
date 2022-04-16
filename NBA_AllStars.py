from unicodedata import category
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import os
import sqlite3
import unittest
import json
import requests

# api key: a3bc00bd1408bda3382a2abe01b8eda2

# this function will gather data from the api  
def scrape_api(url):
    pass

# this function will gather data from the nba website and create a dictionary fo
def scrape_website():
    url = r"https://www.nba.com/news/2022-all-star-draft"
    pass

# this function will make the connector and cursor to naviagte our database and return them as well
def create_connector_cursor(db_filename):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()
    return cur, conn
     

# using data to create database
def create_database(data):
    info = json.loads(data)


# this function will create all of our final visualizations using matplotlib
def generate_graphs():
    pass


# call all of our functions here
def main():
