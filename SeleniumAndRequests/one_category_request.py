import requests
import selenium
from selenium import webdriver
import selenium.common.exceptions
import re
from time import sleep


def get_api_key():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path='/Users/aleksandarmuzina/Downloads/chromedriver',
                                   options=options)

    driver.get("https://www.carparts.com/")
    sleep(2)

    try:
        captcha_button = driver.find_element_by_id("px-captcha")

        width = captcha_button.size["width"]
        height = captcha_button.size["height"]

        action = webdriver.ActionChains(driver)
        action.move_to_element(captcha_button) \
            .move_by_offset((width / 2) - 2, (height / 2) - 1) \
            .click_and_hold() \
            .pause(5) \
            .release() \
            .pause(5) \
            .perform()
    except selenium.common.exceptions.NoSuchElementException:
        pass

    page_source = driver.page_source
    api_key = re.findall('apikey\"\: \"[a-zA-Z]+', page_source)[0]
    return api_key[api_key.rindex('"') + 1:]


class Product(object):
    pass


header_mozila = {'User-Agent': 'PostmanRuntime/7.28.1',
                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                 'Accept-Encoding': 'gzip, deflate, br',
                 'Connection': 'keep-alive'}
real_headers = {'apikey': get_api_key()}
print(real_headers)

response = requests.get(
    'https://api.usautoparts.io/v1/pages?domain=carparts.com&&itemperpage=3&uri=/bumper-cover&absearch=u&blog=0&bot=0&getTools=0',
    timeout=90, headers=real_headers)
# print(response.request.headers)
# print(response)
r_json = response.json()

items = r_json['data']['products']['items']

for item in items:
    product = Product()

    product.id = item['id']
    product.sku = item['sku']
    product.sku_title = item['skuTitle']
    product.description = item['description']
    product.image = item['productImageUrl']
    product.regular_price = item['pricing']['regularPrice']

    dictionary = {
        "product": {"variants": [{"sku": product.sku, "price": product.regular_price}], "title": product.sku_title,
                    "body_html": product.description
            , "images": [{"src": product.image}]}}

    p = requests.post(
        'https://50b0cb2090d2f9aa42381512c4c87f41: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@carpartsdeploy.myshopify.com/admin/api/2021-04/products.json'
        , json=dictionary)
