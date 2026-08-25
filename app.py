import streamlit as st
from main import generate_flashcard_text, parse_notes

st.set_page_config(
    page_title="AI Flashcard Generator",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS for crisp full-screen layout and 3D card flipping
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    .flashcard-container {
        perspective: 1000px;
        margin: 20px auto;
        cursor: pointer;
    }
    .flashcard {
        width: 100%;
        min-height: 250px;
        background-color: #1E1E2E;
        border: 2px solid #89B4FA;
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.2s ease-in-out;
    }
    .flashcard:hover {
        transform: scale(1.02);
    }
    .card-label {
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #89B4FA;
        margin-bottom: 12px;
        font-weight: 600;
    }
    .card-content {
        font-size: 22px;
        font-weight: bold;
        color: #CDD6F4;
    }
    .click-hint {
        font-size: 12px;
        color: #A6ADC8;
        margin-top: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🎴 AI Flashcard Generator")

# Notes Input
raw_note = st.text_area(
    "Paste your notes:",
    height=180,
    placeholder="Paste a paragraph or notes here. The AI will automatically split key concepts into individual flashcards...",
)

# Initialize Session States for Navigation and Flip State
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
if "flipped" not in st.session_state:
    st.session_state.flipped = False

if st.button("Generate Flashcards", type="primary", use_container_width=True):
    if not raw_note.strip():
        st.warning("Please paste some notes first!")
    else:
        with st.spinner("Analyzing text and creating flashcards..."):
            try:
                ai_output = generate_flashcard_text(raw_note)
                cards = parse_notes(ai_output)

                if cards:
                    st.session_state.flashcards = cards
                    st.session_state.card_index = 0
                    st.session_state.flipped = False
                    st.rerun()
                else:
                    st.error("Could not extract flashcards. Try providing clearer notes.")
            except Exception as e:
                st.error(f"Error: {e}")

# Interactive Flashcard Viewer
if st.session_state.flashcards:
    st.divider()

    total_cards = len(st.session_state.flashcards)
    current_card = st.session_state.flashcards[st.session_state.card_index]

    # Flip Toggle Function
    def flip_card():
        st.session_state.flipped = not st.session_state.flipped

    # Render Active Card
    side_label = "BACK (Definition)" if st.session_state.flipped else "FRONT (Term)"
    side_text = current_card["back"] if st.session_state.flipped else current_card["front"]

    st.button(
        f"🔄 Flip Card — Showing {side_label}",
        on_click=flip_card,
        use_container_width=True,
    )

    st.markdown(
        f"""
        <div class="flashcard-container">
            <div class="flashcard">
                <div class="card-label">{side_label}</div>
                <div class="card-content">{side_text}</div>
                <div class="click-hint">(Click button above to flip)</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Navigation Controls
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            if st.session_state.card_index > 0:
                st.session_state.card_index -= 1
                st.session_state.flipped = False
                st.rerun()

    with col2:
        st.markdown(
            f"<h4 style='text-align: center; color: #CDD6F4;'>Card {st.session_state.card_index + 1} of {total_cards}</h4>",
            unsafe_allow_html=True,
        )

    with col3:
        if st.button("Next ➡️", use_container_width=True):
            if st.session_state.card_index < total_cards - 1:
                st.session_state.card_index += 1
                st.session_state.flipped = False
                st.rerun()