##Automated OSINT & Target Profiling Tool

A modular command-line interface (CLI) tool developed in **Python 3** to automate open-source intelligence (**OSINT**) gathering and infrastructure profiling for target domains and IP addresses.

## Key Features
* **Passive Subdomain Discovery:** Query Certificate Transparency logs (`crt.sh`) and fallback services (`HackerTarget`) without directly interacting with the target infrastructure.
* **DNS Resolution & Tech Stack Fingerprinting:** Extraction of `A`, `MX`, `NS`, and `TXT` records (mapping corporate third-party service providers such as Google Workspace, Microsoft 365, Atlassian, OpenAI, Stripe, etc., through SPF policy analysis).
* **IP Profiling & Geolocation:** Analysis of physical geolocation (country, city), Internet Service Provider (ISP), Autonomous System Number (ASN), and Reverse DNS (`PTR`) resolution.
* **RDAP / WHOIS Domain Registration Profiling:** Queries official registrar information, domain lifecycle key dates, and EPP security status codes.
* **Automated Report Generation:** Complete export of findings in both **JSON** format (for programmatic integration) and **PDF** format (for executive presentations).

## Project Structure

```text
2_OSINT_automation_with_Python/
├── main.py 				# Main script and CLI orchestrator
├── modules/
│   ├── __init__.py
│   ├── subdomains.py 			# Subdomain discovery module
│   ├── dns_info.py 			# DNS resolution and TXT record module
│   ├── profiling.py 			# IP profiling, ASN, and Geolocation module
│   ├── target_profiling.py 		# RDAP / WHOIS registration module
│   └── reporter.py 			# JSON and PDF report generator
├── .env.example 			# Environment variables template
├── .gitignore 				# Exclusion rules for secrets and virtual environment
└── README.md				# Project documentation
```

## Installation & Requirements
1. Clone the repository:
```bash
git clone https://github.com/Jhan-Torres/2_OSINT_automation_with_Python.git
cd 2_OSINT_automation_with_Python
```

2. Create and activate the virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies:
```bash
pip install requests python-dotenv dnspython reportlab
```

## Usage
Run the main script specifying the target domain using the `-d` or `--domain` flag:
```bash
python3 main.py -d hackthebox.com -o hackthebox_scan
```

Parameters:
* -d, --domain: (Required) Target domain for OSINT analysis.
* -o, --output: (Optional) Base filename for the .json and .pdf output reports (Default: report).

## 🎯 Red Team vs. Blue Team Perspective

### 🔴 Red Team (Offensive Focus)

* **Unauditable Passive Reconnaissance:** Gathering subdomains and IP addresses without triggering alerts on the target's infrastructure.
* **Supply Chain Fingerprinting:** Identifying third-party services (Slack, Zendesk, Jamf, Miro) via `TXT` records to craft targeted Spear Phishing campaigns.
* **Attack Surface Discovery:** Spotting abandoned or legacy dev/staging subdomains prone to vulnerabilities such as *Subdomain Takeover*.

### 🔵 Blue Team (Defensive / Threat Intel Focus)

* **Attack Surface Management (ASM):** Continuous inventory and mapping of all organization assets exposed to the internet.
* **SPF/DMARC Record Audit:** Verifying email authentication policies and purging stale `TXT` records from legacy SaaS vendors.
* **Domain Hijacking Prevention:** Verifying EPP security locks (`clientTransferProhibited`, `clientUpdateProhibited`) via RDAP registration records. EOF
