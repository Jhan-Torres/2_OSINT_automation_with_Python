import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def export_json(data, output_path):
	# Saves all the findings in a structured JSON file
	try:
		with open(output_path, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=4, ensure_ascii=False)
		print(f"[+] JSON report succesfully saved to: {output_path}")
	except Exception as e:
		print(f"[-] Error at saving JSON report: {e}")

def export_pdf(data, output_path):
	# Generate a executive PDF report using ReportLab
	try:
		doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
		story = []
		styles = getSampleStyleSheet()

		# Personalized Styles
		title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor("#1e293b"), spaceAfter=12)
		h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor("#0f766e"), spaceBefore=12, spaceAfter=6)
		normal_style = ParagraphStyle('NormalStyle', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor("#334155"), leading=14)

		# Header
		target = data.get("target_domain", "Unknown")
		story.append(Paragraph(f"OSINT Reconnaissance Report to: {target}", title_style))
		story.append(Spacer(1, 10))

		# 1.  RDAP / WHOIS Registration
		story.append(Paragraph("1. Register Information (RDAP / WHOIS)", h2_style))
		rdap = data.get("rdap_info", {})
		rdap_text = f"""
		<b>Domain:</b> {rdap.get('domain', target)}<br/>
		<b>Register:</b> {rdap.get('registrar', 'N/A')}<br/>
		<b>Creation Date:</b> {rdap.get('creation_date', 'N/A')}<br/>
		<b>Expiration Date:</b> {rdap.get('expiration_date', 'N/A')}<br/>
		<b>Last Update:</b> {rdap.get('last_changed_date', 'N/A')}<br/>
		"""
		story.append(Paragraph(rdap_text, normal_style))
		story.append(Spacer(1, 10))

		# 2. DNS Records
		story.append(Paragraph("2. Infrastructure and DNS records", h2_style))
		dns = data.get("dns_info", {})
		dns_text = f"""
		<b>IP Addresses (A):</b> {', '.join(dns.get('A', [])) if dns.get('A') else 'None'}<br/>
		<b>Name Servers (NS):</b> {', '.join(dns.get('NS', [])) if dns.get('NS') else 'None'}<br/>
		"""
		story.append(Paragraph(dns_text, normal_style))

		if dns.get("TXT"):
			story.append(Paragraph("<b>Registros TXT (Technology Footprint / Suppliers):</b>", normal_style))
			for txt in dns.get("TXT", []):
				story.append(Paragraph(f"• {txt}", normal_style))
		story.append(Spacer(1, 10))

		# 3. Subdomains found
		story.append(Paragraph("3. Discovered subdomains", h2_style))
		subs = data.get("subdomains", [])
		story.append(Paragraph(f"Total of subdomains found: <b>{len(subs)}</b>", normal_style))
		sub_sample = subs[:20] if len(subs) > 20 else subs
		for s in sub_sample:
			story.append(Paragraph(f"• {s}", normal_style))
		if len(subs) > 20:
			story.append(Paragraph(f"<i>... and {len(subs) - 20} subdomains in addition (see JSON file).</i>", normal_style))

		# PDF document construction
		doc.build(story)
		print(f"[+] Reporte PDF report saved successfully in: {output_path}")

	except Exception as e:
		print(f"[-] Error in PDF Generation: {e}")

if __name__ == "__main__":
	#Fast test
	dummy_data = {
		"target_domain": "example.com",
		"rdap_info": {"domain": "example.com", "registrar": "Example Registrar", "creation_date": "2020-01-01"},
		"dns_info": {"A": ["93.184.216.34"], "NS": ["a.iana-servers.net"], "TXT": ["v=spf1 -all"]},
		"subdomains": ["api.example.com", "dev.example.com"]
	}
	export_json(dummy_data, "test_report.json")
	export_pdf(dummy_data, "test_report.pdf")
