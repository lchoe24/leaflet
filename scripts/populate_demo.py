import sqlite3
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DB_FILE = PROJECT_ROOT / "journal.db"

entries = [
    ("2025-11-01", "Neutral",
     "Woke up late and missed my usual morning routine. The city felt gray and rainy outside, which made me feel a bit gloomy.",
     "Rainy mornings can affect our mood. How did you try to lift your spirits today?",
     "I brewed some herbal tea and listened to a favorite playlist while getting ready.",
     "Small rituals like music and tea help brighten gray mornings. How did it impact your day?",
     "It helped a little, but I still felt slow at work. Hoping tomorrow is sunnier.",
     "Not every day will feel perfect, but noticing what helps even slightly is progress. Keep cherishing those small wins!"),

    ("2025-11-02", "Content",
     "Met up with a friend for brunch. Talked about our favorite spots in the city, felt more connected.",
     "That's great! How did spending time with a friend influence your mood?",
     "I felt lighter and more relaxed. It's comforting to have someone who understands me here.",
     "Building connections really helps when adjusting to a new city. What did you enjoy most about brunch?",
     "The little jokes we shared and the latte I didn't drink! Coffee still makes me jittery.",
     "Recognizing what nourishes you and what doesn't is important. Keep valuing these positive interactions!"),

    ("2025-11-03", "Happy",
     "Woke up early, got a full 9 hours of sleep. Sat by my window watching the sunrise and wrote a short poem.",
     "Sleep can make such a difference! How did that restful morning feel?",
     "Refreshing. I felt energetic and creative, ready to tackle errands and work.",
     "That's wonderful! Did writing the poem help you process your feelings?",
     "Yes, it gave me a sense of calm and accomplishment.",
     "Starting the day with reflection and rest sets a positive tone. Keep prioritizing your sleep and creative moments!"),

    ("2025-11-04", "Sad",
     "It rained almost all day. Felt stuck inside and a bit lonely since most friends were busy.",
     "Rainy days can feel isolating. How did you cope with the gloom?",
     "I read a novel and lit a few candles to make the apartment cozy.",
     "Creating a comforting space is a great way to care for yourself. Did it help your mood?",
     "A little, but I still missed chatting with someone in person.",
     "Even small acts of self-care are meaningful. Tomorrow you might find a chance to connect!"),

    ("2025-11-05", "Content",
     "Had a productive day running errands and discovering a new bookstore in the East Village.",
     "Exploring the city can be rewarding. What did you enjoy most at the bookstore?",
     "I found a poetry section and spent hours flipping through books, feeling inspired.",
     "Finding moments of joy in small discoveries is wonderful. Did this spark any ideas for you?",
     "Yes! I want to start a little reading journal to track thoughts and favorite passages.",
     "Noticing inspirations and taking notes helps you reflect and grow. Keep nurturing your curiosity!"),

    ("2025-11-06", "Happy",
     "Woke up feeling refreshed, made a light breakfast, and sketched some ideas for a personal project.",
     "Sketching ideas is creative! How did it make you feel?",
     "Motivated and calm. It reminded me why I love planning small projects.",
     "Engaging in creativity early sets a positive tone. Did you follow through with the project later?",
     "Yes, I organized a few tasks and felt accomplished by midday.",
     "Small creative steps lead to bigger achievements. Celebrate these wins!"),

    ("2025-11-07", "Neutral",
     "Overslept slightly, skipped my morning meditation. Felt sluggish and unmotivated.",
     "Missing routines can affect energy. How did you try to recover?",
     "I went for a short walk and drank herbal tea, which helped a bit.",
     "Good adjustments! Did it help your productivity later?",
     "Slightly, but I still felt behind. Planning tomorrow better.",
     "Reflecting and adjusting routines gradually helps maintain consistency. Keep observing your patterns!"),

    ("2025-11-08", "Content",
     "Met a new neighbor and had a casual chat. Felt nice to start forming connections.",
     "That's great! How did it feel socially?",
     "Comfortable and encouraged. I realized I'm slowly getting used to the city.",
     "Social connections make adaptation easier. Did the chat spark any plans?",
     "We decided to grab coffee next weekend — decaf, of course!",
     "Even small social bonds enrich daily life. Keep cultivating these connections!"),

    ("2025-11-09", "Sad",
     "Coffee shop visit made me jittery and anxious despite trying decaf.",
     "Caffeine can affect mood. How did you manage the anxiety?",
     "I stepped outside and walked around the block to calm down.",
     "Physical activity is a great coping tool. Did it help you feel grounded?",
     "Yes, the walk helped, though I still felt a little on edge.",
     "Noticing your triggers and practicing calming strategies builds resilience. Keep experimenting!"),

    ("2025-11-10", "Happy",
     "Had a long, restful sleep and woke up energized. Finished a book I've been reading for weeks.",
     "Sleep really supports mood. How did finishing the book feel?",
     "Accomplished and proud. I even took notes for a future journal entry.",
     "Reflection on achievements is valuable. Did writing notes help process the book?",
     "Yes, it sparked new ideas for my own creative writing.",
     "Capturing insights reinforces learning and creativity. Keep integrating reflection into your routine!"),

    ("2025-11-11", "Content",
     "Visited a small art gallery downtown. Loved the photography exhibits, especially ones featuring city streets.",
     "Art can inspire new perspectives. What caught your attention the most?",
     "The angles of buildings and the way light was captured fascinated me.",
     "Noticing details helps deepen appreciation. Did it influence your own creative work?",
     "Yes, I sketched a few street scenes when I got home.",
     "Translating inspiration into personal projects is a wonderful habit. Keep observing and creating!"),

    ("2025-11-12", "Neutral",
     "Spent the day running errands. Weather was cloudy, made me feel a bit sluggish.",
     "Cloudy days can impact energy. How did you cope?",
     "Listened to upbeat music while walking between stores. Helped slightly.",
     "Small mood-lifting actions are effective. Did it improve your focus for tasks?",
     "Somewhat, but I felt tired by evening.",
     "Recognizing when your environment affects you allows planning better self-care tomorrow."),

    ("2025-11-13", "Happy",
     "Had a video call with my sister in LA. Felt connected and nostalgic.",
     "Long-distance calls can be comforting. What did you enjoy most?",
     "Talking about shared memories made me laugh and smile.",
     "Maintaining bonds nurtures emotional health. Did it inspire you in any way?",
     "Yes, I wrote a short reflection in my journal about family connections.",
     "Capturing meaningful interactions strengthens awareness and gratitude. Keep journaling these moments!"),

    ("2025-11-14", "Content",
     "Discovered a new park and went for an afternoon walk. Sun peeked through clouds, felt uplifting.",
     "Exploring green spaces is refreshing! How did it impact your mood?",
     "I felt calm and more focused, ready to tackle evening work.",
     "Nature often helps reset energy. Did you notice anything new?",
     "The sound of distant children playing and leaves rustling made me smile.",
     "Observing small joys in your environment strengthens mindfulness. Keep noticing these moments!"),

    ("2025-11-15", "Overwhelmed",
     "Work emails piled up and I had three deadlines overlapping. Felt paralyzed and anxious.",
     "That sounds really stressful. How did you try to manage all of it?",
     "I made a priority list but still felt like I was drowning. Took breaks to breathe.",
     "Breaking things down helps even when it feels impossible. Did the breaks help at all?",
     "A little. I got through the most urgent task but still felt drained by evening.",
     "You pushed through despite the overwhelm - that takes strength. Be gentle with yourself tonight."),

    ("2025-11-16", "Happy",
     "Woke up early, brewed tea, and wrote a few creative journal entries before work.",
     "Starting the day creatively is great! How did it affect your mood?",
     "Energized and motivated. Felt like I had a head start on the day.",
     "Creating space for reflection sets a positive tone. Did you continue your tasks smoothly?",
     "Yes, focusing felt easier with the clear mind.",
     "Morning routines that balance reflection and action support overall well-being. Keep practicing!"),

    ("2025-11-17", "Sad",
     "Rainy day, stayed inside. Felt low and unmotivated. Missed friends today.",
     "Rainy days can weigh on mood. How did you cope?",
     "Read a short story and tried to tidy the apartment for a sense of control.",
     "Small actions help even on gloomy days. Did it improve your outlook?",
     "Slightly, but I still felt a little isolated.",
     "Acknowledging feelings and taking small steps helps manage low moods. Keep being gentle with yourself!"),

    ("2025-11-18", "Content",
     "Had a cozy evening cooking a new pasta recipe. Music on, candles lit.",
     "Cooking can be very soothing. How did it feel?",
     "Relaxing and satisfying. Enjoyed trying a new combination of flavors.",
     "Experiences like this bring joy and mindfulness. Did it inspire any future meals?",
     "Yes, I plan to try another recipe this weekend.",
     "Small creative acts enhance daily happiness. Keep experimenting in the kitchen!"),

    ("2025-11-19", "Happy",
     "Went for a sunrise walk. The city was quiet and peaceful, felt reflective.",
     "Morning walks are great for reflection. What stood out to you?",
     "Noticing the way light hit the buildings and the quiet streets made me feel calm.",
     "Observing surroundings can ground you. Did it influence your journaling?",
     "Yes, I wrote a short poem about the morning in my journal.",
     "Translating observations into writing nurtures mindfulness. Keep capturing these moments!"),

    ("2025-11-20", "Neutral",
     "Had a busy day at work. Felt productive but tired by evening.",
     "Busy days can be draining. How did you unwind afterward?",
     "I made chamomile tea and watched a short documentary.",
     "Small evening rituals help balance stress. Did it help you relax?",
     "Yes, it helped me feel calmer before bed.",
     "Recognizing when to pause and rest maintains long-term well-being. Keep honoring your downtime!"),

    ("2025-11-21", "Content",
     "Brunch with friends at a small rooftop café. Sun was shining, felt cheerful.",
     "Rooftop settings can lift spirits. How did the social time feel?",
     "Comfortable and fun. Enjoyed the laughter and light conversations.",
     "Social interactions strengthen connection. Did it boost your energy?",
     "Yes, I felt lighter and more motivated for the rest of the day.",
     "Cherishing social moments fosters well-being. Keep spending time with friends!"),

    ("2025-11-22", "Neutral",
     "Skipped breakfast again. Morning was rushed and a bit chaotic.",
     "Mornings can set the tone for the day. How did you adjust?",
     "I took a short walk to calm down and organized my to-do list.",
     "Good coping strategies! Did it help you regain focus?",
     "Somewhat, but I still felt slightly behind on work.",
     "Adjusting routines gradually helps maintain balance. Keep experimenting with small improvements!"),

    ("2025-11-23", "Happy",
     "Slept in a bit and woke up feeling refreshed. Journaled about goals and aspirations.",
     "Restful sleep is important. How did journaling make you feel?",
     "Motivated and centered. It clarified what I wanted to focus on this week.",
     "Reflection helps prioritize. Did it influence your actions later?",
     "Yes, I tackled tasks more efficiently and with clarity.",
     "Using journaling to align intentions with actions strengthens productivity and emotional clarity!"),

    ("2025-11-24", "Sad",
     "Rainy day again. Felt a little isolated since no friends were available.",
     "Rain can impact mood. How did you cope?",
     "I did a short yoga session and sipped herbal tea.",
     "Small calming actions help. Did it improve your outlook?",
     "Slightly, but I felt a bit lonely in the afternoon.",
     "Acknowledging loneliness and caring for yourself is a healthy approach. Keep these self-soothing habits!"),

    ("2025-11-25", "Content",
     "Went for a walk in the park after rain. Air smelled fresh and crisp.",
     "Walking outdoors can refresh the mind. How did it feel?",
     "Calm and relaxed. Loved seeing a few children play and leaves glistening after rain.",
     "Noticing simple joys boosts well-being. Did it spark any creative thoughts?",
     "Yes, I drafted a few sketches and notes for my journal.",
     "Capturing inspirations in real-time encourages mindfulness and creativity!"),

    ("2025-11-26", "Happy",
     "Woke up well-rested, meditated, and wrote a short story in my journal.",
     "Combining meditation and creativity sounds nurturing. How did it feel?",
     "Calm and accomplished. Felt like a balanced start to the day.",
     "Did this influence your interactions or work?",
     "Yes, I felt focused and patient during meetings.",
     "Building habits that combine reflection and creativity positively impacts your daily life."),

    ("2025-11-27", "Overwhelmed",
     "Had back-to-back meetings all day. By 5pm my brain felt completely fried.",
     "That sounds exhausting. How did you try to decompress?",
     "I canceled evening plans and just lay on the couch staring at the ceiling for a while.",
     "Small self-care moments help. Did it ease fatigue?",
     "Somewhat, but I still felt tired by evening.",
     "Recognizing energy dips allows for proactive self-care. Keep noticing these signals!"),

    ("2025-11-28", "Content",
     "Evening coffee with a friend (decaf). Enjoyed catching up and talking about favorite books.",
     "Catching up is refreshing. How did it affect your mood?",
     "Lighthearted and cheerful. Felt grateful for supportive friendships.",
     "Good company nurtures well-being. Did it inspire any plans?",
     "Yes, we planned a weekend visit to a local museum.",
     "Investing in relationships creates lasting positivity. Keep building your social network!"),

    ("2025-11-29", "Sad",
     "Felt anxious after accidentally drinking regular coffee at lunch.",
     "That can be uncomfortable. How did you recover?",
     "I went for a short walk and practiced deep breathing exercises.",
     "Managing physical reactions with calming strategies is effective. Did it help?",
     "Yes, slowly felt my heart rate normalize, though I was still jittery.",
     "Being mindful of triggers and having coping strategies is key. Keep practicing!"),

    ("2025-11-30", "Happy",
     "Had a great night of sleep. Wrote a poem inspired by city lights before bed.",
     "Restful nights support creativity. How did the writing feel?",
     "Calming and fulfilling. Felt like I captured the city's magic.",
     "Creative expression can be therapeutic. Did it influence your next day?",
     "Yes, I woke up inspired and productive.",
     "Capturing inspiration before sleep nurtures both creativity and mindfulness."),

    ("2025-12-01", "Content",
     "Met a friend for a light lunch and a walk in Central Park. Sunny day lifted spirits.",
     "Nice! How did the combination of social time and nature affect your mood?",
     "Felt calm, happy, and more grounded.",
     "Good balance! Did it motivate any creative work afterward?",
     "Yes, I wrote a short reflective journal entry.",
     "Combining nature, social interaction, and reflection supports emotional health."),

    ("2025-12-02", "Neutral",
     "Skipped breakfast and rushed to work. Felt slightly stressed all morning.",
     "Rushing can affect energy. How did you recover?",
     "I paused for a short walk and did breathing exercises.",
     "Mindful breaks help regulate stress. Did it improve focus?",
     "Somewhat, though fatigue lingered.",
     "Even small mindful pauses help maintain stability. Keep incorporating them!"),

    ("2025-12-03", "Happy",
     "Woke up at 7:00 AM after a full 8 hours of sleep. Felt rested and calm. Made a warm cup of chamomile tea and journaled about three things I'm grateful for: my supportive friends, a cozy apartment in NYC, and the peaceful morning light streaming through my window.",
     "Gratitude journaling can really uplift mood and focus your mind. How did writing about these things make you feel?",
     "I felt centered and appreciative. Recognizing the small joys in my life made me feel grounded and optimistic.",
     "That sense of groundedness is powerful! Did journaling influence how your day unfolded?",
     "Absolutely. I approached work calmly and efficiently, prioritized tasks without feeling rushed.",
     "Starting the day with gratitude and reflection can improve focus, emotional balance, and productivity. Keep nurturing this morning routine!"),

    ("2025-12-04", "Sad",
     "The afternoon was rainy and gray, which made the apartment feel dim and a bit gloomy. I felt lonely because none of my friends were available to hang out this week.",
     "Rainy days can intensify feelings of isolation. How did you cope with these emotions while stuck indoors?",
     "I focused on creating a cozy environment: I lit a few candles, played soft instrumental music, and read a few chapters of my book.",
     "Creating comforting routines like that is a great way to nurture yourself. Did it lift your spirits at all?",
     "Only a little, but it helped me acknowledge my feelings instead of ignoring them. I also journaled briefly about what I was feeling.",
     "Gentle self-care during low moods is important for emotional resilience. Recognizing your feelings and providing yourself small comforts is a healthy strategy."),

    ("2025-12-05", "Content",
     "The sun peeked through clouds in the late morning, lifting my mood. I decided to go for a short walk around the neighborhood.",
     "Discovering street art and exploring your surroundings can be uplifting. How did this experience impact your mood and creativity?",
     "I felt lighthearted and energized. The unexpected visual stimulation sparked ideas for my own creative projects.",
     "Noticing beauty and inspiration in your environment can really enhance mindfulness. Did this spark influence your journaling today?",
     "Yes, I added sketches, observations, and reflections about how visual art affects my emotions.",
     "Taking time to observe and reflect on your surroundings fosters mindfulness and encourages creative expression.")
]


def populate():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("DROP TABLE IF EXISTS messages")
    c.execute("DROP TABLE IF EXISTS entries")
    
    c.execute('''
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            turn_order INTEGER NOT NULL,
            FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE
        )
    ''')
    
    c.execute('CREATE INDEX idx_entries_date ON entries(date)')
    c.execute('CREATE INDEX idx_messages_entry ON messages(entry_id)')
    
    for entry in entries:
        date_str, mood, user1, ai1, user2, ai2, user3, ai_closing = entry
        created_at = datetime.fromisoformat(date_str + "T10:00:00").isoformat()
        
        c.execute(
            'INSERT INTO entries (date, mood, created_at) VALUES (?, ?, ?)',
            (date_str, mood, created_at)
        )
        entry_id = c.lastrowid
        
        messages = [
            ("user", user1, 1),
            ("ai", ai1, 2),
            ("user", user2, 3),
            ("ai", ai2, 4),
            ("user", user3, 5),
            ("ai", ai_closing, 6)
        ]
        
        for role, content, turn_order in messages:
            c.execute(
                'INSERT INTO messages (entry_id, role, content, turn_order) VALUES (?, ?, ?, ?)',
                (entry_id, role, content, turn_order)
            )
    
    conn.commit()
    conn.close()
    
    print(f"✅ Inserted {len(entries)} demo entries with normalized schema!")
    print("\nMood distribution:")
    mood_counts = {}
    for e in entries:
        mood = e[1]
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    for mood, count in sorted(mood_counts.items()):
        print(f"  {mood}: {count}")


if __name__ == "__main__":
    populate()

