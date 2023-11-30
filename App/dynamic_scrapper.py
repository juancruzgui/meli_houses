from bs4 import BeautifulSoup
from requests_html import HTMLSession

url = "https://casa.mercadolibre.com.ar/MLA-1572249708-venta-casa-a-estrenar-en-barrio-privado-santo-tomas-bayugar-negocios-inmobiliarios-_JM#position=2&search_layout=grid&type=item&tracking_id=b41f9426-e7a8-4d01-9ce3-42bdc7f8c56c"

session = HTMLSession()
response = session.get(url)
response.html.render()

#soup = BeautifulSoup(response.content, 'html.parser')

with open('html_parsed.txt', 'w') as file:
    file.write(response.html.html)
