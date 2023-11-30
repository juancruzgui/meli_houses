import requests
import json
import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup as soup

#The functions for this module scrape a house webpage and get the dictionaries for name, location, spechs, points of interest and price

try_url = "https://casa.mercadolibre.com.ar/MLA-1578446312-venta-casa-4-plantas-jardin-pileta-_JM#position=29&search_layout=grid&type=item&tracking_id=413a3992-1394-43c0-85cc-5b23ccf93eae"
headers = {
        'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

try_search = 'https://inmuebles.mercadolibre.com.ar/casas/venta/propiedades-individuales/mendoza/_Desde_49_NoIndex_True'

def get_urls(province):
    base_url = f'https://inmuebles.mercadolibre.com.ar/casas/venta/propiedades-individuales/{province}'
    #get number of pages
    response = requests.get(base_url, headers=headers)
    sopa = soup(response.text, 'html.parser')
    try:
        pages = int(sopa.find("li", {'class' : "andes-pagination__page-count"}).text.split()[1])
    except:
        pages = 0

    #obtain list of url
    def get_links(url_to_scrape):
        url = url_to_scrape
        response = requests.get(url, headers=headers)
        sopa = soup(response.text, 'html.parser')
        articles = sopa.find_all("div", {'class' : 'ui-search-result__wrapper'})
        page_links = []
        for article in articles:
            link = article.find("a", {'class' : 'ui-search-link__title-card ui-search-link'}).get("href")
            with open(f'{province}_links.txt', 'a') as file:
                file.write(f'{link}\n')
            page_links.append(link)
        return page_links

    all_links = []
    #first page
    all_links += get_links(base_url)

    if pages>0:
        for i in range(1, pages-1):
            url = f'{base_url}/_Desde_{i*48+1}_NoIndex_True'
            all_links += get_links(url)

    return all_links


def get_html(url):
    #Pass the url to get the html text response

    response = requests.get(url, headers=headers)
    with open('html.txt', 'w') as file:
        file.write(response.text)
    return response.text

def get_dicts(response_text):
    #pass the html text response to get specs dict and points of interest dicts

    #if response not passed open file

    #regex pattern to find dict
    pattern = re.compile(f'{re.escape("window.__PRELOADED_STATE__ = ")}(.*?){re.escape("};")}')
    #find pattern match
    match = pattern.search(response_text)

    if match:
        #Whole dictionary
        text_dict = match.group(1)+"}"
        data_dict = json.loads(text_dict)
        with open('json.txt','w') as file:
            file.write(text_dict)

        #Name
        id = data_dict["initialState"]["components"]["content_right"][0]["phone_link"]["track"]["melidata_event"]["event_data"]["item_id"]
        seller_id = data_dict["initialState"]["components"]["content_right"][0]["phone_link"]["track"]["melidata_event"]["event_data"]["seller_id"]
        #Price
        price = data_dict["initialState"]["components"]["short_description"][1]["price"]["value"]
        symbol = data_dict["initialState"]["components"]["short_description"][1]["price"]["currency_symbol"]

        #Location
        location = None
        latitude = None
        longitude = None
        try:
            location = data_dict["initialState"]["components"]["content_left"][0]["content_rows"][0]["title"]["text"]
            latitude = data_dict["initialState"]["components"]["content_left"][0]["map_info"]["location"]["latitude"]
            longitude = data_dict["initialState"]["components"]["content_left"][0]["map_info"]["location"]["longitude"]
        except:
            return None, None, None, None, None, None, None, None, None, None
        province = data_dict["initialState"]["components"]["content_right"][0]["phone_link"]["track"]["analytics_event"]["custom_dimensions"]["139"]

        #Check article info
        with open("article_info.txt", "w") as file:
            file.write(f'id: {id}, seller id: {seller_id}\nlocation: {location}, province: {province}\nlatitude: {latitude}, longitude: {longitude} \nPrice: {symbol}{price}')

        #print(f'id: {id}, seller id: {seller_id}\nlocation:{location}, province: {province}\nlatitude:{latitude}, longitude: {longitude}\nPrice: {symbol}{price}\n')
        #Specs
        specs = None
        try:
            specs = data_dict["initialState"]["components"]["content_left"][0]["specs"]
        except:
            try:
                specs = data_dict["initialState"]["components"]["content_left"][1]["specs"]
            except:
                return None, None, None, None, None, None, None, None, None, None


        with open("specs.txt", "w") as file:
            file.write(str(specs))

        #POI
        points_of_interest = None
        try:
            points_of_interest = data_dict["initialState"]["components"]["content_left"][1]["categories"]
            with open("poi.txt", "w") as file:
                file.write(str(points_of_interest))
        except:
            try:
                points_of_interest = data_dict["initialState"]["components"]["content_left"][2]["categories"]
                with open("poi.txt", "w") as file:
                    file.write(str(points_of_interest))
            except:
                print("POIs not found")
                pass


    return id, seller_id, symbol, price, province, location, latitude, longitude, specs, points_of_interest
