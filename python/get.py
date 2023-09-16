#%%
import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from tqdm.notebook import trange
from tqdm import tqdm

import pandas as pd
#import geopandas as gpd

class Mezasta_Shop():
    def __init__(self, name=None, address=None, info=None) -> None:
        self.name = name
        self.address = address
        self.info = info
        self.x = 0.
        self.y = 0.
        self.get_address()
        pass
    
    def get_address(self):
        url = "https://jageocoder.info-proto.com/geocode"
        response = req.get(url,params={'addr':self.address})
        #print(self.address)
        res_json = response.json()
        _json = res_json[-1]
        self.x = float(_json['node']['x'])
        self.y = float(_json['node']['y'])
    def show(self):
        print(self.x,self.y)

def get_shop_data(shop_result):
    shop_name = shop_result.find_all("dd",{"class":"resultList_txt"})[0].text.replace('\t','')
    shop_address = shop_result.find_all("dd",{"class":"resultList_txt"})[1].text
    shop_event = shop_result.find_all("dd",{"class":"resultList_txt"})[2].text
    return [shop_name, shop_address, shop_event]

def get_total_page(soup):
    query = soup.find_all("div", {"class":"pageLink_body"})[0]\
    .find_all("a")[-1]['href']
    return int(parse_qs(query)["page"][0])

url = "https://pokemonmezastar.com/shop/search.html"

# %%
total_page = None
response = req.get(url,params={'page':1})
soup = BeautifulSoup(response.text, "html.parser")# %%
if total_page == None:
    total_page = get_total_page(soup)
    print(f"total_page:{total_page}")

shop_lists = []

for i in tqdm(range(1,total_page+1)):
    response = req.get(url,params={'page':str(i)})
    soup = BeautifulSoup(response.text, "html.parser")# %%
    list_shop_search = soup.find_all("div",{"class":"shop-search"})
    shop_lists += [get_shop_data(shop) for shop in list_shop_search]
# %%
Shops = [Mezasta_Shop(*_shop) for _shop in shop_lists]
df2 = pd.DataFrame(list(map(lambda hoge: vars(hoge), Shops)))
df2.to_csv("Mezasta.csv")
# %%
import jageocoder
# %%
shop_lists
# %%
shop_lists
# %%
