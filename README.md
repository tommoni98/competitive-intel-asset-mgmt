# 📊 Competitive Intelligence Dashboard  
### **BlackRock vs State Street vs Invesco (2024 10-K / Annual Report Analysis)**  

This repository contains a fully self-contained **Streamlit dashboard** and analysis comparing three major global asset managers:

- **BlackRock**
- **State Street**
- **Invesco**

Using data extracted directly from their **2024 10-K filings and annual reports**, the project provides a full competitive intelligence assessment across scale, product mix, technology advantage, fees, strategy, and risk exposure.

The dashboard is designed for strategic insight, BI portfolios, and demonstration of data storytelling and dashboard engineering skills.

---

## 🚀 Features

### **📌 1. Overview & AUM Scale**
Compare the firms across:
- Total AUM  
- ETF AUM  
- Alternatives AUM  
- ETF share of total assets

### **📌 2. Product Mix Explorer**
Breakdown of:
- Equity  
- Fixed income  
- Multi-asset  
- Money market / cash  
- Alternatives  
- ETF platform strengths  
- Flagship products

### **📌 3. Technology Positioning (Tech vs Fee Map)**
Visual comparison of:
- Fee level  
- Technology strength  
- Platform differentiation (Aladdin vs Alpha vs Invesco)

### **📌 4. SWOT Viewer**
Dynamic SWOT analysis for each firm:
- Strengths  
- Weaknesses  
- Opportunities  
- Threats  

### **📌 5. Narrative Insights**
High-level, executive-style insights derived from your 20+ page competitive intelligence report.

---

## 🧠 Data Sources

All data is extracted manually from the following official documents:

- **BlackRock 2024 Form 10-K**  
- **State Street 2024 Form 10-K**  
- **Invesco 2024 Form 10-K**

No external data files are required to run the dashboard.

---

## 🗂 Repository Structure

```
├── dashboard/
│   └── app.py               # Streamlit app (self-contained)
│
├── requirements.txt         # Python dependencies
│
└── README.md                # Project documentation (this file)
```

---

## ▶️ How to Run the Dashboard

### **1. Install dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run Streamlit**
```bash
cd dashboard
streamlit run app.py
```

### **3. Open in browser**
Streamlit will open automatically at:

```
http://localhost:8501
```

---

## 📘 Project Purpose

This project was created as part of a **full competitive intelligence and market research analysis**, culminating in:

- A written research report  
- Executive summary  
- Comparative charts & financial models  
- This interactive dashboard  

It demonstrates skills in:

- Competitive intelligence  
- Financial analysis  
- Data modeling  
- Dashboard development  
- Data storytelling  
- Python (Streamlit, pandas, plotly)  
- Research using SEC filings  

---

## 🧩 Key Insights From the Analysis

### **BlackRock**
- Unmatched global scale (> $11.5T AUM)  
- Dual dominance in active + passive  
- Aladdin is a major technology moat  
- Aggressive expansion into private markets  

### **State Street**
- Leading institutional servicer with huge AUC/A ($46T+)  
- Alpha platform is a sticky front-to-back institutional solution  
- Revenue model tied to servicing fees & NII  
- Highly sensitive to interest rate environment  

### **Invesco**
- Strong independent global manager  
- QQQ franchise provides ETF leadership  
- Less scale → higher pressure from fees  
- Focused on efficiency & distribution optimization  

---

## 🤝 Contributions

Pull requests are welcome for:
- New charts or models  
- Adding more competitors (e.g., Fidelity, Vanguard)  
- Deploying dashboard to Streamlit Cloud  

---


