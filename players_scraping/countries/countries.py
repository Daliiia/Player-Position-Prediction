import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import constants as const
import pandas as pd
import os

class Countries(webdriver.Firefox):
    def __init__(self,driver_path=const.PATH):
        self.driver_path=driver_path
        options=webdriver.ChromeOptions()
        options.add_argument('--disable-browser-side-navigation')
        os.environ['PATH']+=self.driver_path
        super(Countries,self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def land_first_page(self):
        self.get(const.DATA_URL)
        self.maximize_window()
        self.implicitly_wait(5)

    def pull_countries_data(self):
        abbreviation=[]
        player_count=[]
        links=[]
        for abbrev in self.find_elements(By.CSS_SELECTOR,'td[data-stat="governing_body"]'):
            abbreviation.append(abbrev.text)
        for player_cnt in self.find_elements(By.CSS_SELECTOR,'td[data-stat="player_count"]'):
            player_count.append(player_cnt.text)
        for link in self.find_elements(By.CSS_SELECTOR,'td[data-stat="player_count"] > a'):
            links.append(link.get_attribute('href'))
        print(len(abbreviation))
        print(len(player_count))
        self.save_to_csv(abbreviation,player_count,links)

    def save_to_csv(self,abbrev,player_count,links):

        data=pd.DataFrame({
            'abbrev':abbrev,
            'player_count': player_count,
            'link':links
        })
        data.to_csv('countries.csv',index=False)


