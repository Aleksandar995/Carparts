import re

from selenium.common.exceptions import NoSuchElementException
import selenium.common.exceptions
from time import sleep
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import requests

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

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

#######
# proxy = "189.84.122.34:8080"
# options.add_argument('--proxy-server=%s' % proxy)
#######
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
print(api_key[api_key.rindex('"') + 1:])

action = webdriver.ActionChains(driver)
see_all = driver.find_element_by_id("subCatSeeAll0")
action.move_to_element(see_all) \
    .click() \
    .perform()

WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "categories")))
sleep(1)
all_categories = driver.find_element_by_id("seeMoreCategories")
all_action = webdriver.ActionChains(driver)
width_all = all_categories.size["width"]
height_all = all_categories.size["height"]
all_action.move_to_element(all_categories).move_by_offset((width_all / 2) - 2, (height_all / 2) - 1).click().perform()

WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "categories")))
category = driver.find_element_by_id("categories").find_element_by_tag_name("a")

action2 = webdriver.ActionChains(driver)
action2.click(category) \
    .perform()

WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "categories")))
sleep(1)
category2 = driver.find_element_by_id("categories").find_element_by_tag_name("a")

action3 = webdriver.ActionChains(driver)
action3.click(category2) \
    .perform()

WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "sectionCard-0")))
sleep(1)
items = driver.find_element_by_id("sectionCard-0")

count_element = driver.find_element_by_id("topBarinformation")
count_sub = count_element.text[count_element.text.rindex("of"):]
count = re.findall('[0-9]+', count_sub)[0]

action4 = webdriver.ActionChains(driver)
action4.click(items) \
    .perform()


carparts_request = []
f = open("test2.txt", "a")
response_json = {}
i = 0
for request in driver.requests:
    if request.response:
        f.write(
            str(request.url) + "\n" +
            str(request.response.status_code) + "\n" +
            str(request.response.headers['Content-Type']) + '\n'
        )
        if "https://api.usautoparts.io/v1/pages?domain=carparts.com&" in str(request.url):
            carparts_request.append(str(request.url))
            if i == 2:
                print(request.url)
                response_json = json.loads(request.response.body)
                items = response_json['data']['products']['items']
            i = i + 1

for item in items:
    print(item['id'])
    print(item['sku'])


add_items_to_url = "&&itemperpage=" + count
my_url = carparts_request[-1]

final_url = my_url[:my_url.rindex('.com') + 4] + add_items_to_url + my_url[my_url.index('&'):]

print(final_url)
# header = {'apikey': api_key[api_key.rindex('"') + 1:]}
# r = requests.get(final_url, headers=header)
# print(r)

