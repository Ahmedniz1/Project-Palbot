import requests

from bs4 import BeautifulSoup

def scrape_breed_combinations(url):
    response = requests.get(url)
    print(response)
    breed_combinations = ''
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
    # Find all h3 tags as all breeding combinations are in h3 tag
    for h3_tag in soup.find_all('h3'):
        # Find the next sibling tag (the <ul> tag) of the h3 tag
        title = h3_tag.text.lstrip().rstrip()
        ul_tag = h3_tag.find_next_sibling('ul')
        if ul_tag:
            pal_combination = ul_tag.text.lstrip().rstrip()
            breed_combinations += f'{title}\n{pal_combination}\n\n'
#    print(breed_combinations)
    return breed_combinations
#scrape_breed_combinations('https://www.rockpapershotgun.com/palworld-breeding-combos')