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

# %%
