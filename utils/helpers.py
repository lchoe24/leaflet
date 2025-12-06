from datetime import date, timedelta
from typing import Any, List, Tuple, Dict
from services.database import get_all_entries
from utils.config import DAYS_OF_WEEK, GARDEN_PLANTS, MOOD_ORDER


def get_weekly_garden() -> Tuple[List[str], List[str], int]:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    all_entries = get_all_entries()
    journaled_dates = set()
    for e in all_entries:
        try:
            entry_date = date.fromisoformat(e['date'])
            if week_start <= entry_date <= week_start + timedelta(days=6):
                journaled_dates.add(entry_date)
        except (ValueError, KeyError):
            continue
    
    week_display = []
    days_journaled = 0
    for i, day_name in enumerate(DAYS_OF_WEEK):
        day_date = week_start + timedelta(days=i)
        if day_date in journaled_dates:
            week_display.append(GARDEN_PLANTS[i])
            days_journaled += 1
        elif day_date <= today:
            week_display.append("○" if day_date == today else "·")
        else:
            week_display.append("○")
    
    return DAYS_OF_WEEK, week_display, days_journaled


def calculate_mood_stats(entries: List[Dict]) -> Tuple[Dict[str, int], int, str]:
    mood_counts = {mood: 0 for mood in MOOD_ORDER}
    for e in entries:
        mood = e.get('mood', 'Unknown')
        if mood in mood_counts:
            mood_counts[mood] += 1
    
    total = len(entries)
    top_mood = max(mood_counts, key=mood_counts.get) if total > 0 else "Neutral"
    
    return mood_counts, total, top_mood
