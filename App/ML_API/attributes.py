import requests
import pandas
import json
import os
from get_houses_ids import *

def get_attributes(houses= True, start = 0):

    #If True -> houses, if False -> apartments

    #Read ids list
    if houses:
        if os.path.exists('App/ML_API/ids/houses_ids.txt'):
            with open('App/ML_API/ids/houses_ids.txt', 'r') as file:
                property_txt = file.read()

        else:
            print("noexists")
            property_txt = get_houses_ids()
        text = 'houses'
    else:
        if os.path.exists('App/ML_API/ids/apartments_ids.txt'):
            with open('App/ML_API/ids/apartments_ids.txt', 'r') as file:
                property_txt = file.read()
        else:
            property_txt = get_houses_ids(False)
        text = 'apartments'

    #Convert the file into a list of ids
    property_list = property_txt.split('\n')

    #Logic for getting attributes
    #every item of the list is a house id - we need to excecute an html request
    #to ml api to bring attributes
    #https://api.mercadolibre.com/items/{item_id}

    print(f"\n🛏️ Working on {text} attributes ")

    for index, item_id in enumerate(property_list):
        #We start from the index passed, useful when the program crashes and we need to start from a certain house
        #if not index passed start=0
        if index >= start:
            if houses:
                print(f'house {index}/{len(property_list)}')
            else:
                print(f'apartment {index}/{len(property_list)}')
            response = requests.get(f'https://api.mercadolibre.com/items/{item_id}').text
            property_dict = json.loads(response)
            #keys:
            # Basics ->'id', 'title', 'permalink'
            # Price -> 'price', 'currency_id'
            # Location -> 'location': { 'address_line', 'zip_code', 'neighborhood': {
            # 'id', 'name'}, 'city' : {'id', 'name'}, 'state' : {'id', 'name'}
            # Attributes -> 'attributes': {[{'id', 'value_name'},...]} list of attributes

            #Retrieving basic columns
            id, title, url = property_dict['id'], property_dict['title'], property_dict.get('permalink', None)
            price, currency = property_dict.get('price', None),property_dict.get('currency_id', None)

            location = property_dict.get('location', None)
            if location:
                address, zip_code = location['address_line'], location['zip_code']
                neigh_name, neigh_id = location['neighborhood']['name'], location['neighborhood']['id']
                city_name, city_id = location['city']['name'], location['city']['id']
                state_name, state_id = location['state']['name'], location['state']['id']
            else:
                continue


            #Retrieving attributes columns -> they vary for each property
            attribute_list = property_dict.get('attributes', None)
            if attribute_list:
                #We iter over all attributes
                attributes_dict = {}
                for attribute in attribute_list:
                    key = attribute['id']
                    value = attribute['value_name']
                    attributes_dict[f'{key}'] = value
            else:
                continue

            #Building a json of the house with important information
            #id, title, url, currency, price, address, zip_code, neighborhood_name,
            #neighborhood_id, city_name, city_id, state_name, state_id, attributes
            house = {'id':id,
                    'title':title,
                    'url':url,
                    'currency':currency,
                    'price':price,
                    'address':address,
                    'zip_code':zip_code,
                    'neighborhood_name':neigh_name,
                    'neighborhood_id':neigh_id,
                    'city_name':city_name,
                    'city_id':city_id,
                    'state_name':state_name,
                    'state_id':state_id}
            #add attributes to the dictionary unpacking both dicts
            house = {**house, **attributes_dict}

            #Appending dictionary to a file with all the houses to check if working
            if houses:
                with open('App/ML_API/attributes/houses_attri.txt', 'a') as file:
                    file.write(f'{json.dumps(house)}\n')
            else:
                with open('App/ML_API/attributes/apartments_attri.txt', 'a') as file:
                    file.write(f'{json.dumps(house)}\n')
        else:
            pass
    print(f"/n ✅ Done getting {text} attributes")

    return None

get_attributes(start=26359)
