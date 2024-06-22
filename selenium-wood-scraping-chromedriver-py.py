import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from chromedriver_py import binary_path

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    service = Service(executable_path=binary_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(5)  # Respect Crawl-delay: 5

def scrape_wood_database(url):
    driver = setup_driver()
    driver.get(url)
    
    scroll_to_bottom(driver)
    
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    woods = []
    for wood in soup.find_all('div', class_='col-md-6'):
        name = wood.find('strong').text.strip()
        scientific_name = wood.find('em').text.strip()
        try:
            image_url = wood.find('img')['src']
            woods.append({'name': name, 'scientific_name': scientific_name, 'image_url': image_url})
        except TypeError:
            pass
    
    driver.quit()
    return woods

def download_images(woods, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for wood in woods:
        image_url = wood['image_url']
        extension = image_url.split('.')[-1]
        image_name = f"{wood['name'].replace(' ', '_')}.{extension}"
        image_path = os.path.join(output_dir, image_name)
        
        response = requests.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(response.content)
        
        time.sleep(5)  # Respect Crawl-delay: 5

    print(f"Downloaded {len(woods)} wood images to {output_dir}")

url = 'https://www.wood-database.com/wood-filter/'
output_dir = 'wood_images'

woods = scrape_wood_database(url)
download_images(woods, output_dir)

# Create a class mapping file
with open('class_mapping.txt', 'w') as f:
    for i, wood in enumerate(woods):
        f.write(f"{i} {wood['name']}\n")

print(f"Created class mapping file with {len(woods)} wood types")
