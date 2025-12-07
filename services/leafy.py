import os
import random
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from utils.logger import logger
from utils.prompts import (
    WELCOME_PROMPT, RESPONSE_PROMPT, CLOSING_PROMPT,
    MOOD_SUMMARY_PROMPT, EXPLORATION_PROMPT, CHALLENGES_PROMPT,
    FALLBACK_PROMPTS, FALLBACK_CHALLENGES,
    FALLBACK_WELCOME, FALLBACK_WELCOME_NEW_USER,
    FALLBACK_RESPONSE, FALLBACK_CLOSING, FALLBACK_MOOD_SUMMARY
)

load_dotenv()


def get_first_user_message(entry: Dict, max_length: int = 200) -> str:
    for msg in entry.get('messages', []):
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            return content[:max_length] if len(content) > max_length else content
    return ""


class Leafy:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = "gpt-4o-mini"

    def _call_openai(self, messages: List[Dict], max_tokens: int = 150, temperature: float = 0.7) -> Optional[str]:
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            logger.warning("OpenAI rate limit reached")
            return None
        except APIConnectionError:
            logger.warning("OpenAI connection failed")
            return None
        except APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return None

    def generate_personalized_welcome(self, entries: List[Dict]) -> str:
        if not entries:
            return FALLBACK_WELCOME_NEW_USER

        recent = entries[:10]
        
        details = []
        for e in recent:
            msgs = e.get('messages', [])
            user_msgs = [m['content'] for m in msgs if m.get('role') == 'user']
            text = " ".join(user_msgs)[:300]
            details.append(f"- {e.get('date')} | {e.get('mood')} | {text}")

        mood_counts = {}
        for e in recent:
            mood = e.get('mood', 'Unknown')
            mood_counts[mood] = mood_counts.get(mood, 0) + 1

        prompt = WELCOME_PROMPT.format(
            entries_text="\n".join(details),
            entry_count=len(recent),
            mood_summary=", ".join([f"{k}: {v}" for k, v in mood_counts.items()])
        )

        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a warm journaling companion."},
            {"role": "user", "content": prompt}
        ], max_tokens=150, temperature=0.85)

        return result or FALLBACK_WELCOME

    def generate_response(self, conversation: List[Dict], mood: str, is_closing: bool = False) -> str:
        convo_text = "\n".join([f"{msg['role']}: {msg['text']}" for msg in conversation])

        if is_closing:
            prompt = CLOSING_PROMPT.format(convo_text=convo_text, mood=mood)
        else:
            prompt = RESPONSE_PROMPT.format(convo_text=convo_text, mood=mood)

        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a compassionate journaling companion."},
            {"role": "user", "content": prompt}
        ], max_tokens=100, temperature=0.7)

        if result:
            return result
        return FALLBACK_CLOSING if is_closing else FALLBACK_RESPONSE

    def generate_mood_summary(self, entries: List[Dict]) -> str:
        if not entries:
            return FALLBACK_MOOD_SUMMARY

        summaries = []
        for e in entries[:30]:
            first_msg = get_first_user_message(e, max_length=100)
            summaries.append(f"- {e.get('date')} | {e.get('mood')} | {first_msg}")

        prompt = MOOD_SUMMARY_PROMPT.format(entries_text="\n".join(summaries))

        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a warm journaling companion."},
            {"role": "user", "content": prompt}
        ], max_tokens=200, temperature=0.7)

        return result or FALLBACK_MOOD_SUMMARY

    def generate_exploration_prompt(self) -> str:
        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a creative journaling companion."},
            {"role": "user", "content": EXPLORATION_PROMPT}
        ], max_tokens=80, temperature=1.0)

        return result or random.choice(FALLBACK_PROMPTS)

    def generate_challenges(self, entries: List[Dict]) -> List[str]:
        summaries = []
        for e in entries[-10:]:
            first_msg = get_first_user_message(e, max_length=150)
            if first_msg:
                summaries.append(f"- {e.get('mood', 'Unknown')}: {first_msg}...")

        context = "\n".join(summaries) if summaries else "No recent entries"
        prompt = CHALLENGES_PROMPT.format(entries_context=context)

        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a supportive wellness coach."},
            {"role": "user", "content": prompt}
        ], max_tokens=150, temperature=0.8)

        if result:
            challenges = [c.strip() for c in result.split('\n') if c.strip()]
            return challenges[:3]
        return FALLBACK_CHALLENGES.copy()


leafy = Leafy()
