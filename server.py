from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Dict, List, Tuple
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

DATA_PATH = Path("data/index.json")
with DATA_PATH.open("r", encoding="utf-8") as f:
    CONTENT = json.load(f)

PRIMARY_OPTIONS = [
    "VC & Funding Insights",
    "Female Foundry Programs",
    "Community & Stories",
    "Contact & Partners",
]

SECONDARY_OPTIONS: Dict[str, List[str]] = {
    "VC & Funding Insights": ["Headline metrics", "Deep Tech & AI", "Using the Index"],
    "Female Foundry Programs": ["AI Visionaries", "AI Hustle", "Sunday Newsletter"],
    "Community & Stories": ["Join the community", "Campaigns", "Shop"],
    "Contact & Partners": ["Contact", "Partners", "Media coverage"],
}

INFO_MAP: Dict[str, str] = {
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


class ChatRequest(BaseModel):
    session_id: str
    message: str


class SessionResponse(BaseModel):
    session_id: str
    messages: List[Dict[str, str]]
    options: List[str]
    stage: str


def format_bot_message(text: str) -> str:
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


class SessionState:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.stage = "ask_name"
        self.visitor_name: str | None = None
        self.primary_choice: str | None = None
        self.history: List[Tuple[str, str]] = []
        greeting = format_bot_message("Hi! I’m the Female Foundry assistant. What’s your name?")
        self.history.append(("bot", greeting))

    def to_initial_response(self) -> SessionResponse:
        return SessionResponse(
            session_id=self.session_id,
            messages=[{"role": role, "content": content} for role, content in [self.history[-1]]],
            options=[],
            stage=self.stage,
        )


SESSIONS: Dict[str, SessionState] = {}


def create_session() -> SessionState:
    session_id = uuid4().hex
    state = SessionState(session_id)
    SESSIONS[session_id] = state
    return state


def get_session(session_id: str) -> SessionState:
    state = SESSIONS.get(session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Session not found")
    return state


def match_option(text: str, options: List[str]) -> str | None:
    lowered = text.strip().lower()
    for option in options:
        if lowered == option.lower():
            return option
    return None


def respond(state: SessionState, responses: List[str], options: List[str]) -> SessionResponse:
    for response in responses:
        state.history.append(("bot", response))
    return SessionResponse(
        session_id=state.session_id,
        messages=[{"role": "bot", "content": response} for response in responses],
        options=options,
        stage=state.stage,
    )


def reset_session(state: SessionState) -> SessionResponse:
    SESSIONS[state.session_id] = SessionState(state.session_id)
    return SESSIONS[state.session_id].to_initial_response()


def handle_message(state: SessionState, message: str) -> SessionResponse:
    trimmed = message.strip()
    if not trimmed:
        return respond(state, [format_bot_message("Say something or tap one of the options.")], _current_options(state))

    if trimmed.lower() in {"reset", "start over"}:
        return reset_session(state)

    state.history.append(("user", trimmed))

    if state.stage == "ask_name":
        state.visitor_name = trimmed.title()
        state.stage = "menu_primary"
        responses = [
            format_bot_message(f"Nice to meet you, {state.visitor_name}! Choose what you’d like to explore:"),
        ]
        return respond(state, responses, PRIMARY_OPTIONS)

    if state.stage == "menu_primary":
        match = match_option(trimmed, PRIMARY_OPTIONS)
        if not match:
            return respond(
                state,
                [format_bot_message("Pick one of the quick options so I can guide you." )],
                PRIMARY_OPTIONS,
            )
        state.primary_choice = match
        state.stage = "menu_secondary"
        options = SECONDARY_OPTIONS[match]
        responses = [
            format_bot_message(f"Great! Let’s drill into {match}. Pick a specific topic:"),
        ]
        return respond(state, responses, options)

    if state.stage == "menu_secondary":
        primary = state.primary_choice
        options = SECONDARY_OPTIONS.get(primary, [])
        match = match_option(trimmed, options)
        if not match:
            return respond(
                state,
                [format_bot_message("Choose one of the follow-up options so I can share the right highlights.")],
                options,
            )
        state.stage = "menu_primary"
        state.primary_choice = None
        info = INFO_MAP.get(match)
        if not info:
            return respond(state, [format_bot_message("I don’t have that snippet yet—try another option.")], PRIMARY_OPTIONS)
        responses = [
            format_bot_message(info),
            format_bot_message("Anything else you'd like to explore?"),
        ]
        return respond(state, responses, PRIMARY_OPTIONS)

    return respond(state, [format_bot_message("Let’s start fresh—tap ‘Start over’.")], PRIMARY_OPTIONS)


def _current_options(state: SessionState) -> List[str]:
    if state.stage == "menu_primary":
        return PRIMARY_OPTIONS
    if state.stage == "menu_secondary" and state.primary_choice:
        return SECONDARY_OPTIONS.get(state.primary_choice, [])
    return []


app = FastAPI(title="Female Foundry Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/session", response_model=SessionResponse)
def start_session() -> SessionResponse:
    state = create_session()
    return state.to_initial_response()


@app.post("/api/session/{session_id}/reset", response_model=SessionResponse)
def reset(session_id: str) -> SessionResponse:
    state = get_session(session_id)
    return reset_session(state)


@app.post("/api/chat", response_model=SessionResponse)
def chat(request: ChatRequest) -> SessionResponse:
    state = get_session(request.session_id)
    return handle_message(state, request.message)


# Serve the static front-end (index.html, JS, CSS)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
