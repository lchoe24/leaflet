# 🍃 Leaflet

**Where thoughts come to rest** — An AI-powered journaling companion that helps you reflect, explore, and grow.

## Features

- **Guided Journaling**: Three modes — Reflective (AI analyzes patterns), Explore (random prompts), Free Write
- **Conversational Flow**: Chat-like UI with Leafy, your AI companion
- **Weekly Garden**: Visual streak tracker that grows as you journal
- **Mood Insights**: Track mood patterns over 30 days with AI-generated summaries
- **Daily Challenges**: Personalized micro-challenges based on your entries

## Setup

### 1. Clone & Navigate
```bash
git clone https://github.com/lchoe24/leaflet.git
cd leaflet
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. (Optional) Populate Demo Data
```bash
python scripts/populate_demo.py
```
> ⚠️ **Warning:** This script wipes all existing journal entries and replaces them with demo data.

### 6. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

> **Note:** The SQLite database (`journal.db`) is created automatically on first run.

## Project Structure

```
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── .env                   # API keys (not committed)
├── journal.db             # SQLite database (auto-created)
│
├── services/
│   ├── leafy.py           # AI companion (OpenAI integration)
│   └── database.py        # SQLite operations
│
├── ui/
│   ├── components.py      # Reusable UI components
│   └── styles.css         # Custom CSS
│
├── utils/
│   ├── config.py          # Constants and settings
│   ├── helpers.py         # Helper functions
│   └── logger.py          # Logging setup
│
├── scripts/
│   └── populate_demo.py   # Demo data generator
│
└── tests/
    ├── test_config.py
    ├── test_database.py
    └── test_leafy.py
```

## Running Tests

```bash
pytest tests/ -v
```

## Tech Stack

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4o-mini
- **Database**: SQLite
- **Language**: Python 3.13