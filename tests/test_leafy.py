import pytest
from services.leafy import get_first_user_message, Leafy


def test_get_first_user_message():
    entry = {'messages': [{'role': 'user', 'content': 'Hello'}]}
    assert get_first_user_message(entry) == 'Hello'


def test_get_first_user_message_empty():
    assert get_first_user_message({}) == ""


def test_leafy_has_fallbacks():
    assert len(Leafy.FALLBACK_PROMPTS) > 0
    assert len(Leafy.FALLBACK_CHALLENGES) == 3

