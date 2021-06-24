import requests
import os
from bs4 import BeautifulSoup


class Book:

    def get_soup(self, url):
        htmlResponse = requests.get(url).content.decode('utf8').encode('utf8', 'ignore')
        soup = BeautifulSoup(htmlResponse, 'lxml')
        return soup

    def book_url(self, url):
        return {'product_page_url': url}

    def book_title(self, url):
        soup = self.get_soup(url)
        return {'title': soup.h1.text}

    def book_desc_reviews(self, url):
        soup = self.get_soup(url)

        desc = ""
        review = ""

        for p in soup.find_all('p'):
            try:
                rating = p['class']
                if 'star-rating' in rating:
                    review = rating[1]
            except KeyError:
                desc = p.text
        return {
            'review_rating': review,
            'product_description': desc
        }

    def book_category(self, url):
        soup = self.get_soup(url)
        for a in soup.ul.find_all('a'):
            if 'Home' not in a.text and 'Books' not in a.text:
                return {'category': a.text}

    def book_upc_prices_stocks(self, url):
        soup = self.get_soup(url)

        upc = ""
        priceExclTax = ""
        priceInclTax = ""
        stock = ""

        for tr in soup.find_all('tr'):
            if 'UPC' in tr.text:
                upc = tr.td.text
            elif 'excl' in tr.text:
                priceExclTax = tr.td.text.replace('Â', '')
            elif 'incl' in tr.text:
                priceInclTax = tr.td.text.replace('Â', '')
            elif 'Availability' in tr.text:
                stock = tr.td.text.split(' ')[3].replace('(', '')
        return {
            'upc': upc,
            'price_excluding_tax': priceExclTax,
            'price_including_tax': priceInclTax,
            'number_available': stock
        }

    def book_img(self, url):
        soup = self.get_soup(url)

        imageUrl = soup.img['src'].replace('../..', 'http://books.toscrape.com')
        imageBinary = requests.get(imageUrl)
        category = self.book_category(url)
        title = self.book_title(url)
        path = 'data/' + category['category'] + '/imgs'
        imgTitle = ''.join([x for x in title['title'] if x.isalnum()]) + '.jpg'

        if not os.path.exists(path):
            os.makedirs(path)
        # write image
        open(path + '/' + imgTitle, 'wb').write(imageBinary.content)

        return {
            'image_url': imageUrl,
            'image_path': path + '/' + imgTitle
        }

    def generate_data(self, url):
        bookInfos = {}
        bookInfos.update(self.book_url(url))
        bookInfos.update(self.book_title(url))
        bookInfos.update(self.book_desc_reviews(url))
        bookInfos.update(self.book_category(url))
        bookInfos.update(self.book_upc_prices_stocks(url))
        bookInfos.update(self.book_img(url))

        return bookInfos
