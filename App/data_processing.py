import json

def get_attributes(specs_dict = None):

    if not specs_dict:
        with open('specs.txt', 'r') as file:
            #print(file.read())
            try:
                string = file.read()
                string = string.replace("'", '"').replace('True','true').replace('False','false')
                specs_dict = json.loads(string)
            except:
                print("Attributes not found")
                return None

    attributes = {}
    #Get basic attributes
    for attribute in specs_dict[0]['attributes']:
        attributes[f"{attribute.get('id',None)}"] = attribute.get('text',None)
        print(f"{attribute['id']} : {attribute['text']}")

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
            print(f"{element}: {yes}")

    return attributes
