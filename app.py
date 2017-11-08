#!/usr/bin/python3

####my code ######

from flask import Flask, request, jsonify, send_from_directory, g, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import sqlite3
import re
import urllib
import requests
from bs4 import BeautifulSoup
import csv
import codecs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__, static_url_path='')
api = Api(app)

@app.route('/')
def root():
    return app.send_static_file('index.html')


class Tasks(Resource):
    def get(self, query):

        result = baseline_representation(query)
        return jsonify(result)


api.add_resource(Tasks, '/api/v1.0/<query>')


def baseline_representation(query):
    """This method is the simplest, we take the first result from searching the query on from the Wikihow.
       Then the subheadings of the page are scraped to create the subtasks.
    """
    task_dict = {}
    sub_tasks = []

    query =  query.lower()
    query = query.split(" ")
    query = ("+").join(query)
    search_url = "https://www.wikihow.com/wikiHowTo?search=" + query
    #print(search_url)
    htmlfile = urllib.request.urlopen(search_url)
    html = BeautifulSoup(htmlfile.read(), "html.parser") 
    title = html.find_all("div", {"class": "firstHeading"})
    search_page = html.find_all("a", {"class": "result_link"})
    #print(search_page)
    #print(search_page[0].text) # add to dict for json request
    #get sub-tasks
    if len(search_page) == 0:
        task_dict = "Sorry no results"
    else:
        top_link = search_page[0]
        soup = BeautifulSoup(str(top_link))
        for a in soup.find_all('a', href=True):
            link = a['href']
        link = "https:" + link
        #print("https:" + link)
        article = urllib.request.urlopen(link)
        article_soup = BeautifulSoup(article)
        sub = article_soup.find_all("b", {"class": "whb"})
        for tx in sub:
            sub_tasks.append(tx.text)

        task_dict[search_page[0].text] = sub_tasks
    return task_dict


if __name__ == '__main__':
     app.run()

     
