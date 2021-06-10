import requests
import os
from bs4 import BeautifulSoup

def scrap_book_info(url):
    
    # declaration du dictionnaire qui contiendra les infos du livre
    bookInfos = {
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
    
    # Recupération du html brut de la page, reencodage en utf8 pour garder les charactères spéciaux puis passage dans bs4
    htmlResponse = requests.get(url).content.decode('utf8').encode('utf8', 'ignore')
    soup = BeautifulSoup(htmlResponse, 'lxml')
    
    # url
    bookInfos['product_page_url'] = url
    
    # Title
    bookInfos['title'] = soup.h1.text
    
    # description, review_rating
    for p in soup.find_all('p'):
        try:
            rating = p['class']
            if 'star-rating' in rating:
                bookInfos['review_rating'] = rating[1]
        except KeyError:
            bookInfos['product_description'] = p.text

    # category
    for a in soup.ul.find_all('a'):
        if 'Home' not in a.text and 'Books' not in a.text:
            bookInfos['category'] = a.text
    
    # UPC, prices, availability
    for tr in soup.find_all('tr'):
        if 'UPC' in tr.text:
            bookInfos['upc'] = tr.td.text
        elif 'excl' in tr.text:
            bookInfos['price_excluding_tax'] = tr.td.text.replace('Â', '')
        elif 'incl' in tr.text:
            bookInfos['price_including_tax'] = tr.td.text.replace('Â', '')
        elif 'Availability' in tr.text:
            bookInfos['number_available'] = ''.join(x for x in tr.td.text if x.isdigit())
    
    # image url
    bookInfos['image_url'] = soup.img['src'].replace('../..', 'http://books.toscrape.com')

    # download image
    img = requests.get(bookInfos['image_url'])

    # write image
    path = 'data/' + bookInfos['category'] + '/imgs'
    if not os.path.exists(path):
        os.makedirs(path)
    open(path + '/' + ''.join([x for x in bookInfos['title'] if x.isalnum()]) + '.jpg', 'wb').write(img.content)

    return bookInfos