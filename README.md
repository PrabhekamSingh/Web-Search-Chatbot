# Web-Search-Chatbot
# Gemini Web Search Chatbot

A Streamlit-based chatbot powered by Google's Gemini LLM and enhanced with real-time web search using Tavily. The app demonstrates conversational AI with tool use, session memory, and a modern chat UI.

---

## Features

- **Conversational AI**: Uses Gemini (`gemini-2.0-flash-exp`) via LangChain/Langgraph for natural language chat.
- **Web Search Tool**: Integrates Tavily for up-to-date web search results.
- **Session Memory**: Remembers conversation history per user session.
- **Modern UI**: Chat bubbles, theme toggles (Day/Night/Reading), and multipage navigation.
---

## Setup

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd streamlit\ basic_chatbot
```

### 2. Create and activate a virtual environment (recommended)

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```sh
pip install -r requirements.txt
```

### 4. Set up API keys

Create a `.env` file in the project root with your keys:

```
GOOGLE_API_KEY="your-google-api-key"
TAVILY_API_KEY="your-tavily-api-key"
```

---

## Usage

Start the Streamlit app:

```sh
streamlit run frontend.py
```

- Use the sidebar to switch between **Chatbot** and **About** pages.
- Select Day/Night/Reading mode for your preferred reading experience.
- Chat with the bot and get real-time web search answers.

---

## File Structure

```
streamlit basic_chatbot/
│
├── backend.py       # LangGraph workflow, Gemini LLM, and tool logic
├── frontend.py      # Streamlit UI and chat logic
├── requirements.txt # Python dependencies
├── .env             # API keys (not tracked by git)
├── README.md        # Project documentation
└── .gitignore
```

---

## Credits

- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
- [Tavily Search](https://www.tavily.com/)

---

## Support

If you find this project useful, consider [buying me a coffee](https://www.buymeacoffee.com/YOUR_USERNAME)! ☕
