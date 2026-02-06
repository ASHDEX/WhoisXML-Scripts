# WhoisXML Scripts

This repository contains Python scripts for interacting with the **WhoisXML API** and related DNS/WHOIS services to automate domain and IP threat intelligence enrichment.

Whois and DNS data are important signals in security investigations, threat hunting, and risk assessment. This collection of scripts helps security professionals quickly gather contextual information about domains, IPs, and related infrastructure.

---

## 🚀 What These Scripts Do

The scripts in this repository allow you to:
- Query WHOIS records for domains
- Look up DNS records (A, MX, TXT, NS, etc.)
- Perform bulk lookups for multiple domains/IPs
- Parse and format intelligence for downstream use in detection, investigation, or automation workflows

These tools simplify enrichment tasks that would otherwise be manual and repetitive.

---

##  Why This Matters

Domain and IP reputation data are essential in:
- Identifying potentially malicious infrastructure
- Correlating suspicious activity with known bad actors
- Augmenting SIEM and SOAR enrichment steps
- Triaging alerts during incident response

Automating these lookups saves time, reduces errors, and provides consistent threat context across investigations.

---

## Prerequisites

Before using the scripts:
- Python 3.6+ installed
- A **WhoisXML API key** (free or paid tier)
- Install dependencies:
  ```bash
  pip install -r requirements.txt
