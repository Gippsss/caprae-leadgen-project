# 🚀 Caprae LeadGen Project

A lead generation and enrichment tool that extracts, scores, and analyzes potential leads from company domains. Built in Python with Streamlit for a **user-friendly web interface**.

[**Live Demo on Streamlit Cloud**](https://gippsss-caprae-leadgen-project-app-onnuig.streamlit.app/)  

---

## 📝 Project Overview

Caprae LeadGen helps sales and marketing teams identify high-quality leads by:  
- Extracting emails from company websites  
- Identifying relevant contact pages  
- Inferring the company industry  
- Scoring leads based on actionable metrics  

This tool is designed to **save time** and **prioritize high-impact leads**, aligning closely with real business needs.

---

**## ⚡ Features**

- ✅ Upload a CSV of company domains (`website` column required)  
- ✅ Automated extraction of emails and contact links  
- ✅ Industry inference (SaaS, Marketplace, Services)  
- ✅ Lead scoring (0–100) based on real enrichment metrics  
- ✅ Parallel processing for faster performance  
- ✅ Download enriched CSV directly from the web app  
- ✅ Adjustable number of threads for optimal speed  

---

**## 📁 Folder Structure**
CAPRAE-LEADGEN-PROJECT/
│
├─ app.py # Streamlit front-end
├─ main.py # Core processing logic
├─ enrich.py # Lead enrichment functions
├─ yc_companies.csv # Example input CSV
├─ requirements.txt # Project dependencies
├─ README.md
├─ output/ # Enriched CSVs
└─ venv/ # Python virtual environment

---

## 🚀 Getting Started


### 1. **Clone the Repository**

```bash
git clone https://github.com/Gippsss/caprae-leadgen-project.git
cd caprae-leadgen-project
```

**###2. Set up the Virtual Environment**
```python -m venv venv ```
# Windows
```venv\Scripts\activate```
# Mac/Linux
```source venv/bin/activate```

**###3. Install Dependencies**
```pip install -r requirements.txt```

**###4. Run Locally**
```streamlit run app.py```

Open the URL provided in the terminal (usually http://localhost:8501) to use the app.

#**📄 Usage Instructions**
Upload a CSV file containing a website column with company domains.
Preview your input data in the Streamlit app.
Set the number of parallel threads for faster processing (default = 10).
Click "Run Lead Generation Tool" to start enrichment.
View the enriched results and download the CSV.

---

#**🔧 Technology Stack**
Python 3.10+
Streamlit (Web interface)
Pandas (Data handling)
Requests & BeautifulSoup4 (Web scraping)
Concurrent Futures (Parallel processing)

---

#**⚡ Notes & Recommendations**
Ensure your input CSV column is named website exactly.
Large CSVs with many domains may take several minutes; increase Max parallel threads for faster results.
All processing is performed in-memory; no temporary files are required.

---

#**⚙️ Performance & Scalability Notes**

The tool is optimized for processing thousands of domains efficiently using parallel threading. Actual runtime depends on your system and network bandwidth.

*⏱️ Typical Runtime Estimates*
Dataset Size	Threads	Avg Timeout	Approx Runtime
500 domains	10	30s	~5–7 minutes
2,000 domains	15	25s	~20–25 minutes
5,000 domains	25	30s	~45–60 minutes
(These are based on a mid-range laptop with 8 GB RAM and stable internet.)

*🚀 Tips to Improve Speed*
Increase Threads: Set Max parallel threads to 25–30 for faster execution.
(Keep it below 40 to avoid network throttling.)
Reduce Timeout: Lower Timeout per website from 30 → 15 seconds for a quicker pass (skips slow domains).
Split Large Files: Split large CSVs (e.g., 5000+ rows) into smaller chunks to make progress easier to track.
Resume Feature: The tool automatically skips already-processed domains when re-run, preventing duplicate work.

*🧠 Developer Insight*
Parallel processing uses Python’s ThreadPoolExecutor for concurrent requests, allowing simultaneous enrichment of multiple domains.
Error handling includes:
Automatic retries (up to 2 per domain)
Timeout control per request
Intermediate checkpoint saving every 100 records
This ensures even long-running jobs remain stable and recoverable if interrupted.

*🧩 Example: Optimized Settings for Different Machines*
System Specs	Recommended Threads	Timeout
4 GB RAM, Dual Core	8–10	20s
8 GB RAM, Quad Core	20	25s
16+ GB RAM, 6+ Cores	30–35	30s

---

#**📈 Future Enhancements**
Add enrichment from social media profiles (LinkedIn, Twitter)
Integrate with CRM systems for direct lead export
Implement caching for repeated domain checks to speed up processing
Add more sophisticated lead scoring based on company size, traffic, or tech stack

#**📞 Contact**
For questions or collaborations, reach out via email: [gurupreethikasayala@gmail.com]
LinkedIn profile: https://www.linkedin.com/in/guru-preethika-sayala/

---
