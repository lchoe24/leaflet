import streamlit as st
from datetime import date, timedelta
from services.leafy import leafy
from services.database import get_all_entries, get_entry_by_date, save_entry
from utils.config import (
    MOOD_OPTIONS, MOOD_ORDER,
    get_mood_display, get_mood_value, get_mood_color, get_mood_emoji,
    JOURNAL_MODES, DEFAULT_SESSION_STATE
)
from utils.helpers import get_weekly_garden, calculate_mood_stats
from ui.components import (
    chat_bubble, locked_card, mode_card, prompt_card,
    section_header, challenge_item, info_text, spacer
)

st.set_page_config(page_title="Leaflet", page_icon="🍃", layout="centered")

def load_css():
    with open("ui/styles.css", "r") as f:
        return f"<style>{f.read()}</style>"

st.markdown(load_css(), unsafe_allow_html=True)

for key, default in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = default

today_str = date.today().isoformat()
today_entry = get_entry_by_date(today_str)
greeting = "Hello there!"
days, week_display, days_journaled = get_weekly_garden()

st.markdown("""
<div style='text-align:center;'>
    <h1 style='margin:0; padding:0; line-height:1;'>🍃 Leaflet</h1>
    <p style='color:rgba(255,255,255,0.15); font-style:italic; margin:0.1rem 0 1.25rem 0; font-size:0.85rem; opacity:0.8;'>where thoughts come to rest</p>
</div>
""", unsafe_allow_html=True)

day_icons = "".join([
    f"<div style='display:inline-block; text-align:center; margin:0 0.4rem;'><div style='font-size:0.6rem; color:rgba(255,255,255,0.4);'>{day}</div><div style='font-size:1.3rem;'>{plant}</div></div>"
    for day, plant in zip(days, week_display)
])
st.markdown(f"""
<div style='text-align:center; margin-bottom:1rem;'>
    {day_icons}
    <span style='color:rgba(255,255,255,0.4); font-size:0.75rem; margin-left:0.5rem;'>({days_journaled}/7)</span>
</div>
""", unsafe_allow_html=True)

tab_journal, tab_challenges, tab_insights, tab_history = st.tabs(["✍️ Journal", "🎯 Challenges", "📊 Insights", "📚 History"])

with tab_challenges:
    past_entries = [e for e in get_all_entries() if e['date'] != today_str]
    
    if not today_entry:
        locked_card("🔒", "Challenges Locked", "Complete today's journal entry to unlock your personalized challenges")
    elif not past_entries:
        locked_card("🎯", "Keep Journaling!", "Write a few more entries so Leafy can learn your interests and create personalized challenges.")
    else:
        section_header("🎯", "Today's Tiny Challenges", "Small steps inspired by your journey")
        
        if 'daily_challenges' not in st.session_state or st.session_state.get('challenges_date') != today_str:
            with st.spinner("Creating your challenges..."):
                st.session_state.daily_challenges = leafy.generate_challenges(past_entries[-10:])
                st.session_state.challenges_date = today_str
        
        for i, challenge in enumerate(st.session_state.daily_challenges, 1):
            challenge_item(i, challenge)
        
        info_text("Come back and tell Leafy how it went! 💬")
        
        if st.button("🔄 New Challenges", use_container_width=True):
            if 'daily_challenges' in st.session_state:
                del st.session_state.daily_challenges
            st.rerun()

with tab_history:
    entries = get_all_entries()
    
    if not entries:
        st.info("No entries yet. Start journaling!")
    else:
        for idx, entry in enumerate(entries):
            with st.expander(f"📅 {entry['date']} - {get_mood_display(entry['mood'])}", expanded=False):
                for msg in entry.get('messages', []):
                    role = "You" if msg['role'] == 'user' else "Leafy"
                    st.markdown(chat_bubble(role, msg['content']), unsafe_allow_html=True)

with tab_insights:
    if not today_entry:
        locked_card("🔒", "Insights Locked", "Complete today's journal entry to unlock your mood insights")
    else:
        entries = get_all_entries()
        
        if len(entries) < 3:
            st.info("Journal a few more days to see your mood insights!")
        else:
            thirty_days_ago = date.today() - timedelta(days=30)
            last_30_days = [
                e for e in entries 
                if e.get('date') and date.fromisoformat(e['date']) >= thirty_days_ago
            ]
            
            mood_counts, total, top_mood = calculate_mood_stats(last_30_days)
            
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:1.5rem;'>
                <div>
                    <h3 style='margin:0;'>Last 30 Days</h3>
                    <p style='color:rgba(255,255,255,0.5); margin:0.25rem 0 0 0; font-size:0.85rem;'>{total} entries</p>
                </div>
                <div style='text-align:right;'>
                    <p style='color:rgba(255,255,255,0.5); margin:0; font-size:0.75rem;'>Most frequent</p>
                    <p style='margin:0; font-size:1.1rem;'>{get_mood_emoji(top_mood)} {top_mood}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            bar_segments = "".join([
                f"<div style='width:{(mood_counts[mood]/total)*100}%; background:{get_mood_color(mood)}; height:100%;' title='{mood}: {mood_counts[mood]}'></div>"
                for mood in MOOD_ORDER if mood_counts[mood] > 0
            ])
            
            st.markdown(f"""
            <div style='display:flex; height:12px; border-radius:6px; overflow:hidden; margin-bottom:1rem;'>
                {bar_segments}
            </div>
            """, unsafe_allow_html=True)
            
            legend_items = "".join([
                f"<span style='margin-right:1rem; font-size:0.8rem;'><span style='color:{get_mood_color(mood)};'>●</span> {get_mood_emoji(mood)} {mood_counts[mood]}</span>"
                for mood in MOOD_ORDER if mood_counts[mood] > 0
            ])
            
            st.markdown(f"<div style='display:flex; flex-wrap:wrap; justify-content:center; margin-bottom:1.5rem;'>{legend_items}</div>", unsafe_allow_html=True)
            
            st.markdown("### ✨ AI Summary")
            
            if 'mood_summary' not in st.session_state:
                with st.spinner("Analyzing your patterns..."):
                    st.session_state.mood_summary = leafy.generate_mood_summary(last_30_days)
            
            st.markdown(f"""
            <div style='background:rgba(233,69,96,0.1); border:1px solid rgba(233,69,96,0.2); border-radius:16px; padding:1.25rem; line-height:1.7; color:rgba(255,255,255,0.9);'>
                {st.session_state.mood_summary}
            </div>
            """, unsafe_allow_html=True)

with tab_journal:
    st.markdown(f"""
    <div style='text-align:center; padding: 0.5rem 0 0.5rem 0;'>
        <h2 style='margin: 0; font-size: 1.8rem;'>{greeting}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.journal_step == 0:
        st.markdown("<p style='text-align:center; color:rgba(255,255,255,0.7); margin-bottom:1rem;'>How would you like to journal today?</p>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, (mode_key, mode_data) in enumerate(JOURNAL_MODES.items()):
            with cols[i]:
                st.markdown(mode_card(mode_data["icon"], mode_data["title"], mode_data["subtitle"]), unsafe_allow_html=True)
                if st.button("Select", key=mode_key, use_container_width=True):
                    st.session_state.journal_mode = mode_key
                    st.session_state.journal_step = 1
                    
                    if mode_key == "reflective":
                        past_entries = get_all_entries()
                        st.session_state.welcome_prompt = leafy.generate_personalized_welcome(past_entries)
                    elif mode_key == "explore":
                        st.session_state.welcome_prompt = leafy.generate_exploration_prompt()
                    else:
                        st.session_state.welcome_prompt = None
                    st.rerun()
    
    elif st.session_state.journal_step == 1:
        if st.session_state.journal_mode in ["reflective", "explore"] and st.session_state.get('welcome_prompt'):
            mode_icon = JOURNAL_MODES[st.session_state.journal_mode]["icon"]
            prompt_card(mode_icon, st.session_state.welcome_prompt)
            
            if st.session_state.journal_mode == "explore":
                _, col_center, _ = st.columns([1, 1, 1])
                with col_center:
                    if st.button("🔄 New Prompt", use_container_width=True, key="regen_prompt"):
                        st.session_state.welcome_prompt = leafy.generate_exploration_prompt()
                        st.rerun()
                spacer("0.75rem")
                
        elif st.session_state.journal_mode == "freewrite":
            st.markdown("<div style='text-align:center; color:rgba(255,255,255,0.6); margin-bottom:1rem;'>📝 Your space to write freely. No prompts, no pressure.</div>", unsafe_allow_html=True)
        
        selected_mood_display = st.selectbox("How are you feeling?", MOOD_OPTIONS, index=1)
        selected_mood = get_mood_value(selected_mood_display)
        
        entry_1 = st.text_area(
            "Share your thoughts...",
            height=150,
            placeholder="Write freely... no judgment here.",
            key="journal_entry_1"
        )
        
        col_back, col_send = st.columns([1, 2])
        with col_back:
            if st.button("← Back", use_container_width=True):
                st.session_state.journal_step = 0
                st.session_state.journal_mode = None
                if 'welcome_prompt' in st.session_state:
                    del st.session_state.welcome_prompt
                st.rerun()
        with col_send:
            if st.button("Send", type="primary", use_container_width=True):
                if entry_1.strip():
                    st.session_state.mood = selected_mood
                    st.session_state.entry_1 = entry_1
                    
                    with st.spinner(""):
                        conversation = [{"role": "User", "text": entry_1}]
                        st.session_state.ai_response_1 = leafy.generate_response(conversation, selected_mood, is_closing=False)
                    
                    st.session_state.journal_step = 2
                    st.rerun()
    
    elif st.session_state.journal_step == 2:
        st.markdown(chat_bubble("You", st.session_state.entry_1), unsafe_allow_html=True)
        st.markdown(chat_bubble("Leafy", st.session_state.ai_response_1), unsafe_allow_html=True)
        
        entry_2 = st.text_area(
            "Your response...",
            height=100,
            placeholder="Continue sharing...",
            key="journal_entry_2"
        )
        
        if st.button("Send", type="primary"):
            if entry_2.strip():
                st.session_state.entry_2 = entry_2
                
                with st.spinner(""):
                    conversation = [
                        {"role": "User", "text": st.session_state.entry_1},
                        {"role": "Leafy", "text": st.session_state.ai_response_1},
                        {"role": "User", "text": entry_2}
                    ]
                    st.session_state.ai_closing = leafy.generate_response(conversation, st.session_state.mood, is_closing=True)
                
                st.session_state.journal_step = 3
                st.rerun()
    
    elif st.session_state.journal_step == 3:
        st.markdown(chat_bubble("You", st.session_state.entry_1), unsafe_allow_html=True)
        st.markdown(chat_bubble("Leafy", st.session_state.ai_response_1), unsafe_allow_html=True)
        st.markdown(chat_bubble("You", st.session_state.entry_2), unsafe_allow_html=True)
        st.markdown(chat_bubble("Leafy", st.session_state.ai_closing), unsafe_allow_html=True)
        
        messages = [
            {"role": "user", "content": st.session_state.entry_1},
            {"role": "ai", "content": st.session_state.ai_response_1},
            {"role": "user", "content": st.session_state.entry_2},
            {"role": "ai", "content": st.session_state.ai_closing}
        ]
        save_entry(today_str, st.session_state.mood, messages)
        
        st.success("✨ Journal entry complete!")
        spacer()
        
        if st.button("📝 Write Another Entry", use_container_width=True):
            st.session_state.journal_step = 0
            st.session_state.journal_mode = None
            st.session_state.entry_1 = ""
            st.session_state.ai_response_1 = ""
            st.session_state.entry_2 = ""
            st.session_state.ai_closing = ""
            if 'welcome_prompt' in st.session_state:
                del st.session_state.welcome_prompt
            st.rerun()
