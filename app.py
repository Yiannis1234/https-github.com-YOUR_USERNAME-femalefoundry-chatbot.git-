import streamlit as st

st.set_page_config(
    page_title="Female Foundry Navigator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
    body {
        font-family: "Inter", "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
        background: radial-gradient(circle at top, #fdf6ff 0%, #f4f7ff 35%, #f2f4f8 100%) !important;
        color: #161d2b;
    }
    [data-testid="stAppViewContainer"] {
        background: transparent;
    }
    [data-testid="stHeader"] {
        background: transparent;
        border-bottom: none;
    }
    .main .block-container {
        max-width: 980px;
        margin: 0 auto;
        padding: 2.5rem 2.5rem 5rem !important;
    }
    .hero-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(123,77,255,0.12);
        border-radius: 32px;
        padding: 2.4rem;
        margin-bottom: 2rem;
        box-shadow: 0 24px 68px rgba(23, 32, 54, 0.08);
    }
    .hero-card h1 {
        font-size: clamp(2.2rem, 4vw, 3rem);
        margin: 0 0 0.8rem 0;
        letter-spacing: -0.5px;
    }
    .hero-card p {
        font-size: 1.05rem;
        color: #475067;
        margin: 0;
    }
    .option-card {
        background: rgba(255,255,255,0.88);
        border-radius: 20px;
        padding: 1.8rem;
        border: 1px solid rgba(123,77,255,0.08);
        box-shadow: 0 16px 40px rgba(20, 21, 36, 0.06);
        margin-top: 1rem;
    }
    .option-card h3 {
        margin-top: 0;
        margin-bottom: 0.6rem;
    }
    .cta-link {
        display: inline-block;
        margin-top: 0.4rem;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        background: linear-gradient(135deg, #7b4dff, #ff60b2);
        color: #fff !important;
        font-weight: 600;
        text-decoration: none;
    }
    .reset-btn > button {
        background: transparent;
        color: #7b4dff;
        border: 1px solid rgba(123,77,255,0.25);
        border-radius: 999px;
        padding: 0.4rem 1.1rem;
    }
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem 1.2rem 5rem !important;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

GUIDED_CONTENT = {
    "VC & Funding Insights": {
        "Headline metrics (2024)": {
            "summary": (
                "Female-founded startups raised **€5.76B across 1,305 deals** in Europe during 2024, representing **1,196 companies** "
                "(around 12% of total VC). The Female Innovation Index aggregates data from 1,215 survey respondents and 145,038 European companies."
            ),
            "bullets": [
                "Use the Index to benchmark the innovation funnel, from idea-stage to growth funding.",
                "Filter by country, sector, or stage to monitor where female founders are gaining momentum.",
                "Combine survey evidence with Dealroom data for investment memos or LP updates."
            ],
            "links": [
                ("Explore the Female Innovation Index (2025 edition)", "https://www.femalefoundry.co/"),
                ("Request datasets via Dealroom (DR_FF_C_1, DR_MC_C_5, etc.)", "https://www.femalefoundry.co/")
            ]
        },
        "Deep Tech & AI focus": {
            "summary": (
                "About **one-third of 2024 capital raised by female-founded startups flowed into Deep Tech and AI ventures**. "
                "Survey respondents in Data & AI (136 founders) cited access to funding (67 mentions), slow tech adoption (47), cultural norms (29) "
                "and economic uncertainty (24) as top hurdles."
            ),
            "bullets": [
                "Deep Tech and health ventures highlight the largest funding needs by ticket size.",
                "Use these insights to prioritise scouting or investment theses in frontier tech.",
                "Pair survey narratives with deal-level data to evidence the opportunity."
            ],
            "links": [
                ("Download Deep Tech overview", "https://www.femalefoundry.co/"),
                ("Visit AI Visionaries", "https://www.femalefoundry.co/")
            ]
        },
        "How to use the Index": {
            "summary": (
                "The Index provides funnel metrics across sectors. Pair it with Female Foundry campaigns and community intel to support fundraising, diligence, or policy briefs."
            ),
            "bullets": [
                "Cross-reference company profiles with the Female Foundry community for warm introductions.",
                "Identify under-served segments or stages for accelerator cohorts.",
                "Prompt visitors to request the dataset inside Wix via a form or CRM action."
            ],
            "links": [
                ("Access ecosystem data", "https://www.femalefoundry.co/")
            ]
        }
    },
    "Female Foundry Programs": {
        "AI Visionaries incubator": {
            "summary": (
                "Flagship incubator in partnership with Google Cloud supporting AI-native founders. The homepage CTA ‘Visit AI Visionaries’ leads to cohorts, mentors, and application details."
            ),
            "bullets": [
                "Ideal for founders building frontier AI products in Europe.",
                "Backed by Google Cloud mentors and Female Foundry’s network.",
                "Embed the CTA in Wix to drive applications or discovery calls."
            ],
            "links": [("Visit AI Visionaries", "https://www.femalefoundry.co/")]
        },
        "AI Hustle sessions": {
            "summary": (
                "Free monthly 1-hour clinics with Agata Nowicka for up to three founders. Focus on growth, GTM, connections, or bottleneck busting in the AI era."
            ),
            "bullets": [
                "Apply via the ‘Sign Up’ CTA on the homepage.",
                "Great for founders transitioning from MVP to traction.",
                "Use in Wix to drive bookings or integrate Calendly." 
            ],
            "links": [("Reserve an AI Hustle slot", "https://www.femalefoundry.co/")]
        },
        "Sunday Newsletter": {
            "summary": (
                "Weekly digest covering venture news, fundraising tips, and ecosystem insights for female founders and investors."
            ),
            "bullets": [
                "Use the ‘Read’ CTA to subscribe.",
                "Share with portfolio founders or LPs to keep them informed.",
                "Automate signup via Wix forms connected to your mailing tool."
            ],
            "links": [("Subscribe to the Sunday Newsletter", "https://www.femalefoundry.co/")]
        }
    },
    "Community & Storytelling": {
        "Join the 7,000+ community": {
            "summary": (
                "Female Foundry’s community spans 7,000+ founders, investors, advisers, and ecosystem shapers. The homepage invites you to ‘Join the Community’."
            ),
            "bullets": [
                "Membership unlocks curated introductions, programs, and resources.",
                "Useful call to action for investors seeking deal flow or partners backing founders.",
                "Embed the join form inside Wix and sync submissions to your CRM."
            ],
            "links": [("Join the Female Foundry community", "https://www.femalefoundry.co/")]
        },
        "Campaigns & storytelling": {
            "summary": (
                "The ‘Celebrating female founders’ section highlights video campaigns and stories from a female perspective." 
            ),
            "bullets": [
                "Use campaigns for media outreach or sponsor showcases.",
                "Feature videos inside Wix to keep visitors engaged.",
                "Great inspiration for founders building their narrative."
            ],
            "links": [("Watch campaigns", "https://www.femalefoundry.co/")]
        },
        "Female Foundry Shop": {
            "summary": "Homepage footer links to the Shop where supporters can buy branded identity assets and merchandise.",
            "bullets": [
                "Perfect for welcome packs, event swag, or gifting.",
                "You can deep-link directly from Wix to the shop page.",
                "Helps reinforce Female Foundry identity." 
            ],
            "links": [("Visit the Shop", "https://www.femalefoundry.co/")]
        }
    },
    "Contact & Partners": {
        "Contact & location": {
            "summary": "HQ: 11 Welbeck Street, W1G 9XZ, London. Email: HELLO@FEMALEFOUNDRY.CO.",
            "bullets": [
                "Add these details to your Wix contact widgets.",
                "Use the email link to trigger CRM automations.",
                "Include address and email in investor decks." 
            ],
            "links": [
                ("Email Female Foundry", "mailto:HELLO@FEMALEFOUNDRY.CO"),
                ("Open in Google Maps", "https://maps.google.com/?q=11+Welbeck+Street,+W1G+9XZ+London")
            ]
        },
        "Partners & collaborators": {
            "summary": (
                "Homepage partner grid features Impact Shakers, LPEA, SuperReturn International, AustrianStartups, Tech Barcelona, Slush, London Stock Exchange, IVCA, and more." 
            ),
            "bullets": [
                "Showcase this partner list to attract sponsors or new collaborators.",
                "Link logos to partner pages inside Wix.",
                "Use the list in pitch decks or media kits." 
            ],
            "links": [("View partner list", "https://www.femalefoundry.co/")]
        },
        "Media coverage": {
            "summary": "Female Foundry has been featured in FT Adviser, Maddyness, tech.eu, UKTN, Sifted (Financial Times), Startups Magazine, TFN, and others.",
            "bullets": [
                "Great proof points for credibility slides.",
                "Add media logos to the Wix footer or press section.",
                "Link to clippings in Notion or Google Drive for press follow-ups." 
            ],
            "links": [("Download press kit", "https://www.femalefoundry.co/")]
        }
    }
}


def reset_conversation():
    for key in ["visitor_name", "primary_choice"]:
        if key in st.session_state:
            del st.session_state[key]


st.markdown(
    '<div class="hero-card"><h1>Female Foundry Navigator</h1><p>Guide visitors through the Female Foundry ecosystem. '
    "Embed this flow inside Wix for a guided, button-first experience.</p></div>",
    unsafe_allow_html=True,
)

if "visitor_name" not in st.session_state:
    st.session_state["visitor_name"] = ""

if not st.session_state["visitor_name"]:
    st.markdown("### 👋 Welcome! Let’s personalise your journey.")
    name_input = st.text_input("What’s your name?")
    start_clicked = st.button("Start exploring")
    if start_clicked:
        if name_input.strip():
            st.session_state["visitor_name"] = name_input.strip().title()
            st.experimental_rerun()
        else:
            st.warning("Please enter a name to continue.")
    st.stop()

st.markdown(f"### Hi {st.session_state['visitor_name']}! What would you like to explore?")

primary_options = list(GUIDED_CONTENT.keys())
primary_choice = st.radio(
    "Pick a path:",
    primary_options,
    key="primary_choice",
    horizontal=True,
)

sub_options = list(GUIDED_CONTENT[primary_choice].keys())
sub_choice_key = f"{primary_choice}_sub_choice"
sub_choice = st.radio(
    "Choose a topic to get a concise briefing:",
    sub_options,
    key=sub_choice_key,
)

selected_info = GUIDED_CONTENT[primary_choice][sub_choice]

st.markdown(
    f'<div class="option-card"><h3>{sub_choice}</h3><p>{selected_info["summary"]}</p></div>',
    unsafe_allow_html=True,
)

st.markdown("###### Why it matters")
for bullet in selected_info.get("bullets", []):
    st.markdown(f"- {bullet}")

if selected_info.get("links"):
    st.markdown("###### Quick actions")
    for label, url in selected_info["links"]:
        st.markdown(f"- [{label}]({url})")

st.divider()
st.markdown(
    "Need a different path? Use the reset button below. When embedding in Wix, you can capture the visitor’s name and choices "
    "with Velo to log interest in specific programs or datasets."
)

if st.button("↺ Start over", key="reset", help="Reset name and selections", on_click=reset_conversation):
    st.experimental_rerun()
