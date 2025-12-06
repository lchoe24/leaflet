import os
import random
from typing import List, Dict, Optional
from dotenv import load_dotenv
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from utils.logger import logger

load_dotenv()


def get_first_user_message(entry: Dict, max_length: int = 200) -> str:
    for msg in entry.get('messages', []):
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            return content[:max_length] if len(content) > max_length else content
    return ""


WELCOME_PROMPT = """Analyze these recent journal entries and create a thoughtful reflection prompt.

ENTRIES (most recent first):
{entries_text}

MOOD DISTRIBUTION (last {entry_count} entries): {mood_summary}

Generate a personalized prompt that does ONE of these (pick the most relevant):

1. Follow-up: Reference something specific from their most recent entry
   Example: "You mentioned trying that pasta recipe - did it turn out how you hoped?"

2. Pattern observation: If you notice a recurring theme, gently acknowledge it
   Example: "I've noticed walks seem to lift your spirits. Have you been outside today?"

3. Contrast question: If recent moods have shifted, ask about the transition
   Example: "Yesterday felt heavy, but today might be different. What's one small thing you're looking forward to?"

4. Deeper reflection: If they've mentioned something meaningful multiple times, explore it
   Example: "You've written about missing LA a few times. What do you miss most right now?"

RULES:
- Be SPECIFIC - use actual details from their entries
- Keep it to 1-2 sentences
- Sound like a caring friend, not a therapist
- NO generic phrases like "How are you feeling today?"
- Match the warmth level to their recent moods

Return ONLY the prompt."""

RESPONSE_PROMPT = """The user just shared this in their journal:

{convo_text}

Their current mood is: {mood}

Respond with:
1. A brief empathetic acknowledgment (1 sentence)
2. A thoughtful follow-up question to help them reflect deeper (1 sentence)

Be warm, non-judgmental, and genuine. Keep total response under 40 words."""

CLOSING_PROMPT = """The user had this journaling conversation:

{convo_text}

Their mood was: {mood}

Write a warm, closing message that:
1. Acknowledges something meaningful from their reflection
2. Offers gentle encouragement
3. Thanks them for sharing

Keep it to 2-3 sentences. Be genuine and supportive. End with "Take care 💫" """

MOOD_SUMMARY_PROMPT = """Analyze these journal entries from the past month:

{entries_text}

Write a brief, warm summary (3-4 sentences) that:
1. Notes what tends to bring them UP (specific activities, people, situations)
2. Notes what tends to bring them DOWN (specific triggers)
3. Highlights any positive growth or patterns you notice
4. Offers one gentle, actionable insight

Be specific - reference actual things from their entries. Sound like a caring friend, not a therapist.

Return ONLY the summary."""

EXPLORATION_PROMPT = """Generate ONE thought-provoking journaling prompt that helps someone explore something new.

Pick randomly from these categories:
- An interesting philosophical question
- A "what if" scenario to imagine
- A creative prompt (describe a place, person, memory)
- A gratitude or appreciation prompt
- A future-focused question

Make it specific and engaging, not generic. Keep it to 1-2 sentences.

Return ONLY the prompt."""

CHALLENGES_PROMPT = """Based on these recent journal entries, generate exactly 3 small, achievable challenges for today.

Recent entries:
{entries_context}

Requirements:
- Each challenge should be tiny and doable in a few minutes
- Make them personal based on the entries (interests, struggles, goals mentioned)
- Focus on well-being, creativity, connection, or self-care
- Keep each challenge to ONE short sentence (under 15 words)

Return ONLY 3 challenges, one per line, no numbers or bullets."""


class Leafy:
    FALLBACK_PROMPTS = [
        "If you could have dinner with anyone from history, who would it be and what would you ask them?",
        "Describe your perfect day, from morning to night. What makes it perfect?",
        "What's a small moment from this week that you want to remember?",
        "If you woke up tomorrow with a new skill fully mastered, what would you want it to be?",
        "Write about a place that makes you feel calm. What do you see, hear, and feel there?",
    ]

    FALLBACK_CHALLENGES = [
        "Take a 5-minute walk and notice something beautiful",
        "Write down 3 things you're grateful for today",
        "Send a kind message to someone you appreciate"
    ]

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
            return "What’s been lingering in your mind, even if it feels small or insignificant?"

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

        return result or "What's been on your mind lately that you haven't had a chance to explore?"

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
        if is_closing:
            return "Thank you for sharing today. Every moment of reflection brings you closer to understanding yourself. Take care 💫"
        return "Thank you for sharing that. What's the main thing you want to take away from this reflection?"

    def generate_mood_summary(self, entries: List[Dict]) -> str:
        if not entries:
            return "Keep journaling to unlock deeper insights about your patterns!"

        summaries = []
        for e in entries[:30]:
            first_msg = get_first_user_message(e, max_length=100)
            summaries.append(f"- {e.get('date')} | {e.get('mood')} | {first_msg}")

        prompt = MOOD_SUMMARY_PROMPT.format(entries_text="\n".join(summaries))

        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a warm journaling companion."},
            {"role": "user", "content": prompt}
        ], max_tokens=200, temperature=0.7)

        return result or "Keep journaling to unlock deeper insights about your patterns!"

    def generate_exploration_prompt(self) -> str:
        result = self._call_openai([
            {"role": "system", "content": "You are Leafy, a creative journaling companion."},
            {"role": "user", "content": EXPLORATION_PROMPT}
        ], max_tokens=80, temperature=1.0)

        return result or random.choice(self.FALLBACK_PROMPTS)

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
        return self.FALLBACK_CHALLENGES.copy()


leafy = Leafy()
