import requests
import json
import os
import pandas as pd

def get_states():
    #We make a request to ML API to get a list of states dictiionaries
    response = requests.get('https://api.mercadolibre.com/classified_locations/countries/AR')
    states_dict = json.loads(response.text)

    print ("🌎 Getting state ids")
    #We get the list of states dictionaries excluding some values corresponding to Uruguay, Brazil and USA
    states_list = states_dict['states'][1:-2]

    #We then save that list into a json file
    with open('App/ML_API/locations/states.json', 'w') as file:
        file.write(str(states_list))
    print("\n ✅ States retrieved \n")

    return states_list

def get_cities():
    #Get the cities of every state making a request to the ML API
    #We save the result into a txt file

    #first we need to chek if the file of states list exist, if not, create it
    if os.path.exists('App/ML_API/locations/states.json'):
        with open('App/ML_API/locations/states.json', 'r') as file:
            states_list = json.load(file)
    else:
        states_list = get_states()


    print("\n 🏰 Getting cities...")

    cities_list = []
    #we iter over every state dictionary on the list of states dictionray
    for index, state_dict in enumerate(states_list):
        print(f'{index}/{len(states_list)} states')
        #retrieve the state id
        state_id = state_dict['id']
        #get the list of cities dictionaries on the state making a request to the api
        cities_response = requests.get(f'https://api.mercadolibre.com/classified_locations/states/{state_id}')
        cities_dicts = json.loads(cities_response.text)['cities']
        #We add the list of cities to the city_id_lists
        cities_list += cities_dicts

    with open('App/ML_API/locations/cities.json', 'w') as file:
        file.write(str(cities_list))

    print("✅ City ids retrieved")



    return cities_list

def get_neighs():
    #We get a list of neighborhoods dicts making a request to the ml api
    #We return a json file with a list of all the dictionaries

    if os.path.exists('App/ML_API/locations/cities.json'):
        with open('App/ML_API/locations/cities.json', 'r') as file:
            cities_list = json.load(file)
    else:
        cities_list = get_cities()

    print('\n🆔 Getting neighboorhoods ids...')

    #now we need to get the ids of all of the neighborhods for each city
    #we create a list to add the neighborhood ids
    neighborhood_list = []
    #we iterate over each city dictionary to get its ids in order to retrieve all the neighborhood dictionaries
    for index, city_dict in enumerate(cities_list):
        print(f'{index}/{len(cities_list)} cities')
        city_id = city_dict['id']
        #we make a request to get the neighborhoods of each city
        neighs_response = requests.get(f'https://api.mercadolibre.com/classified_locations/cities/{city_id}')
        neighs_dict = json.loads(neighs_response.text)
        #the neighborhoods of each city is gonna be a list of neighborhood dictionaries
        neighs_list = neighs_dict['neighborhoods']
        #We add that list to the neighborhood_list
        neighborhood_list += neighs_list

    #We save the list of neighborhoods
    with open('App/ML_API/locations/neigh_list.json', 'w') as file:
        file.write(str(neighborhood_list))

    print("\n✅ Done with neighborhood ids\n")
    #each neighborhood has the form
    # {"id": "TVhYQXJlbmFzIDE5VFV4QlEwTlBVM1JoWlhOd", "name": "Arenas 19"}
    return neighborhood_list

def get_neigh_info():
    #We now need to retrieve all of the information of the neighborhoods
    #passing the id of each neighborhood
    if os.path.exists('App/ML_API/locations/neigh_list.json'):
        with open('App/ML_API/locations/neigh_list.json', 'r') as file:
            neighborhood_list = json.load(file)
    else:
        neighborhood_list = get_neighs

    print("\n 👣 Getting full information for each neighborhood...")

    #We iter over each neigh id to make a request to the ml api and get all of
    #the neigh information

    #We start an empty list to fill with the dictionaries
    neighborhood_dicts_list = []

    #We iter over each dictionary of the list of neighborhoos to get its id
    #and pass it to the request
    for index, neighborhood in enumerate(neighborhood_list):
        print(f'{index}/{len(neighborhood_list)} neighborhoods')
        neigh_id = neighborhood['id']
        location_response = requests.get(f'https://api.mercadolibre.com/classified_locations/neighborhoods/{neigh_id}')
        location_dict = json.loads(location_response.text)
        #we then add the dictionary to the list
        neighborhood_dicts_list.append(location_dict)

    #finally we save our full list of dictionaries of neigh information
    #that is goint to be used to make a csv file
    with open('App/ML_API/locations/neigh_infos.json', 'w') as file:
        file.write(str(neighborhood_dicts_list))

    print('\n✅ Neighborhoods information retrieved \n')
    return neighborhood_dicts_list

def make_neighs_csv():
    #We then make a dictionary of all of the neighborhoods

    if os.path.exists('App/ML_API/locations/neigh_infos.json'):
        with open('App/ML_API/locations/neigh_infos.json', 'r') as file:
            neighborhoods = json.load(file)
    else:
        neighborhoods = get_neigh_info()

    print("\n 📈 Building neighborhoods.csv")

    df = pd.DataFrame(neighborhoods)
    #We need to access each of the elements of each row in order to get the info
    #we want as this elements are mostly dictionaries
    df['city_name'] = df.city.apply(lambda x: x['name'])
    df['city_id'] = df.city.apply(lambda x: x['id'])
    df['state_name'] = df.state.apply(lambda x: x['name'])
    df['state_id'] = df.state.apply(lambda x: x['id'])
    df['country_name'] = df.country.apply(lambda x: x['name'])
    df = df.dropna(subset = 'geo_information')
    df['latitude'] = df.geo_information.apply(lambda x: x.get('location', None).get('latitude', None) if x.get('location', None) is not None else None)
    df['longitude'] = df.geo_information.apply(lambda x: x.get('location', None).get('longitude', None) if x.get('location', None) is not None else None)
    df = df.drop(columns = ['city', 'state', 'country', 'geo_information', 'subneighborhoods'])
    df = df.dropna(subset=['latitude', 'longitude'])

    #We then save the new dataset
    df.to_csv('App/ML_API/csvs/neighborhoods.csv.csv')

    print("✅ CSV done \n")

    return df






def get_neighbors():
    #We get all the nieghborhoods for each city in each state

    #first we check if the list of neighborhoods exists
    if not os.path.exists('App/ML_API/locations/neighs.json'):
        #if they don't exist we retrieve all of the states making a request to the api
        response = requests.get('https://api.mercadolibre.com/classified_locations/countries/AR')
        states_dict = json.loads(response.text)

        #We get the list of states dictionaries excluding some values corresponding to Uruguay, Brazil and USA
        states_list = states_dict['states'][1:-2]
        #We create an empty list to add the dictionaries of each city
        city_id_list = []
        #we iter over every state dictionary on the list of states dictionray
        for state_dict in states_list:
            #retrieve the state id
            state_id = state_dict['id']
            #get the list of cities dictionaries on the state making a request to the api
            cities_response = requests.get(f'https://api.mercadolibre.com/classified_locations/states/{state_id}')
            cities_dict = json.loads(cities_response.text)
            cities_list = cities_dict['cities']
            #We add the list of cities to the city_id_lists
            city_id_list += cities_list

        #now we need to get the ids of all of the neighborhods for each city
        #we create a list to add the neighborhood ids
        neighborhood_list = []
        #we iterate over each city dictionary to get its ids in order to retrieve all the neighborhood dictionaries
        for city_dict in city_id_list:
            city_id = city_dict['id']
            #we make a request to get the neighborhoods of each city
            neighs_response = requests.get(f'https://api.mercadolibre.com/classified_locations/cities/{city_id}')
            neighs_dict = json.loads(neighs_response.text)
            #the neighborhoods of each city is gonna be a list of neighborhood dictionaries
            neighs_list = neighs_dict['neighborhoods']
            #We add that list to the neighborhood_list
            neighborhood_list += neighs_list
        #We then create
        with open('neigh_list.json', 'w') as file:
            file.write(str(neighborhood_list))

    neighborhood_dicts_list = []
    with open('neigh_list.json', 'r') as file:
        neighborhood_list = json.load(file)

    total_neighs = len(neighborhood_list)
    retrieved_n = 0
    for neighborhood in neighborhood_list:
        neigh_id = neighborhood['id']
        location_response = requests.get(f'https://api.mercadolibre.com/classified_locations/neighborhoods/{neigh_id}')
        location_dict = json.loads(location_response.text)
        neighborhood_dicts_list.append(location_dict)
        retrieved_n += 1
        print(f'{retrieved_n}/{total_neighs}')

    with open('full_neigh.json', 'w') as file:
        file.write(str(neighborhood_dicts_list))
    return None

#print(len(n_list))

make_neighs_csv()
