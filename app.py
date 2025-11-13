from pathlib import Path
import json
import streamlit as st

DATA_PATH = Path("data/index.json")
with DATA_PATH.open("r", encoding="utf-8") as f:
    CONTENT = json.load(f)

# Build a simple knowledge base mapping question IDs to summaries
KNOWLEDGE = {}
for entry in CONTENT:
    if entry["id"].startswith("ff_site_") or entry["id"].startswith("survey_") or entry["id"].startswith("macro_") or entry["id"].startswith("headline_"):
        KNOWLEDGE[entry["id"]] = entry["answer"]

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
        }
        .chat-header-row div[data-testid="column"] {
            padding: 0 !important;
        }
        .chat-header-row div[data-testid="stButton"] {
            margin: 0 !important;
        }
        .chat-header-row .logo {
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: 0.08em;
            color: #2b1f63;
            text-transform: uppercase;
        }
        .chat-header-row div[data-testid="stButton"] > button {
            border: none;
            background: #ebeaff;
            color: #4537a0;
            border-radius: 10px;
            width: 32px;
            height: 32px;
            font-size: 1.1rem;
            cursor: pointer;
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
            padding: 0.75rem 0.9rem;
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
        .chat-footer {
            padding: 0.9rem 1rem 1.1rem;
            background: #ffffff;
            border-top: 1px solid #edf0ff;
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
        }
        .chat-footer-note {
            font-size: 0.72rem;
            color: #7d8090;
            text-align: center;
            padding: 0 1rem 0.9rem;
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
        .chat-footer div[data-testid="stTextInputRoot"] label {
            display: none;
        }
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
        .chat-launcher {
            position: fixed;
            right: 32px;
            bottom: 32px;
            z-index: 1200;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.35rem;
        }
        .chat-launcher div[data-testid="stButton"] {
            margin: 0 !important;
        }
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
        header_cols = st.columns([0.8, 0.2])
        with header_cols[0]:
            st.markdown('<div class="logo">Female Foundry</div>', unsafe_allow_html=True)
        with header_cols[1]:
            if st.button("✖", key="close_chat"):
                st.session_state["chat_open"] = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chat-body">', unsafe_allow_html=True)
        if st.session_state["chat_log"]:
            for role, text in st.session_state["chat_log"]:
                role_class = "user" if role == "user" else ""
                st.markdown(f'<div class="chat-bubble {role_class}">{text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="chat-bubble">Hi! I’m the Female Foundry assistant. Shall we get started?</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chat-footer">', unsafe_allow_html=True)

        titles = {
            "intro": "Ready to begin?",
            "ask_name": "Tell me your name",
            "menu_primary": "Choose what to explore",
            "menu_secondary": "Fine‑tune your choice",
            "show_info": "Here’s what I found",
        }
        st.markdown(
            f'<div class="chat-footer-title">{titles.get(st.session_state["stage"], "Continue")}</div>',
            unsafe_allow_html=True,
        )

        if st.session_state["stage"] == "intro":
            if st.button("I’m ready", key="cta_ready"):
                st.session_state["chat_log"].append(("bot", "First things first—what’s your name?"))
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
                        ("bot", f"Nice to meet you, {pretty_name}! Choose what you’d like to explore:")
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
                "Headline metrics": KNOWLEDGE.get("headline_female_founders_2024"),
                "Deep Tech & AI": KNOWLEDGE.get("science_stem_female_founders"),
                "Using the Index": (
                    "Use the Index’s funnel metrics plus Dealroom exports (DR_FF_C_1 for VC into female-founded companies, "
                    "DR_MC_C_5 for monthly totals) to build investment memos and monitor trends. "
                    "The homepage’s ‘Female Innovation Index’ section links straight to the 2025 edition."
                ),
                "AI Visionaries": (
                    "Female Foundry’s AI incubator with Google Cloud supports founders experimenting with frontier AI. "
                    "Click “Visit AI Visionaries” on the hero section to view cohorts, mentors, and application timing."
                ),
                "AI Hustle": (
                    "AI Hustle is a free monthly 1-hour clinic with Agata Nowicka (up to three founders per session). "
                    "Hit “Sign Up” in the AI Hustle panel to request a slot."
                ),
                "Sunday Newsletter": (
                    "Stay informed with the Sunday Newsletter—venture news, fundraising tips, ecosystem insights. "
                    "Select “Read” in the newsletter section to subscribe."
                ),
                "Join the community": (
                    "Join the 7,000+ strong community of founders, investors, and operators via the “Join the Community” button. "
                    "It unlocks intros, resources, and access to Female Foundry programs."
                ),
                "Campaigns": (
                    "Scroll to “Celebrating female founders” and tap “Watch all” to see storytelling campaigns filmed from a female perspective."
                ),
                "Shop": (
                    "The Female Foundry Shop (linked in the footer) offers identity assets and merchandise—ideal for events, partners, or supporter gifts."
                ),
                "Contact": KNOWLEDGE.get("ff_site_contact"),
                "Partners": KNOWLEDGE.get("ff_site_navigation"),
                "Media coverage": (
                    "Female Foundry is featured in FT Adviser, Maddyness, tech.eu, UKTN, Sifted, Startups Magazine, TFN and more. "
                    "Use these logos (shown above the partner grid) in your decks or press materials."
                ),
            }
            answer = info_map.get(st.session_state.get("sub_choice"), "")
            st.session_state["chat_log"].append(("bot", answer))
            st.session_state["chat_log"].append(("bot", "Anything else you'd like to explore?"))
            st.session_state["stage"] = "menu_primary"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # close footer
        st.markdown('<div class="chat-footer-note">Powered by Female Foundry • Embed this widget inside Wix via iframe.</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)  # close card and shell