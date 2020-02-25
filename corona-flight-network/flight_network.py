#%%
import pandas as pd

airports = pd.read_csv('airports.txt', delimiter='\t')

airports


# %%

routes = pd.read_csv('routes.txt', delimiter='\t')

routes


# %%

# merge source lat long onto routes

routes_copy = routes.copy()

routes_copy['iata'] = routes_copy['source']

airports_source = airports[[
    'name','city','country','lat','long','iata']].rename(
        columns={"name": "sourcename", "city": "sourcecity",
            "country": "sourcecountry",
            "lat": "sourcelat", "long": "sourcelong"})

routes_merge_source = pd.merge(airports_source, routes_copy, on='iata').drop(columns='iata')

routes_merge_source

# %%

routes_merge_source['iata'] = routes_merge_source['destination']

airports_destination = airports[[
    'name','city','country','lat','long','iata']].rename(
        columns={"name": "destinationname", "city": "destinationcity",
            "country": "destinationcountry",
            "lat": "destinationlat", "long": "destinationlong"})

routes_merge_airports = pd.merge(routes_merge_source, airports_destination, on='iata').drop(columns='iata')

column_order = ['airline', 'airlinecode',
    'source', 'sourcecode', 'sourcename', 'sourcecity', 'sourcecountry', 'sourcelat', 'sourcelong',
    'destination', 'destinationcode', 'destinationname',
    'destinationcity', 'destinationcountry', 'destinationlat',
    'destinationlong',
    'codeshare', 'stops', 'equipment']

routes_merge_airports[column_order]

#%%

def latlongToArray(x, y):
    return [x, y]

#%%

airports['pos'] = airports.apply(lambda x: latlongToArray(x['lat'], x['long']), axis=1)

airports

# %%

import networkx as nx

FG = nx.from_pandas_edgelist(routes, 'source', 'destination', edge_attr=['airline', 'source', 'destination', 'equipment'], create_using=nx.MultiDiGraph())

FG.edges(data=True)

#%%

nx.set_node_attributes(FG, airports.set_index('iata')['name'].to_dict(), 'name')
nx.set_node_attributes(FG, airports.set_index('iata')['lat'].to_dict(), 'lat')
nx.set_node_attributes(FG, airports.set_index('iata')['long'].to_dict(), 'long')
nx.set_node_attributes(FG, airports.set_index('iata')['city'].to_dict(), 'city')
nx.set_node_attributes(FG, airports.set_index('iata')['country'].to_dict(), 'country')
pos = airports[airports['iata'] != '\\N'].set_index('iata')[['pos']].to_dict(orient='dict')['pos']

#%%

FG.nodes(data=True)

#%%

# TODO: Fix bug "NetworkXError: Node 'AOS' has no position."
# pos['AOS'] KeyError

for node in FG.nodes:
    try:
        FG.nodes[node]['pos'] = pos[node]
    except KeyError:
        FG.nodes[node]['pos'] = [0,0]
        pos[node] = {}
        pos[node]['lat'] = 0
        pos[node]['long'] = 0

#%%

FG_pos = {}
for node in FG.nodes:
    FG_pos[node] = FG.nodes[node]['pos']

#%%

import matplotlib.pyplot as plt

nx.draw_networkx(FG, pos=FG_pos)
plt.figure(figsize=[100,50])
plt.show()

# %%
