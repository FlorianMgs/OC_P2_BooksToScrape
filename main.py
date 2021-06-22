import requests
from bs4 import BeautifulSoup
from scraper import Book
from create_csv import write_csv

# recuperation des urls de toutes les categories
htmlResponse = requests.get('http://books.toscrape.com/index.html')
soup = BeautifulSoup(htmlResponse.text, 'lxml')

categories = {}
print("Scrapping in progress...")
for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    if 'books_1' not in a.get('href'):
        categories[a.text.replace('\n', '').replace('  ', '')] = 'http://books.toscrape.com/' + a.get('href')

# scrap des livres de chaque categories
for categorie, catUrl in categories.items():
    htmlResponse = requests.get(catUrl)
    soup = BeautifulSoup(htmlResponse.text, 'lxml')

    # determination du nb de pages de la catégorie
    if soup.find('ul', {'class': 'pager'}):
        nbPages = int(''.join(x for x in soup.find('li', {'class': 'current'}).text if x.isdigit() and x != '1'))
    else:
        nbPages = 1

    # récupération des urls de chaque livre présent dans la catégorie
    i = 0
    booksUrl = []
    while i < nbPages:
        for book in soup.find_all('article'):
            bookUrl = book.h3.a.get('href').replace('../../../', 'http://books.toscrape.com/catalogue/')
            booksUrl.append(bookUrl)
        i += 1
        if nbPages > 1:
            nextPage = requests.get(catUrl.replace('index.html', 'page-' + str(i+1) + '.html'))
            soup = BeautifulSoup(nextPage.text, 'lxml')

    # Scrap des infos de chaque livre
    allBooksFromCurrentCategory = []
    for url in booksUrl:
        currentBook = Book().generate_data(url)
        allBooksFromCurrentCategory.append(currentBook)

    # Ecriture des fichiers CSV
    write_csv(allBooksFromCurrentCategory)

    print("Successfully scrapped " + str(len(allBooksFromCurrentCategory)) + " books from " + categorie + " category")