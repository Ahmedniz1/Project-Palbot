import requests
import time
import os
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
def scrape_all_items(link):
    #scrape_page(link)
    driver = webdriver.Chrome()
    driver.get(link)
    items = []
    pages = driver.find_elements(By.CLASS_NAME,'page-nav-btn')
#        next_page = active_page.ne
#        page_list = active_page.find_element(By.CLASS_NAME,'page-nav-btn')
    for page in pages:
        page.click()
        WebDriverWait(driver, 5)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_items = scrape_page(soup)
        items.append(page_items)
#    print(pages)
    return items

def item_entry(item_dict,recipe=False):

    item = f'Item name:{item_dict["name"]}\nItem desc:{item_dict["desc"]}\nItem keys:{item_dict["keys"]}'
    if recipe:
        item = item+ f'Item recipe:{item_dict["recipe"]}'
    item = item.replace('\n\n\n','\n')
    item = item.replace('\n\n','\n')
    return item

def scrape_page(soup):

#    driver = webdriver.Chrome()
#    driver.get(link)
    bs_item_list = soup.find('section',class_ = 'items-list')
    item_with_recipes = bs_item_list.find_all('div',class_ = 'item')
    bs_items = []
    # remove all sections which are basically recipes to avoid multiple same sections
    for i in item_with_recipes:
        if i.find('div',class_ = 'up'):
            bs_items.append(i)
    items = []
    for i in (bs_items):
        recipe = False
        item_dict = {}
        item_dict['name'] = i.find('div',class_ = 'name').find('div',class_ = 'text').text
        item_dict['desc'] = i.find('div',class_ = 'description').text
        keys = i.find('div',class_ = 'keys').find_all('div',class_ = 'key')
        keys_info = '' 
        for key in keys:
            key_name = key.find('div',class_ = 'text').text
            key_value = key.find('div',class_ = 'value').text
            keys_info = keys_info + key_name+': '+key_value+'\n'
        item_dict['keys'] = keys_info
        recipe = i.find('div',class_ = 'recipe')
        if recipe is not None:
            bs_recipe_items = recipe.find_all('div',class_='item')
            recipe_items = ''
            for j in bs_recipe_items:
                recipe_text = j.find('div',class_ = 'name').text
#                print(recipe_text)
                recipe_value,recipe_name = recipe_text.split(' ',1)
                recipe_items = recipe_items + recipe_name+ ': '+recipe_value+'\n'
            item_dict['recipe'] = recipe_items
            recipe = True
        items.append(item_entry(item_dict,recipe))
#            print(item_dict)        

#    print(items)
#    save_items(items)
    return '\n\n'.join(items)
#    return items
def dict_to_str(dict):
    if 'recipe' in dict:
        return f'item name: {dict["name"]}\nitem description: {dict["desc"]}\nitem Stats:\n{dict["keys"]}\nitem recipe:{dict["recipe"]}'
    return f'item name: {dict["name"]}\nitem description: {dict["desc"]}\nitem Stats:\n{dict["keys"]}\n'

def save_items(items):
    for i in items:
        name = i['name'].replace(' ','_')
        item = dict_to_str(i)
        with open(f'./items/{name}.txt','w',encoding='utf-8') as file:
            file.write(item)
def make_item_file():
    items = os.listdir('./items/')
    print(len(items))
    data = ''
    for item in items:
        with open(f'./items/{item}','r') as file:
            lines = file.readlines()
            lines = ''.join(lines)
            print(lines)
            lines = lines.replace('\n\n\n','\n')
            lines = lines.replace('\n\n','\n')
            print(lines)
            data = data+lines+'\n'
    with open(f'./items.txt','w',encoding='utf-8') as file:
        file.write(data)

# def make_item_file ():
#     items = os.listdir('./items/')
#     for item in items:
#            break
#    print(bs_items[2].find('div',class_ = 'item'))    
#    for i in range(10):
#        print(items[i],'\n\n\n')
#    print(items[:10])

#link = 'https://palworld.gg/items'
#scrape_all_items(link)
#make_item_file()