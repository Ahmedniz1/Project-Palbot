import requests
import time
import os
from bs4 import BeautifulSoup

def pal_entry(pal):
    return f'Pal Name:{pal["name"]}\
    \n{pal["name"]} Number:{pal["num"]}\
    \n{pal["name"]} Element:{pal["element"]}\
    \n{pal["name"]} Drop:{pal["drops"]}\
    \n{pal["name"]} Food:{pal["food"]}\
    \n{pal["name"]} Location:{pal["location"]}\
    \n{pal["name"]} Skill:{pal["skill"]}:{pal["skill description"]}\
    \n{pal["name"]} Work Suitability:{pal["work"]}\
    \n{pal["name"]} Movelist:{pal["movelist"]}'

def save_file(data,name, path = ''):
        filepath = os.path.join(path, f"{name}.txt")
        with open(filepath, 'w', encoding='utf-8') as file:
           file.write(data)


def read_file(pal_links):
    with open(pal_links, 'r') as file:
        return file.readlines()

def capture_pal_details(url):
    pal = {}
    response = requests.get(url)
    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        #Extracting name of Pal
        pal_name = soup.find(class_= 'mw-page-title-main').text.lstrip().rstrip()
        pal['name']=pal_name
        pal_page = soup.find('div',class_= 'mw-parser-output')
        pal_sections = list(pal_page.find_all('section',class_='pi-item pi-group pi-border-color'))
        pal_stats = pal_sections[0].find_all('div','pi-item pi-data pi-item-spacing pi-border-color')
        #pal number, element, drops, food
        pal['num'] = pal_stats[0].find('div',class_='pi-data-value pi-font').text.lstrip().rstrip()
        pal['element'] = pal_stats[1].find('div',class_='pi-data-value pi-font').text.lstrip().rstrip()

        temp_pal_drops = (pal_stats[2].find_all('span'))
        pal_drops = []
        for drops in temp_pal_drops:
            pal_drops.append(drops.text.lstrip().rstrip())
        pal_drops =sorted(list(set(pal_drops)))
        pal['drops'] = ', '.join(map(str, pal_drops))
        food_val = pal_stats[3].find_all('img',alt = 'Food on icon')
        if food_val !=None:
            pal['food']=len(pal_stats[3].find_all('img',alt='Food on icon'))
        #updating pal drops
            
        #pal food required
        #pal skill
        pal['skill'] = pal_sections[1].find('div',class_='pi-item pi-data pi-item-spacing pi-border-color').text.lstrip().rstrip()
        pal['skill description'] = pal_sections[1].find('div',class_='pi-smart-data-value pi-data-value pi-font pi-item-spacing pi-border-color',attrs={'data-source': 'psdesc'}).text.lstrip().rstrip()
        #pal work
        work_type = list(pal_sections[4].find_all('a'))
        pal_work = []
        for work in work_type:
            pal_work.append(work.find_next('b').text)
        pal['work'] = ', '.join(map(str, pal_work))
        movelist=[]
        move_table = list(pal_page.find('table', class_='fandom-table').find_all('tr'))        
        for i in range (0,len(move_table),2):
            move_details = move_table[i].text
            move_details = '\n'.join(line.strip() for line in move_details.splitlines() if line.strip()).splitlines()
            req_lvl = move_details[0].split(' ')[-1]
            restore_time = move_details[2].split(' ')[-1]
            power = move_details[3].split(' ')[-1]
            move_record = f'Move Name: {move_details[1]}\nRequired Level:{req_lvl}\nRestore Time:{restore_time}\nMove Power:{power}'
            movelist.append(move_record)
        pal['movelist'] = '\n'.join(map(str, movelist))
        return pal


def get_pal_links(url):
    links = []
    response = requests.get(url) # get the request page and make sure response is 200
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')    

        # find registed and subspecie pals based on tbody tag
        body = soup.find('tbody')
        registered_pals = list(soup.find('tbody').find_all('tr'))[1:]
        subspecies_pals = list(body.find_next('tbody').find_all('tr'))[1:]

        subspecies_pal_list = []
        #Extract the pal number of each subspecie pal
        for i in subspecies_pals:
            subspecies_pal_list.append((int(i.find_all('td')[0].text[:-2])))

        links = ''
        idx = 0
        #save pals in numeric order of both list. ie: 12 jolthog, jolthog_cryst
        for i in range(len(registered_pals)):
            pal_link ='https://palworld.fandom.com/'+registered_pals[i].find_all('td')[2].find('a').get('href')
            links = links+pal_link+'\n'
            if idx<len(subspecies_pal_list):
                if subspecies_pal_list[idx]== i+1:
                    pal_link ='https://palworld.fandom.com/'+subspecies_pals[idx].find_all('td')[2].find('a').get('href')
                    links = links + pal_link +'\n'
                    idx+=1
#        save_file(links,'pal_links')
        return links


def scrape_locations():
    url = 'https://game8.co/games/Palworld/archives/442159'
    response = requests.get(url) # get the request page and make sure response is 200
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        #find pal table, and get pal name and its location in a dictionary
        pals = soup.find('tbody').find_all('tr')
        locations = {}
        for i in pals:
            data = i.find_all('td')
            locations [data[1].text] = data[-1].text.lstrip().rstrip()
        return locations

def scrape_paldex(pal_links):
#    pal_links = read_file(pal_file)
    
    location = scrape_locations()
    pals = []
    for i in range(len(pal_links)-1):
#        print(i,pal_links[i],'hahaha')
        pal = capture_pal_details(pal_links[i])
        if pal['name'] in location:
            pal['location'] = location[pal['name']]
        else:
            pal['location'] = 'unknown'
        pal_page = pal_entry(pal)
#        save_file(pal_page,pal['name'],'paldex2')
        pals.append(pal_page)
    return pals
def create_paldex_file():
    pal_list =os.listdir('paldex/') 
    paldex = ''
    for pal in pal_list:
        pal_data = read_file('paldex2/'+pal)
        pal_data = ''.join(pal_data)
        paldex+=pal_data
        paldex+='\n\n'
    save_file(paldex,'paldex1')

link = 'https://palworld.fandom.com/wiki/Paldeck'
#get_pal_links(link)
#scrape_locations()
#scrape_paldex('pal_links.txt')
#create_paldex_file()
#update_paldex('Palworld all data/paldex.txt')

