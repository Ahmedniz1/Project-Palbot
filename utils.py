import chromadb
import os

from scrape_items import scrape_all_items
from scrape_pals import get_pal_links,scrape_paldex
from scrape_breed import scrape_breed_combinations
def create_collection():
    client = chromadb.PersistentClient(path="./embeddings/")
    collection = client.get_or_create_collection(name="palworld")
    return collection

def create_embedding(data,model):
    embeddings = model.encode(data)
    return [embedding.tolist() for embedding in embeddings]

def load_file(path):
    with open(path, 'r',encoding='utf-8') as file:
        data = file.readlines()
    data = ''.join(data)
    return data

def save_embeddings(path,collection,model):
    data = load_file(path)
    records = data.split('\n\n')
    record_embeddings = create_embedding(records,model)
    total_records = (len(record_embeddings)//100) +1
    for i in range(total_records):
        if i<total_records-1:
            ids = [f'{j}' for j in range(i*100,(i+1)*100)]
        if i==total_records-1:
            ids = [f'{j}' for j in range(i*100,len(record_embeddings))]
        collection.add(documents = records[i*100:(i+1)*100],embeddings =record_embeddings[i*100:(i+1)*100], ids = ids)
    return True

def response_query(query,collection,model,client):
    query_embeddings = create_embedding(query,model)
    query_result = collection.query(query_embeddings=query_embeddings,n_results=2)
    top_documents = query_result['documents'][0]
    top_documents = '\n'.join(top_documents)
    llm_query = f'You are a chatbot called Palbot. You answer queries regarding the game palbot. Answer the question from the information given below.\nQuestion: {query}\n Information\n{top_documents}'
    response = client.completions.create(model="gpt-3.5-turbo-instruct",prompt=llm_query,temperature = 0.1,max_tokens = 300)
    return response.choices[0].text

def save_file(data,name, path = ''):
        filepath = os.path.join(path, f"{name}.txt")
        with open(filepath, 'w', encoding='utf-8') as file:
           file.write(data)

def create_data_file():
    pal_link = 'https://palworld.fandom.com/wiki/Paldeck'
    item_link = 'https://palworld.gg/items'
    breed_link = 'https://www.rockpapershotgun.com/palworld-breeding-combos'
    pal_links = get_pal_links(pal_link).split('\n')
    print('Extracting pal details')
    pals = scrape_paldex(pal_links)
    print('Extracting item details')
    items = scrape_all_items(item_link)
    print('Extracting breeding combinations')
    breed_combinations = scrape_breed_combinations(breed_link)
    data = 'Pals\n\n'
    data = data + '\n\n'.join(pals)
    data = data + '\n\nItems\n\n'
    data = data + '\n\n'.join(items)
    data = data + '\n\nBreed \n\n'
    data = data + breed_combinations
    save_file(data ,'data')



