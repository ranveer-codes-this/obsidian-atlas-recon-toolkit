import whois

def get_whois(domain):
    result= whois.whois(domain)

    creation_date = result.creation_date
    expiration_date = result.expiration_date


    if isinstance(creation_date, list):
        creation_date = creation_date[0]

    if isinstance(expiration_date, list):
        expiration_date = expiration_date[0]

    return{
        "domain_name": result.domain_name,
        "registrar": result.registrar,
        "creation_date": creation_date,
        "expiration_date": expiration_date,
        "name_servers": result.name_servers,
        "status": result.status,
        "dnssec": result.dnssec,
        "headers": result.headers,
    }