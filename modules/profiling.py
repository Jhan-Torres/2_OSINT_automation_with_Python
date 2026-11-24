import requests
import socket

def get_ip_info(ip):
	#Geoghraphic information, ISP, Organization and ASN from a IP address using public and free endpoints from ip-api.com.
	print(f"[*] Getting information and geolocation from the IP: {ip}...")
	url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"

	try:
		response = requests.get(url, timeout=10)
		if response.status_code == 200:
			data = response.json()
			if data.get("status") == "success":
				return {
					"ip": data.get("query"),
					"country": data.get("country"),
					"country_code": data.get("countryCode"),
					"region": data.get("regionName"),
					"city": data.get("city"),
					"isp": data.get("isp"),
					"org": data.get("org"),
					"asn": data.get("as")
				}
			else:
				print(f"[-] Unsuccessfull response from IP: {ip}: {data.get('message')}")
		else:
			print(f"[-] Error HTTP {response.status_code} requesting IP {ip}")
	except Exception as e:
		print(f"[-] Exception from IP - {ip}: {e}")

	return None

def get_reverse_dns(ip):
	#Inverse DNS query (PTR record) to get linked host IP.
	try:
		host, _, _ = socket.gethostbyaddr(ip)
		return host
	except Exception:
		return "No PTR records / No Available"

def profile_target_ips(ip_list):
	#Receive a list of IP addresses and generate a complete profile for each one.
	profiles = []
	unique_ips = sorted(list(set(ip_list)))

	for ip in unique_ips:
		info = get_ip_info(ip)
		if info:
			info["reverse_dns"] = get_reverse_dns(ip)
			profiles.append(info)

	return profiles

if __name__ == "__main__":
	import sys
	test_ips = sys.argv[1:] if len(sys.argv) > 1 else ["140.82.112.4", "8.8.8.8"]

	print("\n" + "="*50)
	print("(OSINT) IP ADRESSES PROFILING")
	print("="*50)

	results = profile_target_ips(test_ips)
	for p in results:
		print(f"\n[+] IP: {p['ip']}")
		print(f" - Reverse DNS (PTR): {p['reverse_dns']}")
		print(f" - Location: {p['city']}, {p['region']}, {p['country']} ({p['country_code']})")
		print(f" - Provider (ISP): {p['isp']}")
		print(f" - Org: {p['org']}")
		print(f" - ASN: {p['asn']}")
