# Leaflet - Design Documentation

## Overview

**Leaflet** is an AI-powered journaling companion that helps users reflect, explore their thoughts, and build consistent journaling habits through conversational interactions with an AI companion named Leafy.

---

## User Flow

```
1. Open App
      │
      ▼
2. See Weekly Garden (streak tracker)
      │
      ▼
3. Choose Journal Mode
   ├── Be Reflective (AI analyzes past patterns)
   ├── Explore New (random creative prompts)
   └── Free Write (open-ended)
      │
      ▼
4. Select Mood → Write Entry
      │
      ▼
5. Leafy Responds → User Continues
      │
      ▼
6. Leafy Closes → Entry Saved
      │
      ▼
7. Unlock Challenges & Insights
```

---

## AI Features

| Feature | How It Works |
|---------|--------------|
| **Reflective Prompts** | Analyzes past entries to generate personalized, specific questions |
| **Exploration Prompts** | Generates creative, thought-provoking topics |
| **Conversation Responses** | Provides empathetic follow-ups and closing messages |
| **Mood Summary** | Identifies patterns and trends over 30 days |
| **Daily Challenges** | Creates personalized micro-tasks based on past entries — encourages consistent journaling by giving users something to reflect on |

### Prompt Engineering

All prompts follow a consistent structure using prompt engineering best practices:

| Technique | Implementation |
|-----------|----------------|
| **Structured Format** | Every prompt uses CONTEXT → TASK → EXAMPLES → RULES → OUTPUT |
| **Few-Shot Examples** | Good and bad examples guide the AI toward desired responses |
| **System Prompt** | Defines Leafy's personality, tone, and guardrails |
| **Guardrails** | Prevents unwanted behavior (no diagnoses, no clichés, no "As an AI...") |
| **Output Constraints** | Explicit word limits and format requirements |

**Example prompt structure:**
```
CONTEXT: [What data is provided]
TASK: [What to do]
EXAMPLES: [Good vs bad outputs]
RULES: [Constraints and tone]
OUTPUT: [Expected format]
```

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                          │
│                           (Streamlit)                           │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │                        app.py                           │   │
│   │   ┌────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐       │   │
│   │   │Journal │ │Challenges│ │Insights │ │ History │       │   │
│   │   └────────┘ └──────────┘ └─────────┘ └─────────┘       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│        ui/components.py                ui/styles.css            │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                          SERVICES LAYER                         │
│                                                                 │
│     ┌─────────────────────┐        ┌─────────────────────┐      │
│     │      leafy.py       │        │     database.py     │      │
│     │    (AI Service)     │        │     (DB Layer)      │      │
│     └──────────┬──────────┘        └──────────┬──────────┘      │
└────────────────┼─────────────────────────────┼──────────────────┘
                 │                             │
                 ▼                             ▼
         ┌───────────────┐             ┌───────────────┐
         │  OpenAI API   │             │  journal.db   │
         │ (GPT-4o-mini) │             │   (SQLite)    │
         └───────────────┘             └───────────────┘
```

### Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Conversational UX** | Chat-like flow makes journaling feel like talking to a friend, reducing friction and encouraging deeper reflection |
| **Three Journaling Modes** | Users have different needs and often don't know what to write — AI prompts help start the conversation, then Leafy responds to guide deeper reflection through structured reflection, creative exploration, or free expression |
| **AI Fallbacks** | All AI features gracefully degrade to backup prompts if API calls fail — app never breaks |
| **Local-first Storage** | SQLite for simplicity and privacy; no cloud dependency for core functionality |
| **Normalized Database** | Separate `entries` and `messages` tables allow flexible conversation turns |
| **Prompt Separation** | Prompts stored as constants, separate from logic, for easy tuning |

---

## Technical Stack

| Component | Technology | Why |
|-----------|------------|-----|
| Language | Python 3.13 | Rapid prototyping, Streamlit requires Python, clean syntax for maintainable code |
| Frontend | Streamlit | Fast to build, reactive UI, perfect for prototypes |
| Styling | Custom CSS | Enables a branded aesthetic beyond Streamlit defaults |
| Database | SQLite | Local-first, secure, zero setup, ideal for storing private journal entries safely |
| AI Model | OpenAI GPT-4o-mini | Lightweight, fast, cost-efficient, strong conversational and reflective dialogue generation |

### Libraries

| Library | Purpose |
|---------|---------|
| `streamlit` | Frontend UI framework with reactive state management |
| `openai` | LLM interaction for journaling prompts and empathetic AI responses |
| `python-dotenv` | Securely manages and loads API keys without hardcoding |
| `pytest` | Testing framework |

### Database Schema

**entries** (metadata)
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| date | TEXT | Entry date (YYYY-MM-DD) |
| mood | TEXT | User's selected mood |
| created_at | TEXT | Timestamp |

**messages** (conversation turns)
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| entry_id | INTEGER | Foreign key → entries |
| role | TEXT | "user" or "ai" |
| content | TEXT | Message text |
| turn_order | INTEGER | Conversation sequence |

---

## Privacy & Security

| Principle | Implementation |
|-----------|----------------|
| **Local Storage** | All journal entries stored locally in SQLite — nothing saved to external servers |
| **No Accounts** | No sign-up needed — just open and write |
| **Non-judgmental AI** | Leafy is prompted to be warm, supportive, and never critical |
| **OpenAI Privacy** | Journal entries sent to OpenAI for personalized insights — no personal data collected |
| **Transparency** | Open source — see exactly how data is handled |

### API Security

- **Environment Variables**: OpenAI API key stored in `.env` file, never hardcoded
- **Gitignore Protected**: `.env` excluded from version control via `.gitignore`
- **Runtime Loading**: Key loaded via `python-dotenv` in `leafy.py` at startup

---

## Product Roadmap

### UX Enhancements

- **Custom Themes**: Add light mode, high-contrast mode, and soft color palettes to personalize the journaling space
- **Search & Filter**: Enable keyword search, mood filters, and quick navigation of past entries
- **Customizable Insights**: Let users select time ranges for AI summaries (7 days, 30 days, 90 days, all time) instead of fixed 30-day view
- **Voice Journaling**: Add speech-to-text capture for users who prefer reflective audio notes
- **Smart Reminders**: Gentle notifications to maintain journaling streaks, based on the user's preferred time of day

### Feature Additions

- **Export & Import Entries**: Support for exporting journal entries as PDF or JSON, and importing past reflections into the app
- **Challenge Tracking**: Store challenges in the database so users can mark them complete and track progress over time
- **Therapist / Support Mode**: An optional feature that allows exporting structured emotional summaries or sharing certain entries with mental health professionals

### Platform & Infrastructure

- **Multi-User Accounts & Cloud Sync**: Support optional authentication and secure cloud backup so users can access their journals across devices
- **Native Mobile App**: Develop iOS and Android versions to support on-the-go journaling
- **Ecosystem Integrations**: Connect with the user's calendar, health apps, or meditation platforms for deeper context and smarter insights

### AI Capabilities

| Feature | Current State | Future Enhancement |
|---------|---------------|-------------------|
| **Extended Conversations** | Fixed conversation turns with Leafy | Unlimited back-and-forth; user decides when to end the conversation |
| **Smarter Pattern Recognition** | Basic mood frequency tracking | Thorough detection of recurring themes (work stress, relationships), emotional triggers, and time-based patterns |
| **Sentiment Analysis** | User manually selects mood from 5 options | AI auto-detects mood from journal text, suggests corrections |
| **Goal Tracking** | No goal features | User sets personal goals; Leafy tracks progress and offers encouragement |
