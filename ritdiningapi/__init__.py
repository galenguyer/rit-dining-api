""" A small flask Hello World """

from dateutil import parser, tz
from datetime import *
import os
import subprocess
import requests

from flask import Flask, jsonify
from bs4 import BeautifulSoup

APP = Flask(__name__)

# Load file based configuration overrides if present
if os.path.exists(os.path.join(os.getcwd(), 'config.py')):
    APP.config.from_pyfile(os.path.join(os.getcwd(), 'config.py'))
else:
    APP.config.from_pyfile(os.path.join(os.getcwd(), 'config.env.py'))

APP.secret_key = APP.config['SECRET_KEY']

def get_open(text):
    text = text.strip()
    if 'Closed' in text:
        return False
    else:
        open = parser.parse(text.split(' ')[-3], ignoretz=True).astimezone(tz.gettz("America/New_York"))
        close = parser.parse(text.split(' ')[-1], ignoretz=True).astimezone(tz.gettz("America/New_York"))
        now = datetime.now(timezone.utc)
        return open < now < close


@APP.route('/api/v1/open')
def _api_v1_open():
    page = requests.get('https://www.rit.edu/fa/diningservices/places-to-eat/hours')
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    hours_divs = parsed_page.findAll('div', class_='view-places-to-eat')[0].find('div').findAll('div', recursive=False)
    hours = {}
    lastPlace = ''
    hours['Artesano Bakery and Cafe'] = { 
        'open': get_open(hours_divs[1].text) 
    }
    hours['Beanz'] = { 
        'open': get_open(hours_divs[3].text) 
    }
    hours['Ben & Jerry\'s'] = { 
        'open': get_open(hours_divs[5].text) 
    }
    hours['Brick City Cafe'] = { 
        'open': get_open(hours_divs[7].text) or get_open(hours_divs[8].text) or get_open(hours_divs[9].text),
        'Breakfast': get_open(hours_divs[7].text),
        'Lunch': get_open(hours_divs[7].text),
        'Dinner': get_open(hours_divs[9].text) }
    hours['Bytes'] = {
        'open': get_open(hours_divs[11].text)
    }
    hours['Cafe and Market at Crossroads'] = {
        'open': get_open(hours_divs[13].text) or get_open(hours_divs[14].text),
        'Cafe': get_open(hours_divs[13].text),
        'Market': get_open(hours_divs[14].text)
    }
    hours['The College Grind'] = {
        'open': get_open(hours_divs[16].text)
    }
    hours['The Commons'] = {
        'open': get_open(hours_divs[18].text) or get_open(hours_divs[19].text),
        'Lunch': get_open(hours_divs[18].text),
        'Dinner': get_open(hours_divs[19].text)
    }
    hours['The Corner Store'] = {
        'open': get_open(hours_divs[21].text) or get_open(hours_divs[22].text),
        'Breakfast/Lunch': get_open(hours_divs[21].text),
        'Dinner': get_open(hours_divs[22].text)
    }
    hours['Ctrl Alt DELi'] = {
        'open': get_open(hours_divs[24].text)
    }
    hours['Global Village Cantina and Grille'] = {
        'open': get_open(hours_divs[26].text)
    }
    hours['Gracie\'s'] = {
        'open': get_open(hours_divs[30].text) or get_open(hours_divs[31].text) or get_open(hours_divs[32].text) or get_open(hours_divs[33].text),
        'Breakfast': get_open(hours_divs[31].text),
        'Lunch/Brunch': get_open(hours_divs[32].text),
        'Quick Service': get_open(hours_divs[33].text),
        'Dinner': get_open(hours_divs[30].text)
    }
    hours['Java Wally\'s'] = {
        'open': get_open(hours_divs[35].text)
    }
    hours['The Market at Global Village'] = {
        'open': get_open(hours_divs[37].text)
    }
    hours['Midnight Oil'] = {
        'open': get_open(hours_divs[39].text)
    }
    hours['Nathan\'s Soup and Salad'] = {
        'open': get_open(hours_divs[41].text)
    }
    hours['RITz Sports Zone'] = {
        'open': get_open(hours_divs[43].text)
    }
    hours['Sol\'s Underground'] = {
        'open': get_open(hours_divs[45].text)
    }
    return jsonify(hours)
