# 🧾 Fact-Checking Web App

A deployed web application that automatically extracts factual claims from a PDF document and verifies them against **live web data** before publication.

This tool acts as a **fact-checking layer** between content drafts and the final publish step.

---

## 🚀 Live Demo

- **Deployed App:** https://<your-streamlit-app-url>
- **Demo Video:** https://<your-demo-video-link>

---

## 🧠 What This App Does

Given a PDF document, the app performs three core steps:

### 1. Claim Extraction
- Extracts **only factual, verifiable claims**
- Ignores opinions and vague language
- Focuses on:
  - Numbers & statistics
  - Dates & timelines
  - Prices & percentages
  - Named events with time references

### 2. Live Verification
- Searches the **live web** using Tavily Search
- Grounds claims in real-time sources
- Uses a Large Language Model (Gemini) to reason over evidence

### 3. Fact-Check Report
Each claim is labeled as:
- ✅ **Verified** — matches current data
- ⚠️ **Inaccurate** — partially correct or outdated
- ❌ **False** — contradicted or unsupported

Each result includes:
- A short explanation
- Corrected information (if applicable)
- Source URLs

---

## 🖥️ User Interface

- Drag-and-drop PDF upload
- One-click fact checking
- Clean, dark-mode-friendly UI
- Color-coded verdict cards
- Downloadable JSON report

> ℹ️ *Free-tier mode intentionally limits the number of claims verified per run to ensure stability.*

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **PDF Parsing:** PyPDF  
- **LLM:** Google Gemini (Gemini 2.5 Flash)  
- **Web Search:** Tavily Search API  
- **Language:** Python  

---

## ⚙️ How It Works (Pipeline)

PDF Upload
↓
Text Extraction
↓
Claim Extraction (LLM)
↓
Live Web Search (Tavily)
↓
LLM-based Verification
↓
Verdict + Sources


---

## 🧪 Reliability & Error Handling

- Gracefully handles API rate limits and quota exhaustion
- Caches extraction results to reduce repeated LLM calls
- Avoids crashes when APIs are temporarily unavailable
- Clearly communicates free-tier constraints to users

---

## 📦 Installation (Local)

```bash
pip install -r requirements.txt
streamlit run app.py