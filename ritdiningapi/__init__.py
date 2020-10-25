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

@APP.route('/api/v1/open')
def _index():
    page = requests.get('https://www.rit.edu/fa/diningservices/places-to-eat/hours')
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    hours_divs = parsed_page.findAll('div', class_='view-places-to-eat')[0].find('div').findAll('div', recursive=False)
    hours = {}
    lastPlace = ''
    for div in hours_divs:
        if 'hours-title' in div.attrs['class']:
            lastPlace = div.text.strip()
            hours[lastPlace] = {}
        else:
            if hours[lastPlace].get('open') is not True and 'Closed' in div.text.strip():
                hours[lastPlace]['open'] = False
            else:
                text = div.text.strip()
                open = parser.parse(text.split(' ')[-3], ignoretz=True).astimezone(tz.gettz("America/New_York"))
                close = parser.parse(text.split(' ')[-1], ignoretz=True).astimezone(tz.gettz("America/New_York"))
                now = datetime.now(timezone.utc)
                if open < now < close:
                    hours[lastPlace]['open'] = True
    return jsonify(hours)
