# 🔍 Google Photos Feedback Discovery Engine

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](http://localhost:8501)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Fluent 2 UI](https://img.shields.io/badge/Fluent_2-0078D4?style=for-the-badge&logo=microsoft&logoColor=white)](https://fluent2.microsoft.design)

An AI-powered Product Management discovery engine and interactive analytics dashboard that analyzes authentic user feedback to understand why users struggle with photo retrieval in Google Photos.

---

## 🌟 Key Highlights

- **7,358 Raw Feedback Items Ingested**: Collected across 6 public channels (Apple App Store, Google Play Store, Google Help Community, Reddit, YouTube, and X).
- **7,167 Cleaned & Normalised**: Spam and duplicates removed.
- **510 Verified Search Retrieval Reviews**: 100% authentic human feedback (0% synthetic data).
- **Interactive Multi-Tab Dashboard**: Built with modern Fluent 2 design principles, supporting dark/light mode toggles and dynamic visualization.
- **Streamlit Deployment Ready**: Includes one-click `app.py` integration for Streamlit Cloud and local hosting.

---

## 📊 Dashboard Tabs & Features

### 1. 📊 Overview
- **Dataset & Ingestion Funnel**: Clear KPI breakdown of raw, normalized, and verified retrieval reviews.
- **Search Retrieval Resolution**: % of reviews indicating successful vs. failed retrieval.
- **Failure Stages Funnel**: Visualizing critical friction points in the user search journey.
- **Key Takeaway**: Executive summary banner synthesizing core findings.

### 2. 🧩 Problem Clusters
- Detailed breakdown of emergent problem clusters:
  1. **People identification failure**
  2. **Mismatch between user query and search response**
  3. **Failures in date & time based search**
  4. **Users drown in results, struggle to narrow down**
  5. **Failure in object & visual attribute based photo search**
  6. **Failures in text, document, screenshot search**

### 3. 💡 Discovery Qs
- **Exploring User Struggles in Photo Retrieval**: Core Product Management research questions answering what photos users look for, what contextual clues they remember (people, places, dates, activities), when they abandon search, and how failure impacts user confidence.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/prakhardubey23/AI-Powered-Discovery-Engine-Google-Photos-Reviews.git
cd AI-Powered-Discovery-Engine-Google-Photos-Reviews
```

### 2. Set Up Environment & Secrets
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your-gemini-api-key"
GROQ_API_KEY_1="your-groq-api-key-1"
GROQ_API_KEY_2="your-groq-api-key-2"
PORT=8000
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application

#### Option A: Run via Streamlit (Recommended)
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

#### Option B: Run via Lightweight Static HTTP Server
```bash
python -m http.server 8000 --directory web
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## 📁 Project Structure

```
├── app.py                      # Main Streamlit application runner
├── streamlit_app.py            # Streamlit Cloud deployment entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration & API keys (GitIgnored)
├── .gitignore                  # Git exclusion rules
│
├── web/                        # Web Dashboard Frontend
│   ├── index.html              # Core HTML structure
│   ├── index.css              # Fluent 2 design system styles
│   ├── app.js                  # Dynamic dashboard rendering & tab navigation
│   ├── data.js                 # Compiled dataset metrics & clusters
│   └── favicon.svg             # Official Google 4-color icon
│
├── src/                        # Data Pipeline & Analysis Scripts
│   ├── cleaning/               # Text normalization & deduplication
│   ├── classification/         # Relevance filtering
│   ├── extraction/             # Cognitive clue & tri-state memory extraction
│   ├── clustering/             # Emergent problem clustering
│   ├── quantification/         # Metrics calculation
│   └── utils/                  # LLM clients & API helpers
│
└── data/                       # Structured JSON Datasets
    ├── 01_raw/                 # Ingested raw feedback
    ├── 02_normalized/          # Cleaned dataset
    ├── 03_filtered/            # Relevant retrieval reviews
    └── 05_clustering/          # Categorized problem clusters
```

---

## 🌐 Deploying to Streamlit Cloud

1. Fork or push this repository to your GitHub account.
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and click **New App**.
3. Select your repository and set `streamlit_app.py` as the Main File Path.
4. Under **Advanced Settings > Secrets**, add your API keys:
   ```toml
   GEMINI_API_KEY = "your-key"
   GROQ_API_KEY_1 = "your-key"
   ```
5. Click **Deploy**!

---

## 🛡️ License & Research Integrity

All feedback dataset items are derived strictly from authentic public user reviews. Synthetic data is 0% used to maintain strict qualitative research integrity.
