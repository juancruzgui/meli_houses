import pandas as pd
import json
import requests
import os
from nei_ids import *

#https://api.mercadolibre.com/sites/MLA/search?item_location=lat:$LATITUDE1_LATITUDE2,lon:$LONGITUDE1_LONGITUDE2&category=$CATEGORY_ID

#ML houses for sale "MLA1468"
#ML apartments for sale "MLA1474"

#Total 5843 rows
#Chunks of 100 houses

def get_houses_ids(house = True, start = 0):

    #Retrieve neighborhood dataset
    if os.path.exists('App/ML_API/csvs/neighborhoods.csv'):
        df = pd.read_csv('App/ML_API/neighborhoods.csv')
    else:
        df = make_neighs_csv
    #start a counter of properties retrieved in the run
    properties = 0
    #make an empty list to fill with propertis
    properties_list = []

    #Define the logic for houses or for appartment based on house argument
    #if house ->houses else ->apartments
    if house:
        path = 'App/ML_API/ids/houses_ids.txt'
        category = 'MLA1468'
        text = 'houses'
    else:
        path = 'App/ML_API/ids/apartments_ids.txt'
        category = 'MLA1474'
        text = 'apartments'

    print(f'\n 🆔 Sarting to get {text} ids...\n')
    #iter over each row corresponding to a unique neighborhood to bring
    #all of the houses ids from ml api
    for i, row in df.iterrows():
        #if given a start row, in case the program crashes in a certain row
        if i>=start:
            #print to check wich row we are working with
            print(f"\nWorking on neighborhood {i}/{len(df)}")
            #print to check the number of properties retrieved from previous neighborhoods
            #on this run
            print(f"{properties} {text} retrieved")

            #get ids for request
            state_id = row['state_id']
            city_id = row['city_id']
            neigh_id = row['id']

            #Firts request is to check if we have to do pagination and to bring the first houses
            #https://api.mercadolibre.com/sites/MLA/search?&category={category}&state={state_id}&city={city_id}&neighborhood={neigh_id}
            response = requests.get(f'https://api.mercadolibre.com/sites/MLA/search?&category={category}&state={state_id}&city={city_id}&neighborhood={neigh_id}')
            response_dict = json.loads(response.text)
            #Account the total number of houses from the request to check for pagination
            total = response_dict['paging']['primary_results']
            results = response_dict['results']
            #retrieving the id for each of the results
            for result in results:
                properties_list+=result['id']
                #appending the id to a txt file
                with open(path, 'a') as file:
                    file.write(f'{result["id"]}\n')
            #sum the number of results from this neigborhood to the total houses retrieved on this run
            properties+=total
            print(f"Total {text} results: {total}")

            #if the total properties is higher than 50, as the limit is 50 results per request
            #we need to do pagination with the offset argument
            if total>50:
                #The offset needs to be adding 50 every time to check the next results
                #It need to stop when we get to the total or before the total is the total is not multiple of 50
                for offset in range(50,total,50):
                    print(f"Offset {offset}/{total}")
                    response = requests.get(f'https://api.mercadolibre.com/sites/MLA/search?&category={category}&state={state_id}&city={city_id}&neighborhood={neigh_id}&offset={offset}')
                    response_dict = json.loads(response.text)
                    results = response_dict['results']
                    #retrieving the id of each of the results
                    for result in results:
                        properties_list+=result['id']
                        #appending the id to a txt file
                        with open(path, 'a') as file:
                            file.write(f'{result["id"]}\n')
        else:
            pass
    with open(path, 'r') as file:
        property_txt = file.read()
    print(f"\n ✅ {text} ids retrieved \n")
    return property_txt
