import csv
import requests
from bs4 import BeautifulSoup

# declaration du dictionnaire qui contiendra les infos du livre
pdtInfos = {
    'product_page_url': '',
    'upc': '',
    'title': '',
    'price_including_tax': '',
    'price_excluding_tax': '',
    'number_available': '',
    'product_description': '',
    'category': '',
    'review_rating': '',
    'image_url': '',
}

# Recupération du html brut de la page, passage dans bs4
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# url
pdtInfos['product_page_url'] = url

# Title
pdtInfos['title'] = soup.h1.text

# description, review_rating
for p in soup.find_all('p'):
    try:
        rating = p['class']
        if 'star-rating' in rating:
            pdtInfos['review_rating'] = rating[1]
    except KeyError:
        pdtInfos['product_description'] = p.text

# category
for a in soup.ul.find_all('a'):
    if 'Home' not in a.text and 'Books' not in a.text:
        pdtInfos['category'] = a.text

# UPC, prices, availability
for tr in soup.find_all('tr'):
    if 'UPC' in tr.text:
        pdtInfos['upc'] = tr.td.text
    elif 'excl' in tr.text:
        pdtInfos['price_excluding_tax'] = tr.td.text.replace('Â', '')
    elif 'incl' in tr.text:
        pdtInfos['price_including_tax'] = tr.td.text.replace('Â', '')
    elif 'Availability' in tr.text:
        pdtInfos['number_available'] = ''.join(x for x in tr.td.text if x.isdigit())

# image url
pdtInfos['image_url'] = soup.img['src'].replace('../..', 'http://books.toscrape.com')

print(pdtInfos)

#csv
csvColumns = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
csvFile = 'scrapped_books.csv'
with open('data/' + csvFile, 'w', encoding='utf-8') as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames=csvColumns)
    writer.writeheader()
    writer.writerow(pdtInfos)

