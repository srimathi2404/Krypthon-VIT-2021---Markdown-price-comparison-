from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)


chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")

chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the WebDriver with the options
# DOWN LOAD CHROME DRIVER AND SET IT UP
webdriver_service = Service('chromedriver PATH') 
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def FLIPKART(search_query):
    search_url = f"https://www.flipkart.com/search?q={search_query}"
    driver.get(search_url)
    time.sleep(3)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product = soup.find('a', {'class': '_1fQZEK'})
    if product:
        product_name = product.find('div', {'class': '_4rR01T'}).text if product.find('div', {'class': '_4rR01T'}) else 'N/A'
        price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text if product.find('div', {'class': '_30jeq3 _1_WHN1'}) else 'N/A'
        rating = product.find('div', {'class': '_3LWZlK'}).text if product.find('div', {'class': '_3LWZlK'}) else 'N/A'
        reviews = product.find('span', {'class': '_2_R_DZ'}).text if product.find('span', {'class': '_2_R_DZ'}) else 'N/A'
        return {"Product Name": product_name, "Price": price, "Rating": rating, "Reviews": reviews}
    return None

def AMAZON(search_query):
    search_url = f"https://www.amazon.in/s?k={search_query}"
    driver.get(search_url)
    time.sleep(3)  # Wait for the page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product = soup.find('div', {'class': 's-main-slot s-result-list s-search-results sg-row'}).find('div', {'data-component-type': 's-search-result'})
    if product:
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text if product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}) else 'N/A'
        price = product.find('span', {'class': 'a-price-whole'}).text if product.find('span', {'class': 'a-price-whole'}) else 'N/A'
        rating = product.find('span', {'class': 'a-icon-alt'}).text if product.find('span', {'class': 'a-icon-alt'}) else 'N/A'
        reviews = product.find('span', {'class': 'a-size-base'}).text if product.find('span', {'class': 'a-size-base'}) else 'N/A'
        return {"Product Name": product_name, "Price": price, "Rating": rating, "Reviews": reviews}
    return None

def SNAPDEAL(search_query):
    search_url = f"https://www.snapdeal.com/search?keyword={search_query}"
    driver.get(search_url)
    time.sleep(3)  

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    product = soup.find('div', {'class': 'product-tuple-listing'})
    if product:
        product_name = product.find('p', {'class': 'product-title'}).text if product.find('p', {'class': 'product-title'}) else 'N/A'
        price = product.find('span', {'class': 'lfloat product-price'}).text if product.find('span', {'class': 'lfloat product-price'}) else 'N/A'
        rating = product.find('div', {'class': 'filled-stars'}).get('style') if product.find('div', {'class': 'filled-stars'}) else 'N/A'
        rating = rating.split(":")[1] if rating != 'N/A' else rating
        reviews = product.find('p', {'class': 'product-rating-count'}).text if product.find('p', {'class': 'product-rating-count'}) else 'N/A'
        return {"Product Name": product_name, "Price": price, "Rating": rating, "Reviews": reviews}
    return None





@app.route('/', methods=['GET', 'POST'])
def index():
    flipkart_details = None
    amazon_details = None
    snapdeal_details = None
    if request.method == 'POST':
        product = request.form.get('product')
        flipkart_details = FLIPKART(product)
        amazon_details = AMAZON(product)
        snapdeal_details = SNAPDEAL(product)

    return render_template('index.html', flipkart_details=flipkart_details, amazon_details=amazon_details, snapdeal_details=snapdeal_details)

if __name__ == '__main__':
    app.run(debug=True)
