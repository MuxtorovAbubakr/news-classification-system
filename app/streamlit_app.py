import streamlit as st
import requests


# -------------------------
# Page configuration
# -------------------------

st.set_page_config(
    page_title="News Classifier",
    page_icon=None,
    layout="centered"
)


# -------------------------
# Session state
# -------------------------

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "error" not in st.session_state:
    st.session_state.error = None


def clear_app():
    st.session_state.article_input = ""
    st.session_state.prediction = None
    st.session_state.error = None


# -------------------------
# Custom CSS
# -------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #151b35 50%,
        #1e1b4b 100%
    );
    color: #f8fafc;
}

/* Main content width */
.block-container {
    max-width: 850px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* Main heading */
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #ffffff;
    letter-spacing: -1.5px;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #a5b4fc;
    font-size: 16px;
    margin-bottom: 35px;
}

/* Section labels */
.section-label {
    color: #cbd5e1;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* Text area */
.stTextArea textarea {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    border-radius: 12px !important;
    font-size: 15px !important;
}

.stTextArea textarea::placeholder {
    color: #cbd5e1 !important;
    opacity: 1 !important;
}

.stTextArea textarea:focus {
    border: 1px solid #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 45px;
    transition: all 0.2s ease;
}

/* Primary button */
.stButton button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
}

.stButton button[kind="primary"]:hover {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    transform: translateY(-2px);
}

/* Secondary button */
.stButton button[kind="secondary"] {
    background: #334155;
    color: #e2e8f0;
    border: 1px solid #475569;
}

/* Prediction card */
.prediction-card {
    background: linear-gradient(
        135deg,
        rgba(99, 102, 241, 0.18),
        rgba(139, 92, 246, 0.12)
    );
    border: 1px solid rgba(129, 140, 248, 0.4);
    border-radius: 16px;
    padding: 25px;
    text-align: center;
    margin-top: 25px;
}

/* Prediction label */
.prediction-label {
    color: #a5b4fc;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* Category result */
.prediction-category {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# Header
# -------------------------

st.markdown(
    '<div class="main-title">News Classifier</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An AI-powered system for classifying news articles.'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------
# Article input
# -------------------------

st.markdown(
    '<div class="section-label">Enter your news article</div>',
    unsafe_allow_html=True
)

article = st.text_area(
    "Article",
    height=250,
    placeholder="Paste your news article here...",
    label_visibility="collapsed",
    key="article_input"
)


# -------------------------
# Action buttons
# -------------------------

col1, col2 = st.columns([3, 1])

with col1:
    classify_clicked = st.button(
        "Classify Article",
        type="primary",
        use_container_width=True
    )

with col2:
    st.button(
        "Clear",
        type="secondary",
        use_container_width=True,
        on_click=clear_app
    )


# -------------------------
# Prediction
# -------------------------

if classify_clicked:

    st.session_state.prediction = None
    st.session_state.error = None

    if not article.strip():
        st.session_state.error = "Please enter a news article."

    else:
        try:
            with st.spinner("Analyzing article..."):

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json={"text": article},
                    timeout=30
                )

                response.raise_for_status()

                result = response.json()

                st.session_state.prediction = result["category"]

        except requests.exceptions.ConnectionError:
            st.session_state.error = (
                "Could not connect to the API. "
                "Make sure the FastAPI server is running."
            )

        except requests.exceptions.Timeout:
            st.session_state.error = (
                "The request timed out. Please try again."
            )

        except requests.exceptions.RequestException as error:
            st.session_state.error = (
                f"API request failed: {error}"
            )

        except (KeyError, ValueError):
            st.session_state.error = (
                "The API returned an unexpected response."
            )


# -------------------------
# Display result
# -------------------------

if st.session_state.error:
    st.error(st.session_state.error)


if st.session_state.prediction:

    st.markdown(
        f"""
        <div class="prediction-card">
            <div class="prediction-label">
                Predicted Category
            </div>
            <div class="prediction-category">
                {st.session_state.prediction}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# Footer
# -------------------------
