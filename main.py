import os.path
import requests
from bs4 import BeautifulSoup

image_path = 'pictures'
if not os.path.exists(image_path):
    os.makedirs(image_path)

category_path = 'category'
if not os.path.exists(category_path):
    os.makedirs(category_path)

url_category = "http://books.toscrape.com/catalogue/category/books/"
url_index = "http://books.toscrape.com/index.html"


def scrap_book_data(book, category_name):

    url_book = "http://books.toscrape.com/catalogue/"+book
    page_book = requests.get(url_book)
    soup_book = BeautifulSoup(page_book.content, 'html.parser')

    book = {
        "title": "",
        "product_page_url": "",
        "upc": "",
        "product_description": "",
        "price_excluding_tax": "",
        "price_including_tax": "",
        "availability": "",
        "category": "",
        "rating": "",
        "cover_page_url": "",
    }

    data = []
    info_td = soup_book.find_all(["td"])
    for line in info_td:
        data.append(line.get_text("td"))

    book["upc"] = data[0]
    book["price_excluding_tax"] = data[2]
    book["price_including_tax"] = data[3]
    book["availability"] = data[5]

    book["title"] = soup_book.find('h1').text.replace("/", ",")
    book["product_page_url"] = url_book
    book["product_description"] = soup_book.select("p")[3].text.replace(";", ",")
    book["category"] = category_name
    book["rating"] = soup_book.find('p', class_='star-rating').get('class')[1] + '/Five'
    cover_page = soup_book.select('img')[0]
    book["cover_page_url"] = "http://books.toscrape.com/"+cover_page.get('src').lstrip('../')

    book_csv_line = book["product_page_url"] + ";" + \
                    book["upc"] + ";" + \
                    book["title"] + ";" + \
                    book["price_including_tax"] + ";" + \
                    book["price_excluding_tax"] + ";" + \
                    book["availability"] + ";" + \
                    book["product_description"] + ";" + \
                    book["category"] + ";" + \
                    book["rating"] + ";" + \
                    book["cover_page_url"] + ";"

    with open(image_path+'/'+book["title"]+".jpg", "wb") as file:
        image = requests.get(book["cover_page_url"])
        file.write(image.content)

    with open(category_path+'/'+book["category"]+".csv", "a") as file:
        file.write(book_csv_line + "\n")
    return


def category_page(category_name, page):
    page = requests.get(url_category+category_name+'/page-'+page+'.html')
    soup = BeautifulSoup(page.content, 'html.parser')

    for book in soup.find_all("h3"):
        for link in book.find_all('a'):
            scrap_book_data(link.get('href').lstrip("../"), category_name)
    return


def category_index(category_name):
    page = requests.get(url_category+category_name+'/index.html')
    soup = BeautifulSoup(page.content, 'html.parser')

    heading = "product_page_url; upc; title; price_including_tax; price_excluding_tax; availability; product_description; category; rating; cover_page_url"
    with open(category_path+'/'+category_name+".csv", "w") as file:
        file.write(heading + "\n")

    for livre in soup.find_all("h3"):
        for link in livre.find_all('a'):
            scrap_book_data(link.get('href').lstrip("../"), category_name)
    pagination = soup.find(class_="current")

    if pagination:
        pagination = str(pagination)
        pagination = pagination.split()[5]
        nb_page = int(pagination)
        for i in range(nb_page):
            category_page(category_name, str(i))
    return


page = requests.get(url_index)
soup = BeautifulSoup(page.content, 'html.parser')
getFirstUL = soup.find('ul', {"class": "nav-list"})
getUL = getFirstUL.find('ul')
BooksCategory = getUL.find_all('li')

for category in BooksCategory:
    for link in category.find_all('a'):
        category = link.get(('href')).split('/')[3]
        category_index(category)





