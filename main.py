from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections

FILE_EXCEL = 'wine3.xlsx'
SHEET_NAME_EXEL = 'Лист1'


def counts_winery_age():
    today = datetime.datetime.now()
    now_year = today.year
    creation_data = datetime.datetime(year=1920, month=1, day=1)
    creation_year = creation_data.year
    winery_age = now_year - creation_year
    return winery_age


def deduces_assortment():
    wine_excel = pandas.read_excel(FILE_EXCEL, sheet_name=SHEET_NAME_EXEL, na_values=str, keep_default_na=False)
    wines = wine_excel.to_dict(orient='records')
    assortment = collections.defaultdict(list)
    for wine in wines:
        assortment[wine['Категория']].append(wine)
    return assortment


def get_categories(assortment):
    assortment_categories = []
    for wine in assortment:
        assortment_categories.append(wine)
    assortment_categories = sorted(assortment_categories)
    return assortment_categories


def generates_store_data():
    winery_age = counts_winery_age()
    assortment = deduces_assortment()
    assortment_categories = get_categories(assortment)
    rendered_page = template.render(
        wines=assortment,
        winery_age=winery_age,
        wine_categories=assortment_categories,
        category_quantity=len(assortment_categories)
    )
    return rendered_page


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = generates_store_data()
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
