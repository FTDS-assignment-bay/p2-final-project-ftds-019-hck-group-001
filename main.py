import streamlit as st
from pymongo import MongoClient
import urllib, io, json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "INPUT YOUR API KEY" # input API key

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

# MongoDB Atlas setup
username = "notbeekay"
pwd = "brenda123"
client = MongoClient("mongodb+srv://" + urllib.parse.quote(username) + ":" + urllib.parse.quote(pwd) + "@cluster1.esrw4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
db = client["final-project"]
collection = db["locations"]

st.title("SpotSnap: Southeast Asia Travel Recommender Chatbot")
# Display the image
st.image("spotsnap.png", caption="Ask anything about your travel destination and we'll provide you the information!")
input = st.text_area("Enter your question here")

with io.open("sample.txt", "r", encoding="utf-8") as f1:
    sample = f1.read()

prompt = """
You are a highly intelligent AI assistant, an expert in identifying and recommending travel destinations in Southeast Asia based on user input. Your task is to provide detailed responses in complete sentences, including recommendations, descriptions, and relevant information about various destinations.

Please use the schema below to inform your responses, but focus on crafting engaging narratives rather than returning MongoDB aggregation pipeline queries. Make sure the website links can be accessed.
Make sure your responses are in the form of sentences, not json.

Here’s a breakdown of the schema with descriptions for each field:

1. **_id**: Unique identifier for the place.
2. **name**: Name of the place.
3. **address**: Address of the place.
4. **location**: The longitude (lng) and latitude (lat) of the place.
5. **rating**: Measure of how good the place is out of 5.
6. **types**: The categories the place is classified as, such as spa, restaurant, or amusement park.
7. **city**: The city where the place is located.
8. **place_type**: The main purpose of the place (e.g., amusement park).
9. **business_status**: Indicates if the place is temporarily closed, permanently closed, or operating.
10. **current_opening_hours**: The current opening hours of the place.
11. **formatted_phone_number**: Contact phone number for the place.
12. **photos**: Pictures of the place.
13. **price_level**: Price category ranging from 0 (Free) to 4 (Very Expensive).
14. **website**: Official website URL for more information.

This schema provides a comprehensive view of the data structure for travel destinations, adding depth to your recommendations. Use the following sample questions to guide your responses.


Sample question: {sample}

Please provide clear, informative recommendations based on the user’s question: {question}

"""

query_with_prompt = PromptTemplate(
    template=prompt,
    input_variables=["question", "sample"]
)

llmchain = LLMChain(llm=llm, prompt=query_with_prompt, verbose=True)

if input:
    button = st.button("Submit")
    if button:
        response = llmchain.invoke({
            "question": input,
            "sample": sample
        })

        # Check if the response is valid and display it
        if response and "text" in response:
            st.write(response["text"])  # Display the response directly
        else:
            st.error("No response from the model.")
