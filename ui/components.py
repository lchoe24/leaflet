import streamlit as st


def chat_bubble(role: str, text: str) -> str:
    if role == "You" or role == "user":
        return f'<div class="bubble-label" style="text-align:right">You</div><div class="user-bubble">{text}</div>'
    else:
        return f'<div class="bubble-label">Leafy 🍃</div><div class="companion-bubble">{text}</div>'


def locked_card(icon: str, title: str, message: str) -> None:
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: 3rem 2rem;
        margin: 2rem 0;
    '>
        <div style='font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;'>{icon}</div>
        <h3 style='color: rgba(255,255,255,0.5); margin-bottom: 0.5rem;'>{title}</h3>
        <p style='color: rgba(255,255,255,0.4); font-size: 0.9rem;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def mode_card(icon: str, title: str, subtitle: str) -> str:
    return f"""
    <div style='text-align:center; padding:1rem; background:rgba(255,255,255,0.03); border-radius:12px; height:140px;'>
        <div style='font-size:2rem; margin-bottom:0.5rem;'>{icon}</div>
        <div style='font-weight:600; margin-bottom:0.25rem;'>{title}</div>
        <div style='font-size:0.75rem; color:rgba(255,255,255,0.5);'>{subtitle}</div>
    </div>
    """


def prompt_card(icon: str, text: str) -> None:
    st.markdown(f"""
    <div style='
        text-align: center;
        padding: 1rem 1.5rem;
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        margin-bottom: 0.75rem;
        border-left: 3px solid #e94560;
    '>
        <p style='color: rgba(255,255,255,0.8); font-style: italic; line-height: 1.6; margin: 0;'>{icon} {text}</p>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, title: str, subtitle: str = None) -> None:
    subtitle_html = f"<p style='color: rgba(255,255,255,0.5); font-size: 0.85rem;'>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div style='text-align: center; margin: 1.5rem 0;'>
        <div style='font-size: 2.5rem;'>{icon}</div>
        <h3 style='margin: 0.5rem 0 0.25rem 0;'>{title}</h3>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def challenge_item(number: int, text: str) -> None:
    st.markdown(f"""
    <div style='
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #e94560;
        padding: 0.75rem 1rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 0.75rem;
    '>
        <span style='color: #e94560; font-weight: 600;'>#{number}</span> {text}
    </div>
    """, unsafe_allow_html=True)


def info_text(text: str, centered: bool = True) -> None:
    align = "center" if centered else "left"
    st.markdown(f"<p style='text-align:{align}; color:rgba(255,255,255,0.4); font-size:0.8rem; margin-top:1rem;'>{text}</p>", unsafe_allow_html=True)


def spacer(height: str = "1rem") -> None:
    st.markdown(f"<div style='height: {height};'></div>", unsafe_allow_html=True)

