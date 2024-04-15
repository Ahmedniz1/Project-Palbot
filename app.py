import os
import streamlit as st

from dotenv import load_dotenv
from io import BytesIO
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from utils import save_embeddings,create_collection,response_query,create_data_file


load_dotenv()
collection = create_collection()
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

def app():
    st.header("Paldex")
    user_input = st.text_area(
        "Enter your text prompt below and click the button to submit."
    )

    # Button 1
    if st.button("Generate text"):
        response = response_query(user_input,collection,model,client).lstrip().rstrip()
        st.text_area(label ="",value=response+'\n\n', height =200)

    # Button 2
    if st.button("Scrape Data"):
        create_data_file()
        st.write("Data File created!")

    # Button 3
    if st.button("Create Embeddings"):
        save_embeddings('./data.txt',collection,model)
        st.write("Embeddings created!")



#    save_embeddings('./data.txt',collection,model)

if __name__ == "__main__":
    app()