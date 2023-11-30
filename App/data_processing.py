import json

def get_attributes(specs_dict = None):

    attributes = {}
    #Get basic attributes
    try:
        for attribute in specs_dict[0]['attributes']:
            attributes[f"{attribute.get('id',None)}"] = attribute.get('text',None)
    except:
        return None, None

    #Get ambientes, servicios, seguridad, confort
    extras = {}
    for i in range(1,len(specs_dict)):
        for extra in specs_dict[i]['attributes']:
            element = extra['values']['value_text']['text']
            yes_no = extra['text']
            if 'No' in yes_no:
                yes = 'No'
            else:
                yes = 'Si'
            extras[f'{element}'] = yes

    return attributes, extras

def get_pois(pois_dict = None):
    return None
