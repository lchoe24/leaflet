import pytest
from utils.config import MOODS, get_mood_display, get_mood_value


def test_moods_exist():
    assert len(MOODS) == 5


def test_get_mood_display():
    assert "🥰" in get_mood_display("Happy")


def test_get_mood_value():
    assert get_mood_value("🥰 Happy") == "Happy"
