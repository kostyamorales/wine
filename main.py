from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse

parser = argparse.ArgumentParser(
    description='Программа показывает ассортимент магазина'
)
parser.add_argument('file_name', help='Файл с ассортиментом')
args = parser.parse_args()


def counts_winery_age():
    today = datetime.datetime.now()
    now_year = today.year
    creation_data = datetime.datetime(year=1920, month=1, day=1)
    creation_year = creation_data.year
    winery_age = now_year - creation_year
    return winery_age


def deduces_assortment():
    wine_excel = pandas.read_excel(args.file_name, na_values=str, keep_default_na=False)
    wines = wine_excel.to_dict(orient='records')
    assortment = collections.defaultdict(list)
    for wine in wines:
        assortment[wine['Категория']].append(wine)
    return assortment


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    winery_age = counts_winery_age()
    assortment = deduces_assortment()

    template = env.get_template('template.html')
    rendered_page = template.render(
        winery_age=winery_age,
        wines=assortment
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
