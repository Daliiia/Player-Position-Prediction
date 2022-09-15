# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from countries.countries import Countries
from players.players import Players
import pandas as pd


with Countries() as bot:
    bot.land_first_page()
    bot.pull_countries_data()


countries_data=pd.read_csv('countries.csv')
urls=countries_data['link']

for url in urls:
    with Players() as bot:
        bot.pull_first_page(url)
