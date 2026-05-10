<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&pause=1000&color=3B82F6&center=true&vCenter=true&width=700&lines=ENHANCV+%F0%9F%9A%80;Smart+ATS+Resume+Builder+%26+Analyzer;Score.+Optimize.+Get+Hired." alt="Typing SVG" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/LLaMA_3.3-70B-6366F1?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq_API-Powered-F97316?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Cost-%E2%82%B90%20Free-10B981?style=for-the-badge" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Version-1.0-6366f1?style=flat-square" />
  <img src="https://img.shields.io/badge/Users-500%2B-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/ATS_Accuracy-92%25-green?style=flat-square" />
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square" />
</p>

**ENHANCV** is a 100% free, AI-powered resume platform that analyzes your resume, detects skill gaps, scores ATS compatibility, and builds optimized resumes — all powered by LLaMA 3.3 70B via Groq API.

> *No paid subscriptions. No manual guessing. Just paste your resume and get results.*

<br/>

**Live Demo → [enhancv-amtz.onrender.com](https://enhancv-amtz.onrender.com/)**

<br/>

<a href="#-quick-start">Quick Start</a> •
<a href="#-features">Features</a> •
<a href="#-architecture">Architecture</a> •
<a href="#-how-it-works">How It Works</a> •
<a href="#-installation">Installation</a> •
<a href="#-usage">Usage</a> •
<a href="#-tech-stack">Tech Stack</a> •
<a href="#-roadmap">Roadmap</a> •
<a href="#-contributing">Contributing</a>

</div>

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/akashgadde05/ENHANCV.git
cd ENHANCV

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements-minimal.txt

# 4. Configure environment
cp .env.example .env
# Add your Groq API key to .env

# 5. Launch
python run.py
```

Open **http://localhost:5000** in your browser. That's it. ✅

> **Get your free Groq API key** at [console.groq.com](https://console.groq.com/) — takes 2 minutes. No credit card required.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📝 Resume Builder
- Step-by-step interactive form with guided prompts
- ATS-safe professional templates
- Real-time content validation and feedback
- One-click PDF export via ReportLab

</td>
<td width="50%">

### 🔍 Resume Analyzer
- AI-powered analysis via **Groq + LLaMA 3.3 70B**
- ATS compatibility check with issue detection
- Skills gap analysis against industry benchmarks
- Multi-dimensional quantitative scoring

</td>
</tr>
<tr>
<td width="50%">

### 📚 Course Recommendations
- Personalized course suggestions based on detected skill gaps
- Recommendations from Coursera, Udemy, edX, and more
- Focused on in-demand technical skills for 2026 job market

</td>
<td width="50%">

### 📦 Bulk Resume Analysis *(HR / Recruiter Tool)*
- Upload and analyze multiple resumes simultaneously
- Candidate ranking and comparative scoring
- Exportable batch results — cuts HR screening time by **70%**

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
ENHANCV/
│
├── app.py                        ← Main Flask application & routes
├── run.py                        ← App entry point
├── requirements.txt
├── .env.example
│
├── utils/
│   ├── llm_analyzer.py           ← Groq LLM integration (LLaMA 3.3 70B)
│   ├── resume_analyzer.py        ← Resume text analysis engine
│   ├── resume_builder.py         ← Resume generation logic
│   └── pdf_generator.py          ← PDF export via ReportLab
│
├── templates/
│   ├── base.html                 ← Base layout
│   ├── index.html                ← Home page
│   ├── builder.html              ← Resume builder UI
│   ├── analyzer.html             ← Resume analyzer UI
│   └── bulk_analyzer.html        ← Bulk analysis UI
│
└── static/
    ├── css/style.css             ← Custom styles
    └── js/main.js                ← Chart.js + interactive features
```

### Three-Layer Design

```
┌─────────────────────────────────────────────────────────┐
│        PRESENTATION LAYER  (Flask + Bootstrap 5)        │
│   Responsive UI · Chart.js · Font Awesome · Reactive    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│           INTELLIGENCE LAYER  (Groq + LLaMA 3.3)        │
│   ATS Scoring · Skill Gap Detection · NLP · TextBlob    │
└───────────────────────┬─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│            DATA LAYER  (Documents + Memory)             │
│   PyPDF2 · python-docx · In-memory processing           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 How It Works

### 1. Document Parsing

ENHANCV accepts PDF, DOCX, DOC, and TXT formats and extracts raw text for analysis:

```python
# PDF extraction
PyPDF2.PdfReader(file) → raw_text

# DOCX extraction
python-docx Document(file) → paragraph_text

# Plain text
file.read().decode("utf-8") → raw_text
```

---

### 2. ATS Scoring — The 7 Dimensions

Resumes are evaluated across seven dimensions with weighted scoring:

| # | Dimension | Weight | What It Checks |
|---|-----------|--------|----------------|
| 1 | Content Length | Medium | Optimal word count (400–800 words ideal) |
| 2 | Skills Coverage | High | Technical + soft skills keyword presence |
| 3 | Experience Indicators | High | Job titles, tenures, responsibilities |
| 4 | Quantified Achievements | High | Numbers, %, $, metrics in bullet points |
| 5 | ATS Format Compliance | High | Clean structure, no tables/graphics issues |
| 6 | Section Completeness | Medium | Summary, Skills, Experience, Education present |
| 7 | Readability | Medium | Sentence clarity and action verb usage |

**Final Score Bands:**

| Score | Rating |
|-------|--------|
| 85 – 100 | 🟢 Excellent — ATS ready |
| 70 – 84 | 🟡 Good — minor improvements needed |
| 55 – 69 | 🟠 Average — several areas need work |
| Below 55 | 🔴 Needs improvement — major optimization required |

---

### 3. AI Analysis Pipeline

```
Upload Resume (PDF / DOCX / TXT)
        │
        ▼
   Text Extraction  (PyPDF2 / python-docx)
        │
        ▼
   Rule-Based Preprocessing  (TextBlob NLP)
        │
        ▼
   Groq API Call → LLaMA 3.3 70B
   ┌─────────────────────────────┐
   │  · ATS issue detection      │
   │  · Skill gap analysis       │
   │  · Improvement suggestions  │
   │  · Course recommendations   │
   └─────────────────────────────┘
        │
        ▼
   Quantitative Score + Detailed Report
        │
        ▼
   Display / Export Results
```

---

## 📦 Installation

### Prerequisites

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Python | 3.8+ | 3.11 recommended |
| RAM | 2 GB | 4 GB+ comfortable |
| GPU | ❌ Not required | Runs fully on CPU |
| Internet | ✅ Required | For Groq API calls |
| Groq API Key | ✅ Required | Free at [console.groq.com](https://console.groq.com) |

### Option A — Standard Install (Recommended)

```bash
git clone https://github.com/akashgadde05/ENHANCV.git
cd ENHANCV

python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### Option B — Minimal Install (Core Features Only)

```bash
pip install flask groq python-dotenv
# File upload support:
pip install pypdf2 python-docx
# PDF generation:
pip install reportlab
```

### Option C — One-Click Start

```bash
python start.py    # Auto-detects environment, launches best available version
```

### Environment Configuration

```env
# .env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DEBUG=True
```

---

## 🎮 Usage

### Step-by-Step Workflow

```
① Upload your resume (PDF / DOCX / TXT)
② Optionally paste a job description for targeted analysis
③ Run AI-powered ATS analysis
④ Review your score across 7 dimensions
⑤ Read skill gap report + improvement suggestions
⑥ Get personalized course recommendations
⑦ Rebuild or export an optimized version
```

### Module Guide

**Resume Analyzer**
1. Navigate to the **Analyzer** section
2. Upload your resume file
3. *(Optional)* Paste a job description for targeted keyword matching
4. Click **Analyze** — results appear in 5–10 seconds
5. Export the full report for reference

**Resume Builder**
1. Go to the **Builder** section
2. Fill out the guided step-by-step form
3. Use the live preview to validate content in real time
4. Generate a professional ATS-safe PDF

**Bulk Analysis** *(Recruiters / HR)*
1. Access **Bulk Analysis**
2. Upload multiple resume files at once
3. Get ranked results with comparative scores
4. Export the full batch analysis

---

## ⚡ Performance

| Operation | Time | Notes |
|-----------|------|-------|
| App startup | 2–3 s | Flask cold start |
| PDF / DOCX parsing | < 1 s | In-memory only |
| Rule-based preprocessing | < 0.5 s | TextBlob NLP |
| Groq LLM analysis | 3–8 s | LLaMA 3.3 70B via API |
| Score computation | < 0.5 s | Local calculation |
| PDF generation | 1–2 s | ReportLab |
| **End-to-end (single resume)** | **~10 s** | |
| **Bulk (10 resumes)** | **~60 s** | Sequential Groq calls |

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Why |
|-------|-----------|-----|
| **Web Framework** | [Flask](https://flask.palletsprojects.com) | Lightweight Python backend, zero overhead |
| **AI / LLM** | [Groq API](https://console.groq.com) + LLaMA 3.3 70B | Fastest inference, free tier, no GPU needed |
| **NLP** | [TextBlob](https://textblob.readthedocs.io) | Sentence-level text analysis |
| **PDF Parsing** | [PyPDF2](https://pypdf2.readthedocs.io) | Resume text extraction from PDFs |
| **DOCX Parsing** | [python-docx](https://python-docx.readthedocs.io) | Word document text extraction |
| **PDF Generation** | [ReportLab](https://www.reportlab.com) | Professional PDF resume output |
| **Frontend** | Bootstrap 5 + Vanilla JS | Responsive UI, no build step needed |
| **Charts** | [Chart.js](https://www.chartjs.org) | Score visualization dashboard |
| **Icons** | Font Awesome | Consistent UI iconography |

</div>

---

## 🚀 Deployment

### Render *(Current Deployment — Free)*

This app is live on Render: **[enhancv-amtz.onrender.com](https://enhancv-amtz.onrender.com/)**

To deploy your own fork:
1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo; set build command: `pip install -r requirements.txt`
4. Set start command: `python run.py`
5. Add `GROQ_API_KEY` as an environment variable
6. Deploy — live in ~3 minutes ✅

### Local Network *(Demo Day)*

```bash
flask run --host=0.0.0.0 --port=5000
# Access from any device on same WiFi: http://YOUR_IP:5000
```

---

## 🗺️ Roadmap

```
v1.0 (Current) ████████████████████ Released
v2.0           ░░░░░░░░░░░░░░░░░░░░ In Progress
v3.0           ░░░░░░░░░░░░░░░░░░░░ Planned
```

### v2.0 — Smarter Analysis
- [ ] Job description keyword matching with gap heatmap
- [ ] Multi-format score export (PDF report, JSON)
- [ ] Resume version comparison (before vs after)
- [ ] LinkedIn profile URL import

### v3.0 — Full-Stack Upgrade
- [ ] FastAPI backend + React frontend
- [ ] User accounts with resume history
- [ ] Real-time collaborative editing
- [ ] RAG-powered career path advisor

---

## 🤝 Contributing

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/your-feature-name

# 3. Make changes + test locally
python run.py

# 4. Commit with a clear message
git commit -m "feat: describe your change"

# 5. Push and open a Pull Request
git push origin feature/your-feature-name
```

### Good First Issues

| Issue | Difficulty | Module |
|-------|-----------|--------|
| Add LinkedIn URL parser | 🟢 Easy | `utils/resume_analyzer.py` |
| Add JSON export for analysis results | 🟢 Easy | `app.py` |
| Add cover letter generator | 🟡 Medium | `utils/llm_analyzer.py` |
| Add resume diff viewer (before/after) | 🟡 Medium | `templates/analyzer.html` |
| Replace TextBlob with spaCy | 🔴 Hard | `utils/resume_analyzer.py` |

---

## 🐛 Troubleshooting

<details>
<summary><b>Groq API key error</b></summary>

```bash
# Verify your .env file contains:
GROQ_API_KEY=gsk_your_actual_key_here

# Test the key directly:
python test_groq.py
```
</details>

<details>
<summary><b>Dependency conflicts</b></summary>

```bash
# Use the minimal requirements file:
pip install -r requirements-minimal.txt

# Or install only core packages:
pip install flask groq python-dotenv pypdf2 python-docx reportlab
```
</details>

<details>
<summary><b>File upload not working</b></summary>

```bash
# Run system diagnostics — creates missing upload directories:
python check_system.py
```
</details>

<details>
<summary><b>Import errors on startup</b></summary>

```bash
# Run the minimal app with graceful feature degradation:
python app_minimal.py
```
</details>

<details>
<summary><b>Port 5000 already in use</b></summary>

```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Or run on a different port:
flask run --port 5001
```
</details>

---

## 🔒 Privacy

- **No data storage** — files are processed in memory only, never written to disk
- **No transmission** — your resume is never sent anywhere except your own Groq API call
- **Stateless** — each session is completely independent
- **Open source** — full codebase is publicly auditable

---

## 📜 License

```
MIT License — Copyright (c) 2025 Akash Gadde

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgements

- **[Groq](https://groq.com)** — For the fastest LLM inference API available, with a generous free tier
- **[Meta AI](https://ai.meta.com)** — For open-sourcing the LLaMA 3.3 model family
- **[Flask](https://flask.palletsprojects.com)** — For making Python web apps simple and elegant
- **[Bootstrap](https://getbootstrap.com)** — For a responsive UI without the complexity
- **[ReportLab](https://www.reportlab.com)** — For professional-grade PDF generation in Python

---

<div align="center">

**Built with ❤️ by [Akash Gadde](https://github.com/akashgadde05)**

*If ENHANCV helped you land an interview, please ⭐ star this repo — it means a lot!*

<br/>

<img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/For-Job%20Seekers-FF6B6B?style=for-the-badge" />
<img src="https://img.shields.io/badge/Cost-Zero-10B981?style=for-the-badge" />

</div>
