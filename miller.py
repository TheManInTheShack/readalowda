# ==============================================================================
# Miller
# Processes the churn
# 0.1 - Basic workflow
#   [ ] - 
#   [ ] - 
# ==============================================================================

# ------------------------------------------------------------------------------
# Import
# ------------------------------------------------------------------------------
from datetime import datetime
import io
import os
import sys
import argparse
import shutil
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# import requests


# ------------------------------------------------------------------------------
# Init
# ------------------------------------------------------------------------------
pd.set_option("display.width", 0)
pd.set_option("display.max_rows", 50)
pd.set_option("display.max_columns", 30)

sys.stdout.reconfigure(encoding='utf-8')

# ------------------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
#parser.add_argument("some_arg_alas",  type=str, help="help text to be displayed")
#parser.add_argument("other_arg_alas", type=int, help="help text to be displayed")

args = parser.parse_args()

oname = "data\\churnBS4.txt"
onameTOC = "data\\levianthanTOC.txt"
TOCDict = {}

TOCDict['leviathan_TOC'] = {'name':'Leviathan Wakes Table of Contents', 'url': "http://thefreeonlinenovel.com/bi/leviathan-wakes"}
baseURL = "http://thefreeonlinenovel.com"
alinks = {}


books = {}
books['drive']      = {'order':0.1,   'name':"Drive"                           , 'pdf':"https://drive.google.com/file/d/0B_ai6QXrXx1hR2JEbmw4MUZ6UEU/view?resourcekey=0-tPyYpYfC6argPhVx1E7_fw" }
books['churn']      = {'order':0.3,   'name':"The Churn"                       , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50810-the_churn.html"                                   }
books['butcher']    = {'order':0.5,   'name':"The Butcher of Anderson Station" , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50816-the_butcher_of_anderson_station.html"             }
books['leviathan']  = {'order':1,     'name':"Leviathan Wakes"                 , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/1293-leviathan_wakes.html"                              }
books['caliban']    = {'order':2,     'name':"Caliban's War"                   , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50818-calibans_war.html"                                }
books['risk']       = {'order':2.5,   'name':"Gods of Risk"                    , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50811-gods_of_risk.html"                                }
books['abaddon']    = {'order':3,     'name':"Abaddon's Gate"                  , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50815-expanse_03_-_abaddons_gate.html"                  }
books['abyss']      = {'order':3.5,   'name':"The Vital Abyss"                 , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50822-the_vital_abyss.html"                             }
books['cibola']     = {'order':4,     'name':"Cibola Burn"                     , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50820-cibola_burn.html"                                 }
books['nemesis']    = {'order':5,     'name':"Nemesis Games"                   , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50814-expanse_05_-_nemesis_games.html"                  }
books['babylon']    = {'order':6,     'name':"Babylon's Ashes"                 , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50821-babylons_ashes.html"                              }
books['strange']    = {'order':6.5,   'name':"Strange Dogs"                    , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50817-strange_dogs.html"                                }
books['persepolis'] = {'order':7,     'name':"Persepolis Rising"               , 'url':"https://onlinereadfreenovel.com/james-s-a-corey/50813-persepolis_rising.html"                           }
books['auberon']    = {'order':7.5,   'name':"Auberon"                         , 'url':"" }
books['tiamat']     = {'order':8,     'name':"Tiamat's Wrath"                  , 'url':"" }

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    # --------------------------------------------------------------------------
    # Start
    # --------------------------------------------------------------------------
    print("Churning...")

    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    url = books['churn']['url']
    
    
    TOCurl = TOCDict['leviathan_TOC']['url']
    
    pull_online_TOC(TOCurl)
    print(TOCDict)
    ofile = io.open(onameTOC, "w", encoding='utf-8')
    ofile.write(str(TOCDict))
    ofile.close()
    
    # ofile = io.open(oname, "w", encoding='utf-8')
    # ofile.write(TOCDict)
    # ofile.close()
    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    print("...finished...for now... heres all the text in the web page")
    # print(text)


# Pull Table of Contents function 
def pull_online_TOC(url):
    # --------------------------------------------------------------------------
    # Pull the page source
    # --------------------------------------------------------------------------
    # need to have chromedriver.exe in your Path or your directory. 
    driver = webdriver.Chrome()
    # driver.maximize_window()

    driver.get(url)
    
    print("... grabbing URL...")
    # driver.page_source - this returns ALL the HTML of that webpage
    pagesource = driver.page_source
    

    # --------------------------------------------------------------------------
    # Soupify it
    # --------------------------------------------------------------------------
    TOCSoup = BeautifulSoup(pagesource,'html.parser')
    print("...Activating Soup...")

    for i, link in enumerate(TOCSoup.find_all('a')):
        dirLink = link.get('href')
        if dirLink != None: 
            con = link.get('href').split('/')
            if con[1] == "con":
                alinks[i] = str(dirLink)

    for i, key in enumerate(alinks):
        TOCDict['url_' + str(i)] = baseURL + str(alinks[key])
    
    # print(TOCDict)
    # TOCDictText = str(TOCDict)
    # # text = str(soup.title.string)
    # # --------------------------------------------------------------------------
    # # Finish
    # # --------------------------------------------------------------------------
    # return TOCDictText






def tester(x) -> str:
    print('THIS IS A TESTER FUNCTION: ' + str(x))




# ------------------------------------------------------------------------------
# Pull text from site
# ------------------------------------------------------------------------------
def pull_online_text(url) -> str:
    # --------------------------------------------------------------------------
    # Pull the page source
    # --------------------------------------------------------------------------
    # need to have chromedriver.exe in your Path or your directory. 
    driver = webdriver.Chrome()
    # driver.maximize_window()

    driver.get(url)
    print("... grabbing URL...")
    # driver.page_source - this returns ALL the HTML of that webpage
    pagesource = driver.page_source
    #driver.quit()

    # --------------------------------------------------------------------------
    # Soupify it
    # --------------------------------------------------------------------------
    soup = BeautifulSoup(pagesource,'html.parser')
    print("...Activating Soup...")
    # print(soup.prettify())
    # print(soup.get_text())

    #stuff = soup.find_all("div",class_="sc-biJonm")
    #for thing in stuff:
    #    print(thing)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # text = str(soup.get_text())
    

    # this grabs all the Divs and i had to search which div I wanted. Its teh 75 div we want in the array 
    # newsoup = soup.find_all('div')[74]
    
    #this grabs the ID and returns the DOM 
    newsoup = soup.find(id="textToRead")

    text = str(newsoup)
    # text = str(soup.title.string)
    # --------------------------------------------------------------------------
    # Finish
    # --------------------------------------------------------------------------
    return text

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    start_time = datetime.utcnow()
    main()
    end_time     = datetime.utcnow()
    elapsed_time = end_time - start_time
    print("Elapsed time: " + str(elapsed_time))
