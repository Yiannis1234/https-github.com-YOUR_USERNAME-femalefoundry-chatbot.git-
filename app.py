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
        body {font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif; background: #f8f9ff; color: #111826;}
        .chat-wrapper {max-width: 420px; margin: 0 auto; padding: 2.5rem 1.5rem;}
        .logo {font-weight: 800; font-size: 1.4rem; letter-spacing: 0.12em;}
        .chat-bubble {padding: 0.8rem 1rem; border-radius: 1.1rem; margin-bottom: 0.6rem; max-width: 100%;}
        .user-bubble {background: #ecebff; margin-left: auto;}
        .bot-bubble {background: #fff; border: 1px solid #e4e6f2;}
        .option-button {display: block; width: 100%; text-align: left; padding: 0.8rem; border-radius: 0.8rem;
            background: linear-gradient(135deg, #7b4dff, #ff60b2); color: #fff; font-weight: 600; border: none;}
        .option-button:hover {opacity: 0.9;}
        .footer {font-size: 0.75rem; color: #7d8090; text-align: center; margin-top: 1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "stage" not in st.session_state:
    st.session_state["stage"] = "intro"
    st.session_state["chat_log"] = []

chat_container = st.container()
button_container = st.container()

with chat_container:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="logo">FEMALE FOUNDRY</div>', unsafe_allow_html=True)

    if st.session_state["chat_log"]:
        for role, text in st.session_state["chat_log"]:
            bubble_class = "user-bubble" if role == "user" else "bot-bubble"
            st.markdown(f'<div class="chat-bubble {bubble_class}">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="chat-bubble bot-bubble">Hi! I’m the Female Foundry assistant. Shall we get started?</div>',
            unsafe_allow_html=True,
        )

with button_container:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    if st.session_state["stage"] == "intro":
        if st.button("I’m ready"):
            st.session_state["chat_log"].append(("bot", "First things first—what’s your name?"))
            st.session_state["stage"] = "ask_name"
            st.rerun()

    elif st.session_state["stage"] == "ask_name":
        name = st.text_input("Your name")
        if st.button("Continue"):
            if name.strip():
                st.session_state["visitor_name"] = name.strip().title()
                st.session_state["chat_log"].append(("user", name.strip().title()))
                st.session_state["chat_log"].append(
                    ("bot", f"Nice to meet you, {name.strip().title()}! Choose what you’d like to explore:")
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
            "Contact & Partners"
        ]
        for opt in options:
            if st.button(opt, key=opt):
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
            "Contact & Partners": ["Contact", "Partners", "Media coverage"]
        }
        for opt in sub_map.get(choice, []):
            if st.button(opt, key=opt):
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
            )
        }
        answer = info_map.get(st.session_state.get("sub_choice"), "")
        st.session_state["chat_log"].append(("bot", answer))
        st.session_state["chat_log"].append(("bot", "Anything else you'd like to explore?"))
        st.session_state["stage"] = "menu_primary"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chat-wrapper footer">Powered by Female Foundry • Embed this widget inside Wix via iframe.</div>', unsafe_allow_html=True)