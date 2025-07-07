import streamlit as st
import requests
from bs4 import BeautifulSoup
from ollama import chat
import googlesearch

st.set_page_config(page_title="AI Agent Chatbot")

# Wikipedia function
def wikiSummary(query):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
    r = requests.get(url)
    return r.json().get('extract') if r.status_code == 200 else None

# DuckDuckGo function
def duckduckSummary(query):
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    r = requests.get(url)
    data = r.json() if r.status_code == 200 else {}
    return data.get('Abstract') or (data.get('RelatedTopics', [{}])[0].get('Text'))

# Google scraping function
def googleSummary(query, max_results=5):
    for url in googlesearch.search(query, num_results=max_results):
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = "\n".join(p.get_text() for p in paragraphs if len(p.get_text().split()) > 30)
            if text:
                return text, url
        except Exception:
            continue
    return None, None

# Function to generate response using Ollama
def chatbotResponse(user_input, source):
    if source == "Wikipedia":
        info = wikiSummary(user_input)
    elif source == "DuckDuckGo":
        info = duckduckSummary(user_input)
    elif source == "Google":
        info, url = googleSummary(user_input)
        if info:
            prompt = f"You are an intelligent assistant. Use content from this page ({url}) to answer:\n\n{info}"
            res = chat(model='llama3.1:latest', messages=[{'role': 'user', 'content': prompt}])
            return res['message']['content']
        else:
            return "No scrapable content found on Google results."
    else:
        info = None

    prompt = f"You are an assistant. Use this info to answer:\n\n{info or user_input}"
    res = chat(model='llama3.1:latest', messages=[{'role': 'user', 'content': prompt}])
    return res['message']['content']

# Streamlit UI
st.title("AI Agent Chatbot (Wiki / DuckDuckGo / Google / Ollama)")

# Source selection
source = st.selectbox("Choose source:", ["Wikipedia", "DuckDuckGo", "Google", "Ollama"])

# Dynamic placeholder based on selected source
placeholder_map = {
    "Wikipedia": "Type a topic...",
    "DuckDuckGo": "Type a search query...",
    "Google": "Type your question for Google...",
    "Ollama": "Type your question..."
}

# Initialize session state input
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Handle input processing
def processInput():
    q = st.session_state.user_input.strip()
    if q:
        with st.spinner("Thinking..."):
            st.session_state.answer = chatbotResponse(q, source)

# Input field (triggers on Enter)
st.text_input("Your input:", key="user_input", placeholder=placeholder_map[source], on_change=processInput)

# Optional: manual trigger button
if st.button("Get Answer"):
    processInput()

# Display response
if "answer" in st.session_state:
    st.markdown("### Answer:")
    st.write(st.session_state.answer)
