from modules.report_generator2 import generate_report2
from modules.whois_enum import get_whois
from modules.dns_enum import get_dns_records
from modules.subdomain_enum import get_subdomains
from modules.port_scan import scan_ports
from modules.http_fingerprint import fingerprint_http
from modules.tech_detect import detect_tech
from modules.report_generator import *

def run_scan(domain):

    whois_data = get_whois(domain)

    dns_records = get_dns_records(domain)

    subs = get_subdomains(domain)

    ports = scan_ports(domain)

    http_data = fingerprint_http(domain)

    technologies = detect_tech(http_data)
    
    report = generate_report2(
    whois_data,
    dns_records,
    subs,
    ports,
    http_data,
    technologies,
    http_data["headers"],
)

    scan_data = {
        "target": domain,
        "whois": whois_data,
        "dns": dns_records,
        "subdomains": subs,
        "ports": ports,
        "http": http_data,
        "technologies": technologies
    }
    
    return report, scan_data
