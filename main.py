#!/usr/bin/env python3
import argparse
import sys
import os

# Import modules developed
from modules.subdomains import get_subdomains
from modules.dns_info import get_dns_records
from modules.profiling import profile_target_ips
from modules.target_profiling import get_rdap_info
from modules.reporter import export_json, export_pdf

def banner():
	print("""
	=====================================================
	📡 AUTOMATED OSINT & TARGET PROFILING TOOL (Python 3)
	=====================================================
	""")

def main():
	banner()

	parser = argparse.ArgumentParser(description="OSINT automation tool and infrastructure profilinga.")
	parser.add_argument("-d", "--domain", required=True, help="Target Domain to OSINT analysis (ej. example.com)")
	parser.add_argument("-o", "--output", default="report", help="Final report files base name (no extension)")

	args = parser.parse_args()
	target_domain = args.domain.lower().strip()
	output_base = args.output

	print(f"[+] Initializing full OSINT reconnaissance for: {target_domain}\n")

	# 1. Register Profiling (RDAP / WHOIS)
	rdap_data = get_rdap_info(target_domain)
	print("-" * 50)

	# 2. DNS records resolution
	dns_data = get_dns_records(target_domain)
	print("-" * 50)

	# 3. IP addresses profiling (Geolocalization, ASN, Reverse DNS)
	ip_profiles = []
	if dns_data.get("A"):
		ip_profiles = profile_target_ips(dns_data["A"])
		print("-" * 50)

	# 4. Passive Subdomain Discovery
	subdomains_list = get_subdomains(target_domain)
	print("-" * 50)

	# 5. Full Results
	full_report = {
		"target_domain": target_domain,
		"rdap_info": rdap_data,
		"dns_info": dns_data,
		"ip_profiles": ip_profiles,
		"subdomains": subdomains_list
	}

	# 6. Reports Generation
	print("\n[*] Generating findings report...")
	json_filename = f"{output_base}_{target_domain}.json"
	pdf_filename = f"{output_base}_{target_domain}.pdf"

	export_json(full_report, json_filename)
	export_pdf(full_report, pdf_filename)

	print("\n" + "="*55)
	print(" 🚀 RECONNAISSANCE COMPLETED")
	print("="*55)
	print(f"JSON File: {json_filename}")
	print(f"PDF File: {pdf_filename}\n")

if __name__ == "__main__":
	main()
