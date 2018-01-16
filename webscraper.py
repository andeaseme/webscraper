# http://www.gregreda.com/2013/03/03/web-scraping-101-with-python/

from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import os.path

BASE_URL = "http://www.chicagoreader.com"
JSON_FILE = "data.json"


def formatter(text):
    return text \
        .replace(u'\xa0', ' ') \
        .replace(u"\u2018", "'") \
        .replace(u"\u2019", "'")


def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")


def get_category_links(section_url):
    soup = make_soup(section_url)
    boccat = soup.find("dl", "boccat")
    category_links = [BASE_URL + dd.a["href"] for dd in boccat.findAll("dd")]
    return category_links


def get_category_winner(category_url):
    soup = make_soup(category_url)
    category = formatter(soup.find("h1", "headline").text)
    winner = [formatter(h2.text) for h2 in soup.findAll("h2", "boc1")]
    runners_up = [formatter(h2.text) for h2 in soup.findAll("h2", "boc2")]
    return {"category": category,
            "category_url": category_url,
            "winner": winner,
            "runners_up": runners_up}


if os.path.isfile(JSON_FILE):
    with open(JSON_FILE) as json_file:
        read_data = json.load(json_file)
    data = read_data
else:
    read_data = None
    data = {"wins": []}
best_food_drink_url = BASE_URL + '/chicago/best-of-chicago-2011-food-drink/BestOf?oid=4106228'
cat_links = get_category_links(best_food_drink_url)
i = 0
for link in cat_links:
    if read_data is None or not any(d["category_url"] == link for d in read_data["wins"]):
        cat_data = get_category_winner(link)
        print cat_data
        data["wins"].append(cat_data)
        i += 1
        if i > 20:
            break

with open(JSON_FILE, 'w') as json_file:
    json.dump(data, json_file)
