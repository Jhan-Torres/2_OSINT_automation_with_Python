import dns.resolver
import dns.rdatatype

def get_dns_records(domain):
	# Resolves and extract key DNS records (A, MX, NS, TXT) for the domain
	print(f"[*] Consulting DNS record for: {domain}...")
	dns_data = {
		"A": [],
		"MX": [],
		"NS": [],
		"TXT": []
	}

	resolver = dns.resolver.Resolver()
	resolver.timeout = 5
	resolver.lifetime = 5

	# 1: "A" Records (IP addresses)
	try:
		answers = resolver.resolve(domain, 'A')
		for rdata in answers:
			if rdata.rdtype == dns.rdatatype.A:
				dns_data["A"].append(rdata.to_text())
	except dns.resolver.NoAnswer:
		pass
	except Exception as e:
		print(f"[-] Can not get A records: {e}")

	# 2: "MX" Records (Mail Servers)
	try:
		answers = resolver.resolve(domain, 'MX')
		for data in answers:
			if rdata.rdtype == dns.rdatatype.MX:
				dns_data["MX"].append({
					"preference": rdata.preference,
					"exchange": str(rdata.exchange).rstrip('.')
				})
	except dns.resolver.NoAnswer:
		pass
	except Exception as e:
		print(f"[-] Can not get MX records: {e}")

	# 3: "NS" Records (Name Servers)
	try:
		answers = resolver.resolve(domain, 'NS')
		for rdata in answers:
			if rdata.rdtype == dns.rdatatype.NS:
				dns_data["NS"].append(str(rdata.target).rstrip('.'))
	except dns.resolver.NoAnswer:
		pass
	except Exception as e:
		print(f"[-] Can not get NS records: {e}")

	# 4: "TXT" Records (SPF, DMARC, Third Providers)
	try:
		answers = resolver.resolve(domain, 'TXT')
		for rdata in answers:
			# every TXT rdata contains a bytes list inside rdata.strings
			txt_str = "".join([s.decode('utf-8', errors='ignore') for s in rdata.strings])
			dns_data["TXT"].append(txt_str)
	except dns.resolver.NoAnswer:
		pass
	except Exception as e:
		print(f"[-] Can not get TXT records: {e}")

	return dns_data

if __name__ == "__main__":
	import sys
	target = sys.argv[1] if len(sys.argv) > 1 else "github.com"
	results = get_dns_records(target)

	print("\n" + "="*40)
	print(f"DNS RESULTS FOR: {target}")
	print("="*40)

	print("\n[+] Registros A:")
	for val in results["A"]:
		print(f" - {val}")
	if not results["A"]:
		print(" (No data found)")

	print("\n[+] Registros MX:")
	for mx in results["MX"]:
		print(f" - Prioridad: {mx['preference']} | Servidor: {mx['exchange']}")
	if not results["MX"]:
		print(" (No data found)")

	print("\n[+] Registros NS:")
	for val in results["NS"]:
		print(f" - {val}")
	if not results["NS"]:
		print(" (No data found)")

	print("\n[+] Registros TXT:")
	for val in results["TXT"]:
		print(f" - {val}")
	if not results["TXT"]:
		print(" (No data found)")
