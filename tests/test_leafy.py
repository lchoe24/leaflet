import pytest
from services.leafy import get_first_user_message
from utils.prompts import FALLBACK_PROMPTS, FALLBACK_CHALLENGES


def test_get_first_user_message():
    entry = {'messages': [{'role': 'user', 'content': 'Hello'}]}
    assert get_first_user_message(entry) == 'Hello'


def test_get_first_user_message_empty():
    assert get_first_user_message({}) == ""


def test_leafy_has_fallbacks():
    assert len(FALLBACK_PROMPTS) > 0
    assert len(FALLBACK_CHALLENGES) == 3

