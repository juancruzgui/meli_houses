import requests
import json
import re

#The functions for this module scrape a house webpage and get the dictionaries for name, location, spechs, points of interest and price

try_url = "https://casa.mercadolibre.com.ar/MLA-1396590899-casa-venta-parque-patricios-quincho-pileta-cochera-_JM"
def get_html(url = try_url):
    #Pass the url to get the html text response
    if not url:
        url = "https://casa.mercadolibre.com.ar/MLA-1572291106-apto-bancor-casa-3-dorm-villa-belgrano-_JM#position=10&search_layout=grid&type=item&tracking_id=51040e91-a57b-4a90-8868-3a896b79bd86"

    response = requests.get(url)
    with open('html.txt', 'w') as file:
        file.write(response.text)
    return response.text

def get_dicts(response_text = None):
    #pass the html text response to get specs dict and points of interest dicts

    #if response not passed open file
    if not response_text:
        with open('html.txt', 'r') as file:
            response_text = file.read()

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
        #location = data_dict["initialState"]["components"]["content_left"][0]["content_rows"][0]["title"]["text"]
        #latitude = data_dict["initialState"]["components"]["content_left"][0]["map_info"]["location"]["latitude"]
        #longitude = data_dict["initialState"]["components"]["content_left"][0]["map_info"]["location"]["longitude"]
        province = data_dict["initialState"]["components"]["content_right"][0]["phone_link"]["track"]["analytics_event"]["custom_dimensions"]["139"]

        #Check article info
        with open("article_info.txt", "w") as file:
            file.write(f'id: {id}, seller id: {seller_id}\nlocation:, province: {province}\nlatitude:, longitude: \nPrice: {symbol}{price}')

        print(f'id: {id}, seller id: {seller_id}\nlocation:, province: {province}\nlatitude:, longitude: \nPrice: {symbol}{price}\n')
        #Specs
        specs = None
        try:
            specs = data_dict["initialState"]["components"]["content_left"][0]["specs"]
        except:
            try:
                specs = data_dict["initialState"]["components"]["content_left"][1]["specs"]
            except:
                print("Specs not found")
                pass


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


    return id, seller_id, symbol, price,province, specs, points_of_interest
