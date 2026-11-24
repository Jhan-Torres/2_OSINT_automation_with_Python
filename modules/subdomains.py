import requests
import json

def get_subdomains_crtsh(domain):
	#obtains public subdomains requesting transparent certifies (crt.sh)
	print("[*] Searching using CRT.SH")
	url = f"https://crt.sh/?q=%.{domain}&output=json"
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) OSINT-Tool/1.0'
	}
	subdomains = set()

	try:
		response = requests.get(url, headers=headers, timeout=30)
		if response.status_code == 200:
			data = response.json()
			for entry in data:
				name_value = entry.get('name_value', '')
				# crt.sh may return multiple subdomains separated by line breaks
				lines = name_value.split('\n')
				for line in lines:
					line = line.strip().lower()
					# Delete wildcard certs (*.domain.com)
					if line.startswith('*.'):
						line = line[2:]
					# filter those that belongs the consulted domain only
					if line.endswith(domain) and line != domain:
						subdomains.add(line)
			return subdomains
	except Exception as e:
		print(f"[-] CRT.SH failed or timeout: {e}")
	return set()

def get_subdomains_hackertarget(domain):
	#support source with HackerTarget API
	print("[*] Asking another source (HackerTarget)...")
	url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
	subdomains = set()

	try:
		response = requests.get(url, timeout=15)
		if response.status_code == 200 and "error" not in response.text.lower():
			lines = response.text.split('\n')
			for line in lines:
				parts = line.split(',')
				if len(parts) >= 1:
					subdom = parts[0].strip().lower()
					if subdom.endswith(domain) and subdom != domain:
						subdomains.add(subdom)
			return subdomains
	except Exception as e:
		print(f"[-] HackerTarget falló: {e}")
	return set()

def get_subdomains(domain): 
	print(f"[*] Searching subdomains for {domain}...")
	
	# try crt.sh
	subdomains = get_subdomains_crtsh(domain)

	# use hackertarget if crt.sh fails
	if not subdomains:
		subdomains = get_subdomains_hackertarget(domain)

	results = sorted(list(subdomains))
	print(f"[+] Found {len(results)} unique subdomains")
	return results

if __name__ == "__main__":
	import sys
	target = sys.argv[1] if len(sys.argv) > 1 else "example.com"
	results = get_subdomains(target)
	for sub in results[:15]:
		print(f"  -  {sub}")

