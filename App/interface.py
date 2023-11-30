from App.article_scrapper import get_dicts, get_html
from App.data_processing import get_attributes

def run_all():
    get_html()
    get_dicts()
    get_attributes()
