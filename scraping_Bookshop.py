import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

# Base URL of the website
base_url = "http://books.toscrape.com/"

# Open a CSV file for writing
with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Rating"])  # Write header

    # Function to scrape a single page
    def scrape_page(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all book containers
        books = soup.find_all("article", class_="product_pod")
        
        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating = book.p["class"][1]  # The rating is in the second class name
            writer.writerow([title, price, rating])  # Write row

    # Function to scrape all pages
    def scrape_all_pages():
        page_url = base_url
        while True:
            print(f"Scraping page: {page_url}")
            scrape_page(page_url)
            
            # Check if there's a next page
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")
            next_button = soup.find("li", class_="next")
            
            if next_button:
                next_page = next_button.a["href"]
                page_url = urljoin(page_url, next_page)  # Correctly join the URL
            else:
                break
            time.sleep(1)  # Add a delay to avoid overloading the server

    # Start scraping
    scrape_all_pages()
