import csv

import requests
from bs4 import BeautifulSoup

def scrap_book_data(book_url):

    url = "http://books.toscrape.com/catalogue/"+book_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    infos_th = soup.find_all(["th"])
    infos_td = soup.find_all(["td"])

    book = {}
    index = []
    data = []

    for ligne_th in infos_th:
        info_th = ligne_th.get_text("th")
        index.append(info_th)

    for ligne_td in infos_td:
        info_td = ligne_td.get_text("td")
        data.append(info_td)

    for x in range(7):
        book[index[x]] = data[x]

    with open('info_livre.csv', 'a') as fichier:
        writer = csv.writer(fichier, delimiter=',')
        for key in book.keys():
            writer.writerow(([key, book[key]]))
    return

def get_book_from_category(category_url):
    url = "http://books.toscrape.com/"+category_url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(category_url)

    f"""or livre in soup.find_all("h3"):
        for link in livre.find_all('a'):
            scrap_book_data(link.get('href').lstrip("../"))"""
    next = soup.find(class_="next")
    print (next)
    next_page = next.find('a').get('href')

    """if next:
        new_category_url = category_url.replace("index.html", "")
        print(new_category_url+next.find('a').get('href'))
        get_book_from_category(new_category_url+next.find('a').get('href'))"""
    return next_page

url = "http://books.toscrape.com/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

for category in soup.find_all("div", class_= 'side_categories'):
    for link in category.find_all('a'):
        url_category = link.get(('href'))
        next_page = get_book_from_category(url_category)
        while next_page:
            new_page = get_book_from_category(url_category.replace("index.html", next_page))
            next_page = new_page

#print(livres)

""" AUTRE METHODE
product_info = soup.select('table.table')

print(product_info)

for info in product_info:
    universal_product_code = info.select('tr > td')[0].text

print(universal_product_code)"""




