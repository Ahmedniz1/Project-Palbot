# Project Palbot

This is a Github repository to build a RAG based agent for the game called Palbot.
The goal of building the chatbot was to have a single chatbot to answer all queries regarding Palbot game, which included pals, items and detail combinations.

## Data Collection

For getting relevant data related to Palworld game, following were my data sources.</br>
Pals: https://palworld.fandom.com/wiki/Paldeck</br>
Items: https://palworld.gg/items</br>
Pal Breed: https://www.rockpapershotgun.com/palworld-breeding-combos

## Embeddings
For the embeddings, I used the **all-MiniLM-L6-v2** model for creating embeddings. For storing the embeddings, I used **chromadb** and stored the embeddings locally on my drive.

## Query Response

I have used the **openAI 3.5 turbo instruct** model to generate answer from the most similar embeddings. 

## UI
I've used streamlit for a very simple UI.

