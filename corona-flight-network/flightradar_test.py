#%%
import flightradar24
fr = flightradar24.Api()
airports = fr.get_airports()

airports

# %%

import pandas as pd
import json

airports_json = json.dumps(airports)
airports_raw_df = pd.read_json(airports_json, orient='columns')

airports_raw_df


#%%

def read_raw_df(data):
    
    data_json = json.dumps(data)
    data_raw_df = pd.read_json(data_json)
    
    return data_raw_df

# %%

def read_airport_data(df_rows):
    
    df_dict_to_rows = pd.DataFrame.from_dict(df_rows, orient='index').transpose()
    
    return df_dict_to_rows

#%%

def convert_dict_to_df(df):
    
    extracted_rows = []
    for idx in range(len(df)):
        extracted_rows.append(read_airport_data(df['rows'][idx]))
    extracted_df = pd.concat(extracted_rows).reset_index(drop=True)
    
    return extracted_df

#%%

airports_raw_df = read_raw_df(airports)

airports_raw_df

#%%

airports_df = convert_dict_to_df(airports_raw_df)

airports_df
        

#%%

airports_df.loc[0, 'name'] = airports_df.loc[0, 'name'].replace('\t','')

airports_df

#%%

# count if there are other rows with '\t'

[s.find('\t') for s in airports_df['name'].tolist()].count(0)

#%%

fr = flightradar24.Api()
airlines = fr.get_airlines()

airlines

#%%

airlines_raw_df = read_raw_df(airlines)

airlines_raw_df


# %%

airlines_df = convert_dict_to_df(airlines_raw_df)

airlines_df

# %%

#%%

fr = flightradar24.Api()
airlines = fr.get_airlines()

airlines

#%%

airlines_json = json.dumps(airlines)
airlines_raw_df = pd.read_json(airlines_json, orient='columns')

airlines_raw_df


# %%

airlines_df = convert_dict_to_df(airlines_raw_df)

airlines_df

#%%

airline = airlines_df['ICAO'][1300]
fr = flightradar24.Api()
flights = fr.get_flights(airline)

flights

# %%

flight_id = 'SQ185' # Turkish Airlines' Istanbul - New York flight
fr = flightradar24.Api()
flight = fr.get_flight(flight_id)

flight

# %%

from datetime import datetime
datetime.fromtimestamp(flight['result']['response']['data'][3]['time']['other']['eta'])

# %%
