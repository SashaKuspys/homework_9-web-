import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor


# Функція для отримання інформації про авторів цитат
def get_author_info(author_url):
    author_page = requests.get(author_url)
    author_soup = BeautifulSoup(author_page.content, 'html.parser')

    born_date = author_soup.find('span', class_='author-born-date').text.strip()
    born_location = author_soup.find('span', class_='author-born-location').text.strip()
    description = author_soup.find('div', class_='author-description').text.strip()

    author_info = {
        'fullname': author_soup.h3.text.strip(),
        'born_date': born_date,
        'born_location': born_location,
        'description': description
    }

    return author_info


# Функція для отримання інформації про цитати
def scrape_quotes(base_url, quotes_data, page_number):
    page_url = f"{base_url}/page/{page_number}"
    page = requests.get(page_url)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            text = quote.find('span', class_='text').text.strip()
            author = quote.find('small', class_='author').text.strip()
            author_url = base_url + quote.find('a')['href']

            # Додавання цитати до списку
            quotes_data.append({
                'tags': [tag.text.strip() for tag in quote.find_all('a', class_='tag')],
                'author': author,
                'quote': text
            })

            # Отримання та додавання інформації про автора
            author_info = get_author_info(author_url)
            authors_data.append(author_info)
    else:
        print(f"Error accessing page {page_number}. Status code: {page.status_code}")


base_url = "http://quotes.toscrape.com"

quotes_data = []
authors_data = []

# Використання ThreadPoolExecutor для паралельного виконання запитів
with ThreadPoolExecutor() as executor:
    total_pages = 10

    # Виклик функції для скрапінгу цитат
    executor.map(lambda page: scrape_quotes(base_url, quotes_data, page), range(1, total_pages + 1))


with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)

print("Scraping completed. Data saved to quotes.json and authors.json.")
