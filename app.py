from pathlib import Path
import json
import html
import streamlit as st

DATA_PATH = Path("data/index.json")
with DATA_PATH.open("r", encoding="utf-8") as f:
    CONTENT = json.load(f)

# Build a simple knowledge base mapping question IDs to summaries
KNOWLEDGE = {}
for entry in CONTENT:
    if entry["id"].startswith("ff_site_") or entry["id"].startswith("survey_") or entry["id"].startswith("macro_") or entry["id"].startswith("headline_"):
        KNOWLEDGE[entry["id"]] = entry["answer"]


def format_bot_message(text: str) -> str:
    """Return HTML-safe bot message formatted as bullet list when helpful."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""

    bullet_mode = len(lines) > 1 or any(line[:1] in {"•", "-", "*"} for line in lines)
    if bullet_mode:
        cleaned = []
        for line in lines:
            if line[:1] in {"•", "-", "*"}:
                line = line[1:].strip()
            cleaned.append(html.escape(line))
        items = "".join(f"<li>{line}</li>" for line in cleaned)
        return f"<ul class='bot-list'>{items}</ul>"

    return html.escape(lines[0])


def reset_chat():
    """Clear chat history and restart onboarding flow."""
    st.session_state["chat_log"] = []
    st.session_state["stage"] = "intro"
    st.session_state.pop("visitor_name", None)
    st.rerun()

st.set_page_config(page_title="Female Foundry Chatbot", page_icon="🤖", layout="centered")

st.markdown(
    """
    <style>
        :root, body {
            background: linear-gradient(180deg, #f5f4ff 0%, #eff4ff 100%) !important;
            color: #111826;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .stApp > header, .stApp > footer { display: none; }
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="stAppViewContainer"] {
            background: transparent !important;
            padding: 0 !important;
        }
        [data-testid="stAppViewContainer"] > .main {
            background: transparent !important;
            padding: 0 !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        .chat-shell {
            position: fixed;
            right: 32px;
            bottom: 160px;
            width: 360px;
            z-index: 1200;
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        .chat-card {
            background: #ffffff;
            border: 1px solid #dfe3fb;
            border-radius: 18px;
            box-shadow: 0 28px 42px rgba(32, 28, 92, 0.2);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .chat-header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #f7f8ff;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #edf0ff;
            gap: 0.5rem;
        }
        .chat-header-row div[data-testid="column"] { padding: 0 !important; }
        .chat-header-row div[data-testid="stButton"] { margin: 0 !important; }
        .chat-header-row .logo {
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: 0.08em;
            color: #2b1f63;
            text-transform: uppercase;
        }
        .chat-header-row div[data-testid="stButton"] > button {
            width: 36px;
            height: 36px;
            border: none;
            border-radius: 12px;
            background: #ebeaff;
            color: #4537a0;
            font-size: 1.05rem;
            cursor: pointer;
            padding: 0;
        }
        .chat-header-row div[data-testid="stButton"] > button:hover {
            filter: brightness(0.97);
        }
        .chat-body {
            background: #fafaff;
            padding: 1rem;
            max-height: 280px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }
        .chat-bubble {
            padding: 0.78rem 0.95rem;
            border-radius: 12px;
            font-size: 0.95rem;
            line-height: 1.5rem;
            background: #fff;
            border: 1px solid #e3e5fb;
            color: #2f3252;
        }
        .chat-bubble.user {
            margin-left: auto;
            background: #ede9ff;
            border-color: #d5cffc;
            color: #2b2262;
        }
        .chat-bubble ul.bot-list,
        ul.bot-list {
            padding-left: 1.1rem;
            margin: 0;
            list-style: disc;
        }
        .chat-bubble ul.bot-list li { margin-bottom: 0.35rem; }
        .chat-footer {
            padding: 0.95rem 1rem 1.1rem;
            background: #ffffff;
            border-top: 1px solid #edf0ff;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
        }
        .chat-footer-title {
            font-size: 0.9rem;
            font-weight: 600;
            color: #2b2262;
        }
        .chat-footer div[data-testid="stTextInputRoot"] input {
            border-radius: 12px;
            border: 1px solid #d9dcf9;
            padding: 0.7rem 0.85rem;
            font-size: 0.95rem;
            color: #2b2262;
        }
        .chat-footer div[data-testid="stTextInputRoot"] label { display: none; }
        .chat-footer div[data-testid="stButton"] { margin-bottom: 0.4rem; }
        .chat-footer div[data-testid="stButton"]:last-child { margin-bottom: 0; }
        .chat-footer div[data-testid="stButton"] > button {
            width: 100%;
            text-align: left;
            padding: 0.75rem 0.9rem;
            border-radius: 12px;
            border: 1px solid #d6d9f9;
            background: #f4f4ff;
            color: #2b2262;
            font-weight: 600;
            font-size: 0.95rem;
        }
        .chat-footer div[data-testid="stButton"] > button:hover {
            border-color: #b8bcf3;
            background: #ebe9ff;
        }
        .chat-footer-note {
            font-size: 0.72rem;
            color: #7d8090;
            text-align: center;
            padding: 0.75rem 1rem 0.9rem;
        }
        .chat-launcher {
            position: fixed;
            right: 32px;
            bottom: 32px;
            z-index: 1100;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.35rem;
        }
        .chat-launcher div[data-testid="stButton"] { margin: 0 !important; }
        .chat-launcher div[data-testid="stButton"] > button {
            width: 58px;
            height: 58px;
            border-radius: 50%;
            border: none;
            background: linear-gradient(135deg, #7c63ff, #a879ff);
            color: #fff;
            font-size: 1.5rem;
            box-shadow: 0 18px 32px rgba(45, 37, 89, 0.24);
        }
        .chat-launcher .launcher-label {
            margin-top: 0.4rem;
            text-align: center;
            font-size: 0.75rem;
            font-weight: 600;
            color: #2c1f6c;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        @media (max-width: 640px) {
            .chat-shell { width: min(360px, calc(100vw - 32px)); right: 16px; bottom: 140px; }
            .chat-launcher { right: 18px; bottom: 20px; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "chat_open" not in st.session_state:
    st.session_state["chat_open"] = True

if "stage" not in st.session_state:
    st.session_state["stage"] = "intro"
    st.session_state["chat_log"] = []

launcher_clicked = False
launcher_container = st.empty()
with launcher_container:
    if not st.session_state["chat_open"]:
        st.markdown('<div class="chat-launcher">', unsafe_allow_html=True)
        launcher_clicked = st.button("💬", key="chat_launcher_button")
        st.markdown('<div class="launcher-label">Chat</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        launcher_clicked = False

if launcher_clicked:
    st.session_state["chat_open"] = not st.session_state["chat_open"]
    st.rerun()

if st.session_state["chat_open"]:
    shell = st.container()
    with shell:
        st.markdown('<div class="chat-shell"><div class="chat-card">', unsafe_allow_html=True)

        st.markdown('<div class="chat-header-row">', unsafe_allow_html=True)
        header_cols = st.columns([0.6, 0.2, 0.2], gap="small")
        with header_cols[0]:
            st.markdown('<div class="logo">Female Foundry</div>', unsafe_allow_html=True)
        with header_cols[1]:
            if st.button("↺", key="reset_chat_btn", help="Start over"):
                reset_chat()
        with header_cols[2]:
            if st.button("✖", key="close_chat_btn", help="Hide chat"):
                st.session_state["chat_open"] = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chat-body">', unsafe_allow_html=True)
        if st.session_state["chat_log"]:
            for role, text in st.session_state["chat_log"]:
                if role == "user":
                    safe_text = html.escape(text)
                    st.markdown(f'<div class="chat-bubble user">{safe_text}</div>', unsafe_allow_html=True)
                else:
                    content = text if ("<" in text and ">" in text) else html.escape(text)
                    st.markdown(f'<div class="chat-bubble">{content}</div>', unsafe_allow_html=True)
        else:
            intro_msg = format_bot_message("Hi! I’m the Female Foundry assistant. Shall we get started?")
            st.markdown(f'<div class="chat-bubble">{intro_msg}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chat-footer">', unsafe_allow_html=True)

        titles = {
            "intro": "Ready to begin?",
            "ask_name": "Tell me your name",
            "menu_primary": "Choose what to explore",
            "menu_secondary": "Fine-tune your choice",
            "show_info": "Here’s what I found",
        }
        st.markdown(
            f'<div class="chat-footer-title">{titles.get(st.session_state["stage"], "Continue")}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state["stage"] == "intro":
            if st.button("I’m ready", key="cta_ready"):
                st.session_state["chat_log"].append(("bot", format_bot_message("First things first—what’s your name?")))
                st.session_state["stage"] = "ask_name"
                st.rerun()

        elif st.session_state["stage"] == "ask_name":
            name = st.text_input(
                "Your name",
                key="visitor_name_input",
                placeholder="Type your name…",
                label_visibility="collapsed",
            )
            if st.button("Continue", key="visitor_name_submit"):
                if name.strip():
                    pretty_name = name.strip().title()
                    st.session_state["visitor_name"] = pretty_name
                    st.session_state["chat_log"].append(("user", pretty_name))
                    st.session_state["chat_log"].append(
                        ("bot", format_bot_message(f"Nice to meet you, {pretty_name}! Choose what you’d like to explore:"))
                    )
                    st.session_state["stage"] = "menu_primary"
                    st.rerun()
                else:
                    st.warning("Let’s capture your name before we go on.")

        elif st.session_state["stage"] == "menu_primary":
            options = [
                "VC & Funding Insights",
                "Female Foundry Programs",
                "Community & Stories",
                "Contact & Partners",
            ]
            for opt in options:
                if st.button(opt, key=f"primary_{opt}"):
                    st.session_state["chat_log"].append(("user", opt))
                    st.session_state["primary_choice"] = opt
                    st.session_state["stage"] = "menu_secondary"
                    st.rerun()

        elif st.session_state["stage"] == "menu_secondary":
            choice = st.session_state.get("primary_choice")
            sub_map = {
                "VC & Funding Insights": ["Headline metrics", "Deep Tech & AI", "Using the Index"],
                "Female Foundry Programs": ["AI Visionaries", "AI Hustle", "Sunday Newsletter"],
                "Community & Stories": ["Join the community", "Campaigns", "Shop"],
                "Contact & Partners": ["Contact", "Partners", "Media coverage"],
            }
            for opt in sub_map.get(choice, []):
                if st.button(opt, key=f"secondary_{opt}"):
                    st.session_state["chat_log"].append(("user", opt))
                    st.session_state["sub_choice"] = opt
                    st.session_state["stage"] = "show_info"
                    st.rerun()

        elif st.session_state["stage"] == "show_info":
            info_map = {
                "Headline metrics": (
                    "• €5.76B raised by female-founded startups in Europe during 2024 (1,305 deals across 1,196 companies).\n"
                    "• Represents roughly 12% of all European VC; deep tech attracts about one-third of that capital.\n"
                    "• The Female Innovation Index aggregates 1,200+ survey responses and tracks 145k+ companies."
                ),
                "Deep Tech & AI": (
                    "• Deep tech companies capture roughly one-third of the capital raised by female-founded startups.\n"
                    "• Data & AI founders cite funding (67 mentions) and slow adoption (47) as top bottlenecks.\n"
                    "• Health & life-science founders echo funding, adoption, and economic uncertainty challenges—filter Dealroom tags for precise counts."
                ),
                "Using the Index": (
                    "• Use Dealroom exports DR_FF_C_1 (female-founded VC) and DR_MC_C_5 (monthly capital) for charts.\n"
                    "• Funnel views reveal drop-off points across awareness, acceleration, and funding.\n"
                    "• Start from the 2025 Index landing page for methodology and download links."
                ),
                "AI Visionaries": (
                    "• Female Foundry’s AI incubator with Google Cloud for frontier AI founders.\n"
                    "• ‘Visit AI Visionaries’ shows cohorts, mentors, curriculum, and application windows.\n"
                    "• Offers tailored GTM support, mentor office hours, and showcase opportunities."
                ),
                "AI Hustle": (
                    "• Free monthly 1-hour clinic with Agata Nowicka (up to three founders).\n"
                    "• Tap the homepage ‘Sign Up’ CTA to request a slot.\n"
                    "• Ideal for quick GTM troubleshooting, warm intros, and accountability."
                ),
                "Sunday Newsletter": (
                    "• Weekly roundup covering funding news, founder tactics, and ecosystem signals.\n"
                    "• Use the homepage ‘Read’ button to browse the latest edition or subscribe.\n"
                    "• Designed for female founders, operators, and allies tracking European venture."
                ),
                "Join the community": (
                    "• 7,000+ founders, investors, and operators focused on female-led innovation.\n"
                    "• Click ‘Join the Community’ to request access to intros, events, and resources.\n"
                    "• Members tap curated deal flow, mentor sessions, and partner offers."
                ),
                "Campaigns": (
                    "• ‘Celebrating female founders’ spotlights stories you can feature or amplify.\n"
                    "• Use the ‘Watch all’ CTA to stream short films and social assets.\n"
                    "• Great for investor updates, internal culture decks, or event content."
                ),
                "Shop": (
                    "• Female Foundry Shop offers identity assets, merch, and partner gifting ideas.\n"
                    "• Linked from the site footer—ships worldwide with limited drops.\n"
                    "• Popular for event swag, partner onboarding, or community giveaways."
                ),
                "Contact": (
                    "• Email HELLO@FEMALEFOUNDRY.CO for partnerships or press.\n"
                    "• HQ: 11 Welbeck Street, W1G 9XZ, London (by appointment).\n"
                    "• Footer also links to About, Partners, Careers, and Privacy Policy."
                ),
                "Partners": (
                    "• Explore corporate and ecosystem partners via the footer link.\n"
                    "• Collaboration areas include scouting, thought leadership, and program support.\n"
                    "• Submit interest through the partner form for a follow-up call."
                ),
                "Media coverage": (
                    "• Featured in FT Adviser, Maddyness, tech.eu, UKTN, Sifted, Startups Magazine, TFN, and more.\n"
                    "• Logos appear above the partner grid for easy export to decks.\n"
                    "• Cite coverage to boost credibility with LPs, corporates, or press."
                ),
            }
            answer = info_map.get(st.session_state.get("sub_choice"), "")
            formatted = format_bot_message(answer)
            st.session_state["chat_log"].append(("bot", formatted))
            st.session_state["chat_log"].append(("bot", format_bot_message("Anything else you'd like to explore?")))
            st.session_state["stage"] = "menu_primary"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # close footer
        st.markdown('<div class="chat-footer-note">Powered by Female Foundry • Embed this widget inside Wix via iframe.</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)  # close card and shell