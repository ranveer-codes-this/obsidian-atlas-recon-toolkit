from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from pprint import pprint


import whois
def generate_report2(whois_data, dns_records, subdomains, ports, http_data, technologies,headers):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('template.html')

#---------------------------------- Header Card -------------------------------------------
    now = datetime.now().strftime("%d %b %Y • %H:%M")
    target_domain = whois_data["domain_name"]
#------------------------------------------------------------------------------------------

#--------------------------Attack Surface Card --------------------------------------------
    # Admin Panel Count
    admin_count = sum(
    1 for sub in subdomains
    if any(x in sub.lower() for x in [
        'admin',
        'cpanel',
        'manage',
        'portal',
        'dashboard'
    ])
)
    # Headers Count
    header_count = len(headers or {})

    #DNSSEC Check
    dnssec = str(whois_data.get("dnssec","")).strip().lower()

    # Attack Surface Card Values
    attack_surface = [

    {
        "count":len(subdomains),
        "label":"Subdomains"
    },

    {
        "count":len(ports),
        "label":"Ports"
    },

    {
        "count":admin_count,
        "label":"Admin Panel"
    },

    {
        "count":header_count,
        "label":"Headers"
    }

]
    dnssec = str(whois_data.get("dnssec","")).strip().lower()

    dnssec_enabled = dnssec not in [
        "",
        "unsigned",
        "disabled",
        "no",
        "none"
]

    if not dnssec_enabled:
        attack_surface.append(
        {
            "label":"DNSSEC Disabled",
            "danger":True,
            "full_width":True
        }
    )
    else:
        attack_surface.append(
        {
            "label":"DNSSEC Enabled",
            "success":True,
            "full_width":True
        }
    )
#------------------------------------------------------------------------------------------------------


#--------------- Small Cards --------------------------------------------------------------------------
    #DNS Records Count smallCard
    dns_records_count = sum(
        len(v)
        for v in dns_records.values()

)

#-----------------------------------------------------------------------------------------------------

#--------------------------Tactical Assessment Card ------------------------------------------------------
    #Circle value
    score = 100

    #score -= len(threat_factors)*5
    score -= admin_count*3
    score -= len(ports)*2
    if not dnssec_enabled:
        score -= 5
    score=max(score,0)

    #Condition Tray
    if score>=90:
        condition="Secure"

    elif score>=75:
        condition="Good"

    elif score>=60:
        condition="Medium"

    elif score>=40:
        condition="High"

    else:
        condition="Critical"

    #Attack Surface Tray
    surface_score = 0

    surface_score += len(subdomains)

    surface_score += len(ports)

    surface_score += admin_count

    surface_score += int(not dnssec_enabled)

    if surface_score <3:
        attack_surface="Minimal"

    elif surface_score<7:
        attack_surface="Elevated"

    else:
        attack_surface="Extensive"

    #Priority Tray
    if score<40:
        priority="P1"

    elif score<70:
        priority="P2"

    else:
        priority="P3"

    #Confidence Tray
    confidence=0
    if whois_data:
        confidence+=20
    if dns_records:
        confidence+=20
    if headers:
        confidence+=20
    if ports:
        confidence+=20
    if technologies:
        confidence+=20

#-------------------------------------------------------------------------------------------------------



#----------------------Threat Factors -----------------------------
    threat_factors=[]

    dnssec = whois_data["dnssec"]
    if dnssec.lower() in ["unsigned","disabled","no"]:
            threat_factors.append("DNSSEC Disabled")


    header_names = [h.lower() for h in headers.keys()]

    has_csp = any(
        "content-security-policy" in h
        for h in header_names
    )

    if not has_csp:
        threat_factors.append("No CSP")


    has_hsts = any(
    "strict-transport-security" in h
    for h in header_names
)

    if not has_hsts:
        threat_factors.append("No HSTS")
        threat_factors.append("No HSTS")


    management_ports = {
    22,
    21,
    23,
    3306,
    5432,
    6379,
    9200,
    8080,
    8443
    }

    if any(p in management_ports for p in ports):
        threat_factors.append(
            "Open management ports"
        )
#------------------------------------------------------------------------------------------------



#--------------------------Intelligence Card ------------------------------------------------------
    registrar = whois_data["registrar"]
    created_year = whois_data["creation_date"].year
    created_date = whois_data["creation_date"].strftime("%d %b %Y")
    expiry_year = whois_data["expiration_date"].year
    expiry_date = whois_data["expiration_date"].strftime("%d %b %Y")
    nameservers = whois_data["name_servers"]
    statuses = whois_data["status"]
    dnssec = whois_data["dnssec"]

#--------------------------------------------------------------------------------------------------


# --------------------------------- Open Ports ----------------------------------------------------

    ports_display=[]
    
    service_map={
    80:"HTTP",
    443:"HTTPS",
    22:"SSH",
    21:"FTP",
    25:"SMTP",
    53:"DNS",
    110:"POP3",
    143:"IMAP",
    3306:"MySQL",
    5432:"PostgreSQL",
    8080:"HTTP-ALT"
    }

    for port in ports:
        ports_display.append(
            {
            "number":port,
            "service":
                service_map.get(port,"Unknown"),
            "color":"pill-green"
            }
        )

#----------------------------------------------------------------------------------------------------


#------------------------------------------ HTTP Card -----------------------------------------------

    security_headers = []

    header_names = [h.lower() for h in headers.keys()]

    important_headers = [

    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "Permissions-Policy",
    "X-Content-Type-Options",
    "Referrer-Policy"

    ]

    for header in important_headers:

        security_headers.append(

            {
                "name": header,

                "secure": any(
                    header.lower() in h
                    for h in header_names
                )
            }

        )
    server = http_data.get("server", "None")


#-------------------------------------------------------------------------------------------------- 



#------------------------------Technologies Card --------------------------------------------------
    tech=[]
    
    headers = http_data["headers"]

    # Web Server
    server = headers.get("Server","").lower()

    if server=="gws":
        tech.append("Google Web Server")

    elif server:
        tech.append(server)

    # Protocol
    if "Alt-Svc" in headers:
        tech.append("HTTP/3")

    if "HTTP/2" in str(headers):
        tech.append("HTTP/2")


    # Compression
    encoding = headers.get("Content-Encoding","")

    if "gzip" in encoding:
        tech.append("gzip")

    if "br" in encoding:
        tech.append("brotli")


    # Security
    if any("content-security-policy" in h.lower() for h in headers):
        tech.append("CSP")

    if any("strict-transport-security" in h.lower() for h in headers):
        tech.append("HSTS")

    if headers.get("X-Frame-Options"):
        tech.append("XFO")
        
    #Technology Count smallCard
    technologies_count = len(tech)
    print("Detected technologies:", tech)
    print("Technology Count:", len(tech))
#---------------------------------------------------------------------------------------------------


#-------------------------------------------- Cookie Card ------------------------------------------

    cookies = http_data["cookies"]
    

#----------------------------------------------------------------------------------------------------

































    

   
    html = template.render(
        target_domain=target_domain,
        now=now,
        attack_surface=attack_surface,
        dns_records_count=dns_records_count,
        technologies_count=technologies_count,
        technologies=tech,
        risk_score=score,
        condition=condition,
        priority=priority,
        confidence=confidence,
        risk_reasons=threat_factors,
        registrar=registrar,
        created_year=created_year,
        created_date=created_date,
        expiry_year=expiry_year,
        expiry_date=expiry_date,
        nameservers=nameservers,
        statuses=statuses,
        dnssec=dnssec,
        dns=dns_records,
        subdomains=subdomains,
        ports=ports_display,
        http=http_data,
        security_headers=security_headers,
        server=server,
        headers=headers,
        cookies=cookies
    )


    filename = whois_data["domain_name"] + ".html"

    with open(f"reports/{filename}","w",encoding="utf-8") as f:
        f.write(html)
    
    return f"reports/{filename}"