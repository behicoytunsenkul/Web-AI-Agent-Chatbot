![Screenshot 2025-07-07 at 23 49 53](https://github.com/user-attachments/assets/3f79d42b-017f-4317-93a7-5be19e8f0f2b)
# Agent Chatbot

An intelligent multi-source chatbot interface powered by large language models and real-time information retrieval from public web sources. This application uses [Streamlit](https://streamlit.io/) to provide an interactive UI for asking questions and receiving contextual answers based on user-selected knowledge sources.

---

## Features

- **Dynamic Source Selection**: Users can choose from multiple information providers:
  - **Wikipedia**: Extracts summaries using the official REST API.
  - **DuckDuckGo**: Uses DuckDuckGo Instant Answer API for fast, zero-click responses.
  - **Google**: Scrapes content from top-ranked search results using a real-time agent pattern.
  - **Ollama LLM**: Answers directly from a locally running LLM (e.g., LLaMA 3).

- **Autonomous Agent Behavior**: When Google is selected as the source, the system:
  - Performs a live web search.
  - Iteratively scans the top result pages.
  - Scrapes readable content (e.g., paragraphs).
  - Sends the cleaned context to the LLM for synthesis.
  - Automatically falls back to alternative links if scraping is blocked.

- **Contextual Prompting**: Retrieved information is framed into natural language prompts and submitted to the LLM for best-possible answer generation.

- **Local LLM Integration**: Compatible with [Ollama](https://ollama.com/) models such as `llama3.1`, running on local machines.

---

## System Architecture

```mermaid
graph TD
    UI[Streamlit Web UI] --> Q[User Question]
    Q -->|Source: Wikipedia| Wiki[Wikipedia REST API]
    Q -->|Source: DuckDuckGo| DDG[DuckDuckGo API]
    Q -->|Source: Google| G[Google Search + Web Scraping]
    G --> BS[BeautifulSoup for Parsing]
    Wiki --> C[Context Builder]
    DDG --> C
    BS --> C
    C --> LLM[Ollama LLM (local)]
    LLM --> A[Final Answer]
    A --> UI

## How To Running

```bash
streamlit run main.py
