import dns.resolver as res

def get_subdomains(domain):
    subdomains = [ 'www','mail','api','vpn','admin','dev','portal','staging']

    found=[]
    for sub in subdomains:
        full_domain = sub+"."+domain
        try:
            answers = res.resolve(full_domain, 'A')
            found.append(full_domain)
        except (res.NoAnswer, res.NXDOMAIN):
            continue

    return found