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

FALLBACK_WELCOME = "What's been on your mind lately that you haven't had a chance to explore?"
FALLBACK_WELCOME_NEW_USER = "What's been lingering in your mind, even if it feels small or insignificant?"
FALLBACK_RESPONSE = "Thank you for sharing that. What's the main thing you want to take away from this reflection?"
FALLBACK_CLOSING = "Thank you for sharing today. Every moment of reflection brings you closer to understanding yourself. Take care 💫"
FALLBACK_MOOD_SUMMARY = "Keep journaling to unlock deeper insights about your patterns!"

