#%%
import pandas as pd
import jageocoder

jageocoder.init()

def return_x_y(address):
    res = jageocoder.search(address)['candidates']
    return (res[-1]['x'], res[-1]['y'])

data = pd.read_csv("../data/Mezasta.csv",index_col=0)
data["lon"] = data.address.apply(lambda x: return_x_y(x)[0])
data["lat"] = data.address.apply(lambda x: return_x_y(x)[1])

data.to_csv("../data/Mezasta_geoinfo.csv")

# %%
