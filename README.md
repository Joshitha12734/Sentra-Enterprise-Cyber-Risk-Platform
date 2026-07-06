# 🛡️ Sentra Enterprise Cyber Risk Platform

<div align="center">

### AI-Powered Enterprise Cyber Risk Intelligence Platform

Transforming live CVEs into business-aware cyber risk decisions using contextual asset intelligence, exposure modeling, and executive analytics.

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge&logo=streamlit)
![NVD](https://img.shields.io/badge/NVD-Live%20Feed-green?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</div>

---

# Executive Summary

Modern enterprises receive thousands of CVEs every week.

Traditional vulnerability scanners rank vulnerabilities primarily using CVSS scores, often ignoring business context such as:

- Asset criticality
- Revenue impact
- Data sensitivity
- Internet exposure
- Business ownership
- Production environments
- Crown jewel assets

As a result, security teams waste valuable time remediating vulnerabilities that may have minimal business impact while overlooking vulnerabilities affecting mission-critical assets.

Sentra Enterprise Cyber Risk Platform bridges this gap by transforming technical vulnerabilities into business-aware risk intelligence.

Instead of asking:

> "How severe is this CVE?"

Sentra answers:

> "Which business asset is actually at risk, what is the financial exposure, and what should leadership prioritize today?"

---

# Problem Statement

Security Operations Centers (SOCs) are overwhelmed with vulnerability alerts.

Challenges include:

- Thousands of new CVEs published every month
- Lack of business context
- Poor remediation prioritization
- Alert fatigue
- Executive reporting complexity
- Limited visibility into enterprise exposure

Organizations need intelligent prioritization—not simply vulnerability detection.

---

# Solution

Sentra continuously analyzes newly published vulnerabilities from the National Vulnerability Database (NVD), correlates them with enterprise assets, estimates business impact, and produces executive-ready intelligence.

The platform combines:

- Live Threat Intelligence
- Contextual Asset Intelligence
- Business Risk Scoring
- Exposure Estimation
- AI-generated Security Insights
- Executive Dashboards

---

# Key Features

## Live Threat Intelligence

- Real-time NVD CVE retrieval
- Continuous vulnerability monitoring
- Product inference from vulnerability descriptions
- Attack vector extraction
- Severity classification
- CVSS analysis

---

## Business Context Engine

Each vulnerability is evaluated against enterprise assets using:

- Technology stack matching
- Business criticality
- Data sensitivity
- Revenue dependency
- Regulatory impact
- Internet exposure
- Environment (Production/Test)
- Asset ownership
- Recovery objectives
- Crown Jewel classification

---

## Business Risk Prioritization

Unlike traditional vulnerability scanners, Sentra estimates:

- Business Score
- Technology Match Confidence
- Enterprise Exposure
- Executive Priority
- Risk Appetite Breach
- Board Reporting Requirements
- Recommended Remediation

---

## AI-Powered Intelligence

Integrated with Google Gemini to generate:

- Executive summaries
- Risk explanations
- Business impact narratives
- Security recommendations
- Natural-language insights

---

## Executive Dashboard

Interactive Streamlit dashboard including:

- Enterprise Exposure
- Live Threat Feed
- Business Risk Ranking
- Risk Appetite Monitoring
- Board Reporting
- Asset Intelligence
- Exposure Trends
- Executive Decision Support

---

# Architecture

```
                    National Vulnerability Database
                               │
                               ▼
                    Live CVE Collection Engine
                               │
                               ▼
                    Product Inference Engine
                               │
                               ▼
                 Enterprise Asset Correlation Engine
                               │
                               ▼
                 Business Contextualization Engine
                               │
                               ▼
                 Enterprise Risk Scoring Engine
                               │
                               ▼
                Gemini AI Intelligence Generator
                               │
                               ▼
                  Executive Risk Dashboard
```

---

# Technology Stack

| Layer | Technology |
|---------|------------|
| Language | Python 3.13 |
| Dashboard | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Threat Intelligence | NVD API |
| AI | Google Gemini |
| Configuration | dotenv |
| HTTP | Requests |
| Storage | JSON |
| Architecture | Modular Python |

---

# Business Risk Methodology

Each enterprise asset is evaluated using contextual business intelligence rather than relying solely on CVSS.

Business score incorporates:

- Technology similarity
- Business criticality
- Asset value
- Internet exposure
- Production environment
- Crown Jewel classification

The resulting score determines:

- Executive priority
- Financial exposure
- Business impact
- Board reporting requirements
- Risk appetite status

---

# Project Structure

```
Sentra-Enterprise-Cyber-Risk-Platform/

Dashboard/
    app.py

Engine/
    asset_context.py
    business_matcher.py
    config.py
    continuous_monitor.py
    data_loader.py
    llm_enricher.py
    nvd_live_fetch.py
    product_inference.py
    risk_contextualizer.py
    risk_engine.py
    risk_monitor.py
    sentra_intelligence.py
    summary_generator.py
    utils.py

Outputs/
    contextual_risk.json
    final_risk.json
    summary.json
    technical_risk.json
    risk_history.json

requirements.txt
README.md
```

---

# Dashboard Highlights

The platform provides enterprise-level visualizations including:

- Live threat intelligence
- Executive KPIs
- Business risk ranking
- Enterprise exposure
- Board reporting metrics
- AI-generated insights
- Context-aware asset intelligence

---

# Future Enhancements

- Microsoft Sentinel integration
- CrowdStrike Falcon integration
- Splunk SIEM integration
- ServiceNow ticket automation
- Jira remediation workflows
- Azure Defender integration
- AWS Security Hub
- Multi-tenant deployment
- PostgreSQL backend
- Docker deployment
- Kubernetes support
- RBAC authentication
- REST API
- Risk trend forecasting
- Predictive AI models

---

# Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Sentra-Enterprise-Cyber-Risk-Platform.git
```

Navigate into the project

```bash
cd Sentra-Enterprise-Cyber-Risk-Platform
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

```bash
GEMINI_API_KEY=YOUR_API_KEY
```

Run the dashboard

```bash
streamlit run Dashboard/app.py
```

---

# Research Inspiration

This project draws inspiration from modern Enterprise Exposure Management and Cyber Risk Quantification platforms while implementing a custom business-aware prioritization engine for educational and research purposes.

---

# Author

**Joshitha**

Computational & Applied Mathematics

Mahindra University

Specializing in

- Data Science
- Cyber Security
- AI Engineering

---

# Disclaimer

This project is intended for educational, research, and demonstration purposes. Enterprise assets, business context, and exposure values are simulated to demonstrate realistic cyber risk assessment workflows.

---

# License

Licensed under the MIT License.

---

<div align="center">

### ⭐ If you found this project interesting, consider giving it a star.

**Transforming Technical Vulnerabilities into Business Decisions**

</div>