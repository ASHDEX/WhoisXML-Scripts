import requests
import csv
import time
import dns.resolver

API_KEY = "PUT_YOUR_WHOISXML_API_KEY_HERE"

DOMAINS_FILE = r"C:\Users\Jayesh\Downloads\domains.txt"
OUTPUT_FILE = r"C:\Users\Jayesh\Downloads\whoisxml_full_enrichment.csv"

def whois_lookup(domain):
    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    data = r.json().get("WhoisRecord", {})
    return {
        "registrar": data.get("registrarName"),
        "created": data.get("createdDate"),
        "expires": data.get("expiresDate")
    }

def dns_lookup(domain):
    url = "https://www.whoisxmlapi.com/dnslookupservice"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    data = r.json().get("DNSData", {})
    ips = [rec.get("ip") for rec in data.get("dnsRecords", []) if rec.get("ip")]
    return ",".join(set(ips)) if ips else None

def reputation_lookup(domain):
    url = "https://www.whoisxmlapi.com/reputationservice"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    data = r.json().get("reputation", {})
    return data.get("riskScore")

def category_lookup(domain):
    url = "https://www.whoisxmlapi.com/websitescategoryservice"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    data = r.json().get("categories", [])
    return ",".join([c.get("name") for c in data if c.get("name")])

def ssl_lookup(domain):
    url = "https://www.whoisxmlapi.com/sslcertificateservice"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    certs = r.json().get("certificates", [])
    if certs:
        return certs[0].get("issuer"), certs[0].get("notAfter")
    return None, None

def threat_lookup(domain):
    url = "https://www.whoisxmlapi.com/threatintelligenceservice"
    params = {"apiKey": API_KEY, "domainName": domain, "outputFormat": "JSON"}
    r = requests.get(url, params=params, timeout=20)
    data = r.json().get("threatIntelligence", {})
    return data.get("threatType")

with open(DOMAINS_FILE) as f:
    domains = [d.strip() for d in f if d.strip()]

results = []

for i, domain in enumerate(domains, start=1):
    print(f"[{i}/{len(domains)}] Enriching {domain}")

    try:
        whois = whois_lookup(domain)
        dns_ips = dns_lookup(domain)
        risk = reputation_lookup(domain)
        category = category_lookup(domain)
        issuer, ssl_expiry = ssl_lookup(domain)
        threat = threat_lookup(domain)

        results.append({
            "domain": domain,
            "registrar": whois["registrar"],
            "created": whois["created"],
            "expires": whois["expires"],
            "ips": dns_ips,
            "reputation_score": risk,
            "category": category,
            "ssl_issuer": issuer,
            "ssl_expiry": ssl_expiry,
            "threat_type": threat
        })

        time.sleep(0.7)  # avoid rate limits

    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append({
            "domain": domain,
            "registrar": None,
            "created": None,
            "expires": None,
            "ips": None,
            "reputation_score": None,
            "category": None,
            "ssl_issuer": None,
            "ssl_expiry": None,
            "threat_type": None
        })

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved: {OUTPUT_FILE}")
