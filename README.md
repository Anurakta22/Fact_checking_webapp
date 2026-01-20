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

1️⃣ PDF Upload

The user uploads a PDF document through the web interface.
This document typically contains mixed content such as narrative text, opinions, and factual statements.

At this stage:
- No assumptions are made about correctness
- The document is treated as raw, unverified input


2️⃣ Text Extraction

The uploaded PDF is parsed page by page using a PDF parsing library.

- Raw text is extracted from each page
- Layout artifacts such as line breaks and inconsistent spacing are normalized
- Non-textual content (images, formatting) is ignored

The output of this step is a clean, continuous text representation of the document that can be processed by downstream models.


3️⃣ Claim Extraction (LLM-Based)

The extracted text is passed to a Large Language Model with a strictly constrained prompt that instructs the model to:

- Identify only factual, verifiable claims

- Ignore opinions, predictions, and vague statements

- Focus on claims that include:

  - Numbers or statistics

  - Dates or time references

  - Prices or percentages

- Named events with clear temporal context

The LLM outputs a structured JSON list of claims, each annotated with:

The claim text

A category (e.g., economic, technological, political)

A time reference (if applicable)

This step converts unstructured text into machine-verifiable units.

4️⃣ Live Web Search (Tavily)

Each extracted claim is independently queried against the live web using a search API.

For each claim:

- Relevant, up-to-date sources are retrieved

- Source snippets and URLs are collected

- Only recent and authoritative information is considered

This step ensures that verification is based on current, real-world data, not static or outdated knowledge.

5️⃣ LLM-Based Verification

The original claim and the retrieved web evidence are passed back to the LLM for verification.

The model is instructed to:

- Compare the claim strictly against the provided sources

Avoid speculation or unsupported reasoning

Classify the claim into one of three categories:

Verified — fully supported by evidence

Inaccurate — partially correct or outdated

False — contradicted or unsupported

The model also produces:

A concise explanation of the verdict

Corrected information where applicable

This step acts as a reasoning layer, not a source of truth.

6️⃣ Verdict + Sources

The final output for each claim includes:

A clear verdict (Verified / Inaccurate / False)

An explanation grounded in evidence

Links to the original sources used for verification

Results are:

Displayed in a clean, user-friendly UI

Color-coded for quick scanning

Exportable as a structured JSON report

This makes the system suitable for editorial review, compliance checks, or pre-publication validation.
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
