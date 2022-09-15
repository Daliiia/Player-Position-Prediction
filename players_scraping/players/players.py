import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from countries.countries import Countries
from collections import defaultdict

class Players(Countries):
    def __init__(self):
        super(Players,self).__init__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()
    def pull_first_page(self,url):
        try:
            self.get(url)
            self.maximize_window()
        except Exception as e :
            print(e)
            return
        country_name=self.find_element(By.CSS_SELECTOR,'div[id="meta"] > div > h1 > span').text.split('Football')[0]
        print(country_name)
        a_elements=self.find_elements(By.CSS_SELECTOR,'div[class="section_content"] > p > a')
        p_elements=self.find_elements(By.CSS_SELECTOR,'div[class="section_content"] > p')
        links=[element.get_attribute('href') for element in a_elements]
        self.player_page(links,country_name)

    def player_page(self,links,country):
        dic=defaultdict(list)
        i=1
        self.maximize_window()
        for link in links:
            try:
                self.get(link)
                self.implicitly_wait(2)
            except:
                with open("missing_countries.txt", "a+") as file_object:
                    # Append 'hello' at the end of file
                    file_object.write(country)
                    file_object.write('\n')
                continue

            i+=1
            try:

                try:
                    dic['MP'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="games"] ').text)
                except:
                    dic['MP'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="games"] ').text)
                    dic['games_starts'].append(self.find_element(By.CSS_SELECTOR,
                                                                 'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="games_starts"] ').text)
                    dic['minutes'].append(self.find_element(By.CSS_SELECTOR,
                                                            'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="minutes"] ').text)
                    dic['goals'].append(self.find_element(By.CSS_SELECTOR,
                                                          'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="goals"] ').text)
                    dic['assists'].append(self.find_element(By.CSS_SELECTOR,
                                                            'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="assists"] ').text)
                    dic['goals_pens'].append(self.find_element(By.CSS_SELECTOR,
                                                               'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="goals_pens"] ').text)
                    dic['pens_made'].append(self.find_element(By.CSS_SELECTOR,
                                                              'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="pens_made"] ').text)
                    dic['pens_att'].append(self.find_element(By.CSS_SELECTOR,
                                                             'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="pens_att"] ').text)
                    dic['cards_yellow'].append(self.find_element(By.CSS_SELECTOR,
                                                                 'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="cards_yellow"] ').text)
                    dic['cards_red'].append(self.find_element(By.CSS_SELECTOR,
                                                              'table[id="stats_standard_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="cards_red"] ').text)
                    dic['cards_yellow_red'].append(self.find_element(By.CSS_SELECTOR,
                                                                     'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="cards_yellow_red"]').text)
                    dic['fouls'].append(self.find_element(By.CSS_SELECTOR,
                                                          'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="fouls"]').text)
                    dic['fouled'].append(self.find_element(By.CSS_SELECTOR,
                                                           'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="fouled"]').text)
                    dic['offsides'].append(self.find_element(By.CSS_SELECTOR,
                                                             'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="offsides"]').text)
                    dic['crosses'].append(self.find_element(By.CSS_SELECTOR,
                                                            'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="crosses"]').text)
                    dic['interceptions'].append(self.find_element(By.CSS_SELECTOR,
                                                                  'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="interceptions"]').text)
                    dic['tackles_won'].append(self.find_element(By.CSS_SELECTOR,
                                                                'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="tackles_won"]').text)
                    dic['pens_won'].append(self.find_element(By.CSS_SELECTOR,
                                                             'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="pens_won"]').text)
                    dic['pens_conceded'].append(self.find_element(By.CSS_SELECTOR,
                                                                     'table[id="stats_misc_dom_lg"] > tfoot > tr:nth-child(1) > td[data-stat="pens_conceded"]').text)
                    dic['main_info'].append(
                        self.find_element(By.CSS_SELECTOR, 'div[id="meta"]').text.replace('\n', ' '))
                    dic['country'].append(country)
                    continue
                dic['games_starts'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="games_starts"] ').text)
                dic['minutes'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="minutes"] ').text)
                dic['goals'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="goals"] ').text)
                dic['assists'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="assists"] ').text)
                dic['goals_pens'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="goals_pens"] ').text)
                dic['pens_made'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="pens_made"] ').text)
                dic['pens_att'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="pens_att"] ').text)
                dic['cards_yellow'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="cards_yellow"] ').text)
                dic['cards_red'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_standard_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="cards_red"] ').text)
                dic['cards_yellow_red'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="cards_yellow_red"]').text)
                dic['fouls'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="fouls"]').text)
                dic['fouled'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="fouled"]').text)
                dic['offsides'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="offsides"]').text)
                dic['crosses'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="crosses"]').text)
                dic['interceptions'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="interceptions"]').text)
                dic['tackles_won'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="tackles_won"]').text)
                dic['pens_won'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="pens_won"]').text)
                dic['pens_conceded'].append(self.find_element(By.CSS_SELECTOR,'table[id="stats_misc_nat_tm"] > tfoot > tr:nth-child(1) > td[data-stat="pens_conceded"]').text)
                dic['main_info'].append(self.find_element(By.CSS_SELECTOR, 'div[id="meta"]').text.replace('\n',' '))
                dic['country'].append(country)
            except Exception as e:
                print(e)
                print(link)
                continue
            print('i: '+ str(i))
            for key in dic.keys():
                print(len(dic[key]),end=' ')
        self.save_data(dic,country)

    def save_data(self,dic,country):
        players=pd.DataFrame(dic)
        # players_data=pd.read_csv(f'{country}_players.csv')
        # all_players=pd.concat([players_data,players],ignore_index=True,sort='False')
        players.to_csv(f'{country}Players.csv',index=False)




