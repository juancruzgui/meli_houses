from article_scrapper import *
from data_processing import *
import pandas as pd


def make_row(url):
    location = None
    longitude = None
    latitude = None
    specs = None
    attributes_dict = None
    extras_dict = None


    while (location is None) & (specs is None) & (attributes_dict is None):
        response = get_html(url)
        information = get_dicts(response)
        id, seller_id, symbol, price, province, location, latitude, longitude, specs, points_of_interest = information
        attributes_dict, extras_dict = get_attributes(specs)

    house_info = {'id' : id,
                  'seller_id' : seller_id,
                  'symbol' : symbol,
                  'price' : price,
                  'province' : province,
                  'location' : location,
                  'latitude' : latitude,
                  'longitude' : longitude,
                  }
    house_info = {**house_info, **attributes_dict, **extras_dict}

    # unique_values = set()
    # result_dict = {}

    for key,value in house_info.items():
        print(f'{key}: {value}')

    return house_info

url = "https://casa.mercadolibre.com.ar/MLA-1397094217-nuevo-precio-casa-en-venta-tipo-chalet-de-3-amb-en-quilmes-o-apta-credito-consulta-financiacion-_JM#position=3&search_layout=grid&type=item&tracking_id=5a698126-6cf6-4ae4-afe6-e7ce57e787d4"
make_row(url)
