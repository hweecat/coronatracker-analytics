#%%
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from geopy.distance import geodesic
from networkx.algorithms import approximation as approx

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

nx.draw_networkx(FG, pos=FG_pos)
plt.figure(figsize=[100,50])
plt.show()

# %%

# calculate distance between airports and add feature to edges

for source, dest, index in FG.edges:
    FG[source][dest][index]['distance'] = geodesic(tuple(FG.nodes[source]['pos']), tuple(FG.nodes[dest]['pos']),
        ellipsoid='GRS-80').km

# %%

# calculate number of edges incident to each node within MultiGraph

for node in FG.nodes:
    FG.nodes[node]['degree'] = FG.degree(node)
    FG.nodes[node]['in-degree'] = FG.in_degree(node)
    FG.nodes[node]['out-degree'] = FG.out_degree(node)

# %%

# compute node connectivity between source and target
# (two distinct, nonadjacent nodes)
# this algorithm is a fast approximation that gives
# strict lower bound on actual number of
# node independent paths between two nodes 

for source, dest, index in FG.edges:
    try:
        FG[source][dest][index]['no. of node independent paths'] = approx.local_node_connectivity(FG, source, dest)
    except:
        print((source, dest, index))
        continue

# %%

pagerank_overall = nx.pagerank_numpy(FG.to_directed())

pagerank_overall

# %%

sorted(pagerank_overall, key=pagerank_overall.get, reverse=True)

# %%
###################################################################################
# FLIGHTS FROM WUHAN AIRPORT (IATA: WUH)
###################################################################################


routes_WUH = routes[routes['source'] == 'WUH']
FG_WUH = nx.from_pandas_edgelist(routes_WUH, 'source', 'destination', edge_attr=['airline', 'source', 'destination', 'equipment'], create_using=nx.MultiDiGraph())

FG_WUH.edges(data=True)

# %%

nx.set_node_attributes(FG_WUH, airports.set_index('iata')['name'].to_dict(), 'name')
nx.set_node_attributes(FG_WUH, airports.set_index('iata')['lat'].to_dict(), 'lat')
nx.set_node_attributes(FG_WUH, airports.set_index('iata')['long'].to_dict(), 'long')
nx.set_node_attributes(FG_WUH, airports.set_index('iata')['city'].to_dict(), 'city')
nx.set_node_attributes(FG_WUH, airports.set_index('iata')['country'].to_dict(), 'country')
pos = airports[airports['iata'] != '\\N'].set_index('iata')[['pos']].to_dict(orient='dict')['pos']

#%%

for node in FG_WUH.nodes:
    try:
        FG_WUH.nodes[node]['pos'] = pos[node]
    except KeyError:
        FG_WUH.nodes[node]['pos'] = [0,0]
        pos[node] = {}
        pos[node]['lat'] = 0
        pos[node]['long'] = 0

#%%

FG_WUH_pos = {}
for node in FG_WUH.nodes:
    FG_WUH_pos[node] = FG_WUH.nodes[node]['pos']

# %%

#%%


nx.draw_networkx(FG_WUH, pos=FG_WUH_pos)
plt.figure(figsize=[100,50])
plt.show()

# %%

nx.draw(FG_WUH, pos=nx.kamada_kawai_layout(FG_WUH))
plt.show()

# %%

# calculate distance between airports and add feature to edges


for source, dest, index in FG_WUH.edges:
    FG_WUH[source][dest][index]['distance'] = geodesic(tuple(FG_WUH.nodes[source]['pos']), tuple(FG_WUH.nodes[dest]['pos']),
        ellipsoid='GRS-80').km

# %%

# calculate number of edges incident to each node within MultiGraph

for node in FG_WUH.nodes:
    FG_WUH.nodes[node]['degree'] = FG_WUH.degree(node)
    FG_WUH.nodes[node]['in-degree'] = FG_WUH.in_degree(node)
    FG_WUH.nodes[node]['out-degree'] = FG_WUH.out_degree(node)

# %%
###################################################################################
# FLIGHTS OUTSIDE CHINA
###################################################################################

airports_exChina = airports[airports['country'] != 'China'][airports['iata'] != '\\N']
airports_exChina_iata_list = airports_exChina['iata'].unique().tolist()

#%%

routes_exChina = routes[routes['source'].isin(airports_exChina_iata_list)]
FG_exChina = nx.from_pandas_edgelist(routes_exChina, 'source', 'destination', edge_attr=['airline', 'source', 'destination', 'equipment'], create_using=nx.MultiDiGraph())

FG_exChina.edges(data=True)

# %%

nx.set_node_attributes(FG_exChina, airports.set_index('iata')['name'].to_dict(), 'name')
nx.set_node_attributes(FG_exChina, airports.set_index('iata')['lat'].to_dict(), 'lat')
nx.set_node_attributes(FG_exChina, airports.set_index('iata')['long'].to_dict(), 'long')
nx.set_node_attributes(FG_exChina, airports.set_index('iata')['city'].to_dict(), 'city')
nx.set_node_attributes(FG_exChina, airports.set_index('iata')['country'].to_dict(), 'country')
pos = airports[airports['iata'] != '\\N'].set_index('iata')[['pos']].to_dict(orient='dict')['pos']

#%%

for node in FG_exChina.nodes:
    try:
        FG_exChina.nodes[node]['pos'] = pos[node]
    except KeyError:
        FG_exChina.nodes[node]['pos'] = [0,0]
        pos[node] = {}
        pos[node]['lat'] = 0
        pos[node]['long'] = 0

#%%

FG_exChina_pos = {}
for node in FG_exChina.nodes:
    FG_exChina_pos[node] = FG_exChina.nodes[node]['pos']

#%%


nx.draw_networkx(FG_exChina, pos=FG_exChina_pos)
plt.figure(figsize=[100,50])
plt.show()

# %%

nx.draw(FG_exChina, pos=nx.kamada_kawai_layout(FG_exChina))
plt.show()

# %%

# calculate distance between airports and add feature to edges

for source, dest, index in FG_exChina.edges:
    FG_exChina[source][dest][index]['distance'] = geodesic(tuple(FG_exChina.nodes[source]['pos']), tuple(FG_exChina.nodes[dest]['pos']),
        ellipsoid='GRS-80').km

# %%

# calculate number of edges incident to each node within MultiGraph

for node in FG_exChina.nodes:
    FG_exChina.nodes[node]['degree'] = FG_exChina.degree(node)
    FG_exChina.nodes[node]['in-degree'] = FG_exChina.in_degree(node)
    FG_exChina.nodes[node]['out-degree'] = FG_exChina.out_degree(node)

# %%

# compute node connectivity between source and target
# (two distinct, nonadjacent nodes)
# this algorithm is a fast approximation that gives
# strict lower bound on actual number of
# node independent paths between two nodes 


for source, dest, index in FG_exChina.edges:
    try:
        FG_exChina[source][dest][index]['no. of node independent paths'] = approx.local_node_connectivity(FG_exChina, source, dest)
    except:
        print((source, dest, index))
        continue

# %%

nx.to_numpy_matrix(FG_exChina, nodelist=airports_exChina_iata_list, multigraph_weight=sum, weight='no. of node independent paths')
