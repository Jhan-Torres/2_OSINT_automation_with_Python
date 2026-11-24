import requests
import json

def get_rdap_info(domain):
	# Get domain record public information (WHOIS/RDAP), including the register, key dates and domain status
	print(f"[*] Consulting register info RDAP/WHOIS for: {domain}...")
	url = f"https://rdap.org/domain/{domain}"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0'}

	profile = {
		"domain": domain,
		"registrar": "Desconocido / No revelado",
		"creation_date": "No disponible",
		"expiration_date": "No disponible",
		"last_changed_date": "No disponible",
		"status": []
	}

	try:
		response = requests.get(url, headers=headers, timeout=12)
		if response.status_code == 200:
			data = response.json()

			# 1. Extract register name
			entities = data.get("entities", [])
			for entity in entities:
				roles = entity.get("roles", [])
				if "registrar" in roles:
					vcard = entity.get("vcardArray", [])
					if len(vcard) > 1 and isinstance(vcard[1], list):
						for entry in vcard[1]:
							if isinstance(entry, list) and len(entry) >= 4 and entry[0] == "fn":
								profile["registrar"] = entry[3]
								break

			# 2. Extract event dates (registration, expiration, modification)
			events = data.get("events", [])
			for event in events:
				action = event.get("eventAction")
				date = event.get("eventDate")
				if action == "registration":
					profile["creation_date"] = date
				elif action == "expiration":
					profile["expiration_date"] = date
				elif action == "last changed":
					profile["last_changed_date"] = date

			# 3. Domain tecnical status
			profile["status"] = data.get("status", [])

		else:
			print(f"[-] RDAP Request replied HTTP code {response.status_code}")

	except Exception as e:
		print(f"[-] Error al obtener datos RDAP: {e}")

	return profile

if __name__ == "__main__":
	import sys
	target = sys.argv[1] if len(sys.argv) > 1 else "github.com"

	print("\n" + "="*55)
	print(f"REGISTRATION PROFILING (RDAP / WHOIS) FOR: {target}")
	print("="*55)

	res = get_rdap_info(target)
	print(f"\n[+] Domain: {res['domain']}")
	print(f" - Register: {res['registrar']}")
	print(f" - Creation Date: {res['creation_date']}")
	print(f" - Expiration Date: {res['expiration_date']}")
	print(f" - Last Update: {res['last_changed_date']}")
	print(f" - Domain Status: {', '.join(res['status']) if res['status'] else 'No status registered'}")
