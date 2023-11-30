from App.article_scrapper import get_dicts, get_html
from App.data_processing import get_attributes
from article_scrapper import get_urls

def run_all():
    get_html()
    get_dicts()
    get_attributes()

def get_all_urls():
    provinces = ['bsas-costa-atlantica',
                 'bsas-gba-norte',
                 'bsas-gba-oeste',
                 'bsas-gba-sur',
                 'buenos-aires-interior',
                 'capital-federal',
                 'chubut',
                 'cordoba',
                 'corrientes',
                 'entre-rios',
                 'formosa',
                 'jujuy',
                 'la-pampma',
                 'mendoza',
                 'misiones',
                 'neuquen',
                 'rio-negro',
                 'salta',
                 'san-juan',
                 'san-luis',
                 'santa-cruz',
                 'santa-fe',
                 'santiago-del-estero',
                 'tierra-del-fuego',
                 'tucuman']
    links = []
    for province in provinces:
        urls = get_urls(province)
        links += urls
    return links

get_all_urls()
