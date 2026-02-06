import requests
import csv
import time

API_KEY = "PUT YOUR KEY HERE"

DOMAINS_FILE = r"C:\Users\Jayesh\Downloads\domains.txt"
OUTPUT_FILE = r"C:\Users\Jayesh\Downloads\whoisxml_results.csv"

with open(DOMAINS_FILE) as f:
    domains = [d.strip() for d in f if d.strip()]

results = []

for i, domain in enumerate(domains, start=1):
    print(f"[{i}/{len(domains)}] {domain}")

    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"

    params = {
        "apiKey": API_KEY,
        "domainName": domain,
        "outputFormat": "JSON"
    }

    try:
        r = requests.get(url, params=params, timeout=20)
        data = r.json()

        record = data.get("WhoisRecord", {})

        registrar = record.get("registrarName")
        created = record.get("createdDate")
        expires = record.get("expiresDate")
        nameservers = record.get("nameServers", {}).get("hostNames")

        results.append({
            "domain": domain,
            "registrar": registrar,
            "creation_date": created,
            "expiration_date": expires,
            "name_servers": ",".join(nameservers) if nameservers else None
        })

        time.sleep(0.5)  # respect rate limits

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append({
            "domain": domain,
            "registrar": None,
            "creation_date": None,
            "expiration_date": None,
            "name_servers": None
        })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved: {OUTPUT_FILE}")

