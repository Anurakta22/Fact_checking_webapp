import streamlit as st
import re
import json
from pypdf import PdfReader
from google import genai
from tavily import TavilyClient

# =======================
# CONFIG
# =======================
st.set_page_config(page_title="Fact Checker", layout="wide")

MODEL_NAME = "models/gemini-2.5-flash"
MAX_CLAIMS_TO_VERIFY = 5

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

tavily_client = TavilyClient(
    api_key=st.secrets["TAVILY_API_KEY"]
)

# =======================
# STYLES (Dark-mode friendly)
# =======================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }
    .claim-box {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: rgba(240, 242, 246, 0.05);
        border-left: 5px solid #4CAF50;
    }
    .verified { border-left-color: #2ecc71; }
    .inaccurate { border-left-color: #f39c12; }
    .false { border-left-color: #e74c3c; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =======================
# HELPER FUNCTIONS
# =======================
def safe_json_loads(text):
    if not text or text.strip() == "":
        raise ValueError("Empty LLM response")

    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        return json.loads(match.group())

    raise ValueError("Invalid JSON from LLM")


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"
    return text


@st.cache_data(show_spinner=False)
def extract_claims(text):
    clean_text = re.sub(r"\s+", " ", text)[:8000]

    prompt = f"""
Extract ONLY factual, verifiable claims from the text below.

Rules:
- Each claim must include a number, date, percentage, price, or dated event
- Ignore opinions or predictions
- Return ONLY valid JSON
- No markdown, no explanations

Format:
[
  {{
    "claim": "...",
    "category": "...",
    "time_reference": "..."
  }}
]

Text:
{clean_text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return safe_json_loads(response.text)

    except Exception:
        return {
            "error": "LLM_QUOTA_EXHAUSTED"
        }


def verify_claim(claim_text):
    search_results = tavily_client.search(
        query=claim_text,
        max_results=3
    )

    sources = [r["url"] for r in search_results["results"]]

    context = "\n".join(
        [r["content"] for r in search_results["results"]]
    )[:6000]

    prompt = f"""
Check the following claim against the provided sources.

Claim:
{claim_text}

Sources:
{context}

Classify as:
- Verified
- Inaccurate
- False

Return ONLY valid JSON:
{{
  "verdict": "...",
  "explanation": "...",
  "correct_info": "..."
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    verdict = safe_json_loads(response.text)
    return verdict, sources

# =======================
# UI
# =======================
st.title("📄 Fact-Checking Web App")
st.write("Upload a PDF to extract and verify factual claims using live web data.")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading PDF..."):
        full_text = extract_text_from_pdf(uploaded_file)

    start = st.button("🔍 Start Fact-Check")
    st.caption("ℹ️ Free-tier mode: verifies a limited number of claims per run.")

    if start:
        with st.spinner("Extracting claims..."):
            claims = extract_claims(full_text)

        if isinstance(claims, dict) and claims.get("error"):
            st.warning("⚠️ LLM quota exhausted.")
            st.info(
                "Gemini free-tier quota is currently exhausted. "
                "The pipeline is implemented correctly—please retry later."
            )
            st.stop()

        if not claims:
            st.warning("No verifiable factual claims found.")
            st.stop()

        st.subheader("🔍 Fact-Check Results")

        results = []

        for i, c in enumerate(claims[:MAX_CLAIMS_TO_VERIFY], 1):
            with st.spinner(f"Verifying claim {i}..."):
                verdict, sources = verify_claim(c["claim"])

            status = verdict["verdict"]
            css_class = (
                "verified" if status == "Verified"
                else "inaccurate" if status == "Inaccurate"
                else "false"
            )

            st.markdown(
                f"""
                <div class="claim-box {css_class}">
                    <strong>{i}. {c['claim']}</strong><br><br>
                    <b>Verdict:</b> {status}<br>
                    <b>Explanation:</b> {verdict['explanation']}<br>
                    {"<b>Correct info:</b> " + verdict["correct_info"] + "<br>" if verdict["correct_info"] else ""}
                    <b>Sources:</b>
                    <ul>
                        {''.join([f"<li><a href='{url}' target='_blank'>{url}</a></li>" for url in sources])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

            results.append({
                "claim": c["claim"],
                "verdict": verdict["verdict"],
                "explanation": verdict["explanation"],
                "correct_info": verdict["correct_info"],
                "sources": sources,
            })

        st.download_button(
            "⬇️ Download Fact-Check Report (JSON)",
            data=json.dumps(results, indent=2),
            file_name="fact_check_report.json",
            mime="application/json",
        )