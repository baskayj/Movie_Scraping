import json
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup

#----------------------------------------------
API_KEY = "c7282170" #OMDb API KEY
url_part_1 = "http://www.omdbapi.com/?i="
url_part_2 = "&apikey="
#----------------------------------------------

df = pd.read_csv("joined_list.csv")

title_list = []
year_list = []
type_list = []
plot_list = []
ratings_list = []
awards_list = []

fail_counter = 0
for imdb_id in df.id:
    url_full = f"{url_part_1}{imdb_id}{url_part_2}{API_KEY}"
    uClient = urlopen(url_full)
    page_json = json.loads(BeautifulSoup(uClient.read(),"lxml", from_encoding="utf-8").text)   #Turns the html response into a json
    uClient.close()
    if page_json["Response"] == "True": #True is considered a string in the dict...
        title_list.append(page_json["Title"])
        year_list.append(page_json["Year"])
        type_list.append(page_json["Type"])
        plot_list.append(page_json["Plot"])
        ratings_list.append(page_json["imdbRating"])
        awards_list.append(page_json["Awards"])
    else:
        print(f"Error retrieving data for {imdb_id}")
        fail_counter += 1
        title_list.append("N/A")
        year_list.append("N/A")
        type_list.append("N/A")
        plot_list.append("N/A")
        ratings_list.append("N/A")
        awards_list.append("N/A")

df.insert(1,"Title",title_list)
df.insert(2,"Year",year_list)
df.insert(3,"Type",type_list)
df.insert(len(df.columns),"Plot",plot_list)
df.insert(len(df.columns),"Rating",ratings_list)
df.insert(len(df.columns),"Awards",awards_list)
df.to_csv("expanded_list.csv",index = False)
print(f"Total number of errors: {fail_counter}")

