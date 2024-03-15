from flask import Flask, request, jsonify
from flasgger import Swagger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import json
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)  # initialize a flask application
CORS(app)

# Initialize flasgger 
app.config['SWAGGER'] = {
    'title': 'Price Predictor microservice API',
    'version': 1.0,
    "openapi": "3.0.2",
    'description': 'Retrieve current market price of watch'
}
swagger = Swagger(app)
  
def scrape_chrono24(ref_number, manufacturer_id, year, currency="SGD"):
    options = Options()
    options.add_argument('--headless')  # Set Chrome to run in headless mode
    driver = webdriver.Chrome(options=options)

    ref_number_extra = None
    
    if manufacturer_id == "221":
      ref_number_extra = 24221
    elif manufacturer_id == "18":
      ref_number_extra = 2418
    elif manufacturer_id == "194":
      ref_number_extra = 24194
      
    
    # Chrono24 Website URL
    chrono24_url = f"https://www.chrono24.sg/search/index.htm?currencyId={currency}&dosearch=true&manufacturerIds={manufacturer_id}&maxAgeInDays=0&pageSize=60&redirectToSearchIndex=true&referenceNumber={ref_number}%{ref_number_extra}&resultview=list&searchexplain=1&sortorder=0&usedOrNew=used&year={year}&specials=103"

    driver.get(chrono24_url)

    # Wait for the "OK" button to be clickable
    ok_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "js-cookie-accept-all"))
    )

    # Click on the "OK" button
    ok_button.click()

    # Add a delay to ensure the page loads completely
    time.sleep(3)

    # Get the page source after waiting for dynamic content to load
    content = driver.page_source

    # Pass the page source to BeautifulSoup for parsing
    soup = BeautifulSoup(content, 'html.parser')

    # Find the element containing the year of production
    article_item_containers = soup.find_all("div", class_="article-item-container")

    # Array to store scraped watch objects
    scraped_watches_arr = []

    for item in article_item_containers:
        item_infos = item.find_all("strong")
        watch_manufacturer = item.find("a").get("data-manufacturer")
        watch_movement_type = item_infos[0].text.strip()
        watch_case_material = item_infos[1].text.strip()
        watch_year_of_production = item_infos[2].text.strip()
        watch_condition = item_infos[3].text.strip()
        watch_ref_number = item_infos[4].text.strip()
        watch_case_diameter = item_infos[7].text.strip()

        watch_price = item.find("div", class_="text-md text-sm-xlg text-bold").text.strip()
        watch_price = re.sub(r'[^\d.]', '', watch_price) + ".00"
        
        if watch_price == "Price on request" or float(watch_price) == 0.0:
            continue
        else: 
            watch_object = {
                "watch_manufacturer": watch_manufacturer,
                "watch_movement_type": watch_movement_type,
                "watch_case_material": watch_case_material,
                "watch_year_of_production": watch_year_of_production,
                "watch_condition": watch_condition,
                "watch_ref_number": watch_ref_number,
                "watch_case_diameter": watch_case_diameter,
                "watch_price": float(watch_price)
            }
            scraped_watches_arr.append(watch_object)

    # Close the WebDriver
    driver.quit()

    # Calculate mean, max, min of watch prices
    watch_prices = [watch['watch_price'] for watch in scraped_watches_arr]
    mean_price = 0
    max_price = 0
    min_price = 0

    # Check if watch_prices is not empty before calculating mean, max, min
    if watch_prices:
        mean_price = round(sum(watch_prices) / len(watch_prices), 2) 
        max_price = max(watch_prices)
        min_price = min(watch_prices)

    # Add mean, max, min and total number of watches as keys in JSON
    json_data_with_stats = {
        "average_price": mean_price,
        "lowest_price": min_price,
        "highest_price": max_price,
        "num_of_watches": len(scraped_watches_arr),
        "watches": scraped_watches_arr
    }

    return json_data_with_stats

@app.route('/scrape', methods=['GET'])
def scrape():
    """
    Get current market price of auctioned watch.
    ---
    parameters:
      - name: ref_number
        in: query
        type: string
        required: true
        description: Reference number of the watch
      - name: manufacturer_id
        in: query
        type: integer
        required: true
        description: Manufacturer ID of the watch
      - name: year
        in: query
        type: integer
        required: true
        description: Year of production of the watch
    responses:
      200:
        description: Return all prices found on the web for this watch
      500:
        description: Internal server error
    """
    ref_number = request.args.get('ref_number')
    # ref_number_extra = request.args.get('ref_number_extra')
    manufacturer_id = request.args.get('manufacturer_id')
    year = request.args.get('year')
    
    # ref_number_extra = None
      
    if not (ref_number and manufacturer_id and year):
        return jsonify({'error': 'Please provide all parameters: ref_number, manufacturer_id, year'})
    try:
        result = scrape_chrono24(ref_number, manufacturer_id, year)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=5008, debug=True)
