run_get_html:
	python -c 'from App.article_scrapper import get_html; get_html()'

run_get_json:
	python -c 'from App.article_scrapper import get_dicts; get_dicts()'

run_get_attri:
	python -c 'from App.data_processing import get_attributes; get_attributes()'

run_all:
	python -c 'from App.interface import run_all; run_all()'

run_get_js:
	python -c 'from App.article_scrapper import get_js; get_js()'
