# 🧾 Fact-Checking Web App

A deployed web application that automatically extracts factual claims from a PDF document and verifies them against **live web data** before publication.

This tool acts as a **fact-checking layer** between content drafts and the final publish step.

---

## 🚀 Live Demo

- **Deployed App:** https://factcheckingwebapp-anuraktadash.streamlit.app/
- **Demo Video:** https://drive.google.com/file/d/1794GFezhVMr66EI6p-0cKI1z6rWuQsBW/view?usp=sharing

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

Users upload a PDF document through the web interface.
The document may contain a mix of narrative text, opinions, and factual statements.


2️⃣ Text Extraction

The application extracts raw text from the uploaded PDF:

- Processes the document page by page

- Normalizes spacing and formatting artifacts

- Produces clean, continuous text for analysis


3️⃣ Claim Extraction (LLM-Based)

The cleaned text is sent to a Large Language Model with strict instructions to extract only factual, verifiable claims.

Extracted claims must include at least one of:

- A number or statistic

- A date or time reference

- A price or percentage

- A named event with temporal context

Each claim is returned in structured JSON format, making it suitable for automated verification.

4️⃣ Live Web Search (Tavily)

Every extracted claim is queried against the live web using Tavily Search:

- Retrieves up-to-date, relevant sources

- Collects source snippets and URLs

- Ensures verification is grounded in current information

5️⃣ LLM-Based Verification

The claim and its retrieved sources are passed back to the LLM for reasoning.
The model compares the claim strictly against the evidence and classifies it as:

- Verified – fully supported by sources

- Inaccurate – partially correct or outdated

- False – unsupported or contradicted

A short explanation and corrected information (if applicable) are generated for each claim.

6️⃣ Results & Output

The final results include:

- Verdict for each claim

- Explanation of the decision

- Source URLs used for verification

Results are:

- Displayed in a clean, color-coded UI

- Easy to scan and review

- Downloadable as a structured JSON report

This makes the system suitable for editorial review, compliance checks, or pre-publication validation.
---

## 📦 Installation (Local)

```bash
pip install -r requirements.txt
streamlit run app.py
