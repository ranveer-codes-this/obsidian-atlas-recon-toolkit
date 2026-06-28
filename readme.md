<div align="center">

# OBSIDIAN ATLAS

### Passive Attack Surface Intelligence Framework

*Know the surface before the adversary does.*

---

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?style=for-the-badge)
![License](https://img.shields.io/badge/Educational-Use-success?style=for-the-badge)
![Status](https://img.shields.io/badge/Version-1.0.0-cyan?style=for-the-badge)

</div>

---

# Overview

OBSIDIAN ATLAS is a passive reconnaissance and attack surface intelligence framework developed for automated external target enumeration.

The framework consolidates multiple reconnaissance modules into a single tactical dashboard capable of collecting publicly available intelligence, analysing attack surface exposure, identifying technologies, inspecting HTTP security posture, and generating professional intelligence reports.

The platform is designed around a modular architecture, allowing each reconnaissance component to operate independently while contributing to a unified reporting engine.

---

# Core Capabilities

- WHOIS Intelligence
- DNS Enumeration
- Passive Subdomain Discovery
- Port Enumeration
- HTTP Fingerprinting
- Technology Detection
- Security Header Analysis
- Threat Assessment
- Interactive Mission Console
- Tactical Dashboard
- HTML Intelligence Report
- PDF Export
- JSON Export
- CSV Export

---

# Reconnaissance Workflow

```

Acquire Target

↓

WHOIS Intelligence

↓

DNS Enumeration

↓

Passive Subdomain Discovery

↓

Port Enumeration

↓

HTTP Fingerprinting

↓

Technology Detection

↓

Threat Assessment

↓

Report Generation

↓

Interactive Dashboard

```

---

# Project Architecture

```

launcher.py

↓

main.py

↓

Recon Modules

├── WHOIS

├── DNS

├── Subdomains

├── Ports

├── HTTP Analysis

├── Technology Detection

└── Threat Engine

↓

Report Generator

↓

Dashboard

↓

Export Engine

```

---

# Features

## Passive Intelligence Collection

Collects publicly available information without interacting aggressively with the target infrastructure.

---

## WHOIS Intelligence

- Registrar
- Creation Date
- Expiration Date
- Name Servers
- DNSSEC
- Registration Status

---

## DNS Enumeration

Supports collection of

- A Records
- AAAA Records
- MX Records
- TXT Records
- NS Records
- CNAME Records

---

## Passive Subdomain Discovery

Discovers publicly indexed subdomains using passive intelligence sources.

---

## Port Enumeration

Identifies exposed services and evaluates externally accessible ports.

---

## HTTP Fingerprinting

Collects

- Response Headers
- Response Time
- Status Code
- Cookies
- Security Headers

---

## Technology Detection

Identifies

- Web Server
- HTTP Protocol
- Compression
- Framework Indicators
- Security Technologies

---

## Threat Assessment

Generates a tactical overview based on collected intelligence.

Includes:

- Attack Surface
- Risk Score
- Threat Factors
- Confidence
- Priority
- Exposure Summary

---

# Interactive Dashboard

The generated HTML dashboard contains

- Executive Summary
- Attack Surface Metrics
- Tactical Assessment
- WHOIS Intelligence
- DNS Records
- HTTP Analysis
- Security Headers
- Cookie Inspection
- Technology Profile
- Threat Factors
- Report Downloads

---

# Export Formats

The framework supports

- HTML
- PDF
- JSON
- CSV

---

# Directory Structure

```

ReconToolkit/

├── launcher.py

├── main.py

├── requirements.txt

├── start_atlas.bat

│

├── modules/

│ ├── whois_enum.py

│ ├── dns_enum.py

│ ├── subdomain_enum.py

│ ├── port_scan.py

│ ├── http_fingerprint.py

│ ├── tech_detect.py

│ └── report_generator.py

│

├── templates/

├── static/

├── reports/

└── wordlists/

```

---

# Installation

Clone repository

```bash
git clone https://github.com/<username>/obsidian-atlas.git
```

Open project

```bash
cd obsidian-atlas
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch

```bash
python launcher.py
```

or

```bash
start_atlas.bat
```

---

# Technology Stack

Backend

- Python
- Flask

Frontend

- HTML
- CSS
- Vanilla JavaScript
- Jinja2

Libraries

- requests
- dnspython
- python-whois
- BeautifulSoup
- socket
- ssl

---

# Intended Usage

This framework is intended for

- Educational Purposes
- Security Research
- Defensive Reconnaissance
- Internal Security Assessments

---

# Roadmap

- ASN Enumeration
- SSL Certificate Analysis
- WAF Detection
- Wayback Integration
- Shodan Integration
- CVE Correlation
- Screenshot Engine
- Docker Support
- REST API
- Plugin System

---

# Disclaimer

This framework is intended solely for authorised security assessments, educational purposes, and defensive reconnaissance.

Only analyse systems that you own or have explicit permission to assess.

The developers assume no responsibility for misuse of this software.

---

<div align="center">

**OBSIDIAN ATLAS**

Passive Attack Surface Intelligence Framework

Version 1.0.0

</div>