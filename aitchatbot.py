import streamlit as st
import requests

# Function to read API keys safely
def get_api_key(service_name):
    try:
        return st.secrets[service_name]["api_key"]
    except KeyError:
        st.error(f"API key for {service_name} not found in secrets.")
        return None

nasa_api_key = get_api_key("nasa")
news_api_key = get_api_key("newsapi")
huggingface_api_key = get_api_key("huggingface")
huggingface_model_endpoint = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B"

# NASA API for space information
def get_space_info(api_key):
    if not api_key:
        return "NASA API key is missing."
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data[0]['title']}: {data[0]['explanation']}"
    return "No space information available."

# News API for latest research
def get_latest_research(api_key):
    if not api_key:
        return "News API key is missing."
    url = f"https://api.currentsapi.services/v1/search?apiKey={api_key}&keywords=AI"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json().get('news', [])
        if news_data:
            return f"{news_data[0]['title']}: {news_data[0]['description']}"
    return "No news available on this topic."

# Function to call the Hugging Face model API
def get_ai_response(api_key, model_endpoint, question):
    if not api_key:
        return "Hugging Face API key is missing."
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {"inputs": question}
    try:
        response = requests.post(model_endpoint, headers=headers, json=data)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        response_data = response.json()
        # Handle model output
        if isinstance(response_data, list) and len(response_data) > 0:
            generated_text = response_data[0].get("generated_text", "No text generated.")
            return generated_text
        return "Unexpected response format."
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
        elif any(keyword in user_input.lower() for keyword in ["ai", "agi", "asi"]):
            info = get_latest_research(news_api_key)
        elif "research" in user_input.lower():
            info = get_latest_research(news_api_key)
        else:
            info = "Sorry, I couldn't find information on that topic."

        # Generate a detailed response using the hosted LLaMA model
        prompt = f"{user_input} {info}"
        response = get_ai_response(huggingface_api_key, huggingface_model_endpoint, prompt)

        st.write(response)
    else:
        st.write("Please enter a question.")
