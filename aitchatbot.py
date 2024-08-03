import streamlit as st
import requests

# Read API keys from Streamlit secrets
nasa_api_key = st.secrets["nasa"]["api_key"]
news_api_key = st.secrets["newsapi"]["api_key"]
huggingface_api_key = st.secrets["huggingface"]["api_key"]
huggingface_model_endpoint = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"

# NASA API for space information
def get_space_info(api_key, query="space"):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count=1"
    response = requests.get(url)
    data = response.json()
    return data[0] if response.status_code == 200 else {}

# NewsAPI for AI, AGI, ASI
def get_latest_news(api_key, query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get('articles', [])

# arXiv API for latest research
def get_latest_research(query="AI"):
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=1"
    response = requests.get(url)
    return response.text if response.status_code == 200 else {}

# Function to call the Hugging Face model API
def get_llama_response(prompt):
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}",
        "Content-Type": "application/json",
    }
    data = {"inputs": prompt}
    response = requests.post(huggingface_model_endpoint, headers=headers, json=data)
    return response.json()[0]["generated_text"] if response.status_code == 200 else "Error fetching response"

# Streamlit app
st.title("Advanced Chatbot")
st.write("Ask me anything about Space, AI, AGI, ASI, or the latest research!")

user_input = st.text_input("Your question:")
if st.button("Get Response"):
    if user_input:
        # Fetch relevant information based on the user query
        if "space" in user_input.lower():
            info = get_space_info(nasa_api_key)
        elif "ai" in user_input.lower() or "agi" in user_input.lower() or "asi" in user_input.lower():
            info = get_latest_news(news_api_key, "AI")
        elif "research" in user_input.lower():
            info = get_latest_research("AI")
        else:
            info = {"message": "Sorry, I couldn't find information on that topic."}

        # Generate a detailed response using the hosted LLaMA model
        prompt = user_input + " " + str(info)
        response = get_llama_response(prompt)

        st.write(response)
