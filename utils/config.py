MOODS = {
    "Happy": {"emoji": "🥰", "color": "#4ade80"},
    "Content": {"emoji": "🙂", "color": "#86efac"},
    "Neutral": {"emoji": "😐", "color": "#fbbf24"},
    "Sad": {"emoji": "😔", "color": "#f97316"},
    "Overwhelmed": {"emoji": "😞", "color": "#ef4444"}
}

MOOD_OPTIONS = [f"{v['emoji']} {k}" for k, v in MOODS.items()]
MOOD_ORDER = list(MOODS.keys())


def get_mood_display(mood_text: str) -> str:
    for mood, data in MOODS.items():
        if mood in mood_text:
            return f"{data['emoji']} {mood}"
    return mood_text


def get_mood_value(display_mood: str) -> str:
    for mood in MOODS.keys():
        if mood in display_mood:
            return mood
    return display_mood


def get_mood_color(mood: str) -> str:
    return MOODS.get(mood, {}).get("color", "#888")


def get_mood_emoji(mood: str) -> str:
    return MOODS.get(mood, {}).get("emoji", "")


JOURNAL_MODES = {
    "reflective": {"icon": "🪞", "title": "Be Reflective", "subtitle": "AI analyzes your patterns"},
    "explore": {"icon": "✨", "title": "Explore New", "subtitle": "Spark curiosity & ideas"},
    "freewrite": {"icon": "📝", "title": "Free Write", "subtitle": "Open space for thoughts"}
}

DEFAULT_SESSION_STATE = {
    "journal_step": 0,
    "journal_mode": None,
    "mood": None,
    "entry_1": "",
    "ai_response_1": "",
    "entry_2": "",
    "ai_closing": "",
    "welcome_prompt": None
}

GARDEN_PLANTS = ["🌱", "🌿", "🌷", "🌸", "🌺", "🌻", "🌼"]
DAYS_OF_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
