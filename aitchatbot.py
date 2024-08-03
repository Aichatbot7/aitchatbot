import streamlit as st
import requests

# Fetch secrets
nasa_api_key = st.secrets.get("nasa", {}).get("api_key", "")
currents_api_key = st.secrets.get("currentsapi", {}).get("api_key", "")
huggingface_api_key = st.secrets.get("huggingface", {}).get("api_key", "")
huggingface_model_endpoint = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"

# NASA API for space information
def get_space_info(api_key):
    if not api_key:
        return "NASA API key is missing."
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0]['title'] + ": " + data[0]['explanation']
    return "No space information available."

# Currents API for news
def get_latest_news(api_key, query):
    if not api_key:
        return "Currents API key is missing."
    url = f"https://api.currentsapi.services/v1/search?apiKey={api_key}&keywords={query}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json().get('news', [])
        if news_data:
            return news_data[0]['title'] + ": " + news_data[0]['description']
    return "No news available on this topic."

# arXiv API for latest research
def get_latest_research(query="AI"):
    url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return "No research information available."

# Function to call the Hugging Face model API
def get_llama_response(prompt):
    if not huggingface_api_key:
        return "Hugging Face API key is missing."
    headers = {
        "Authorization": f"Bearer {huggingface_api_key}",
        "Content-Type": "application/json",
    }
    data = {"inputs": prompt}
    try:
        response = requests.post(huggingface_model_endpoint, headers=headers, json=data)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        return response.json()[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"

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
            info = get_latest_news(currents_api_key, "AI")
        elif "research" in user_input.lower():
            info = get_latest_research("AI")
        else:
            info = "Sorry, I couldn't find information on that topic."

        # Generate a detailed response using the hosted LLaMA model
        prompt = user_input + " " + str(info)
        response = get_llama_response(prompt)

        st.write(response)
    else:
        st.write("Please enter a question.")
