def detect_tech(http_data):
    technologies=[]
    headers = http_data.get("headers", {})
    html = http_data.get("html", "").lower()    
    server=headers.get("Server", "").lower()

    server_sig = {
    'nginx':'Nginx',
    'apache':'Apache',
    'iis':'Microsoft IIS',
    'gws':'Google Web Server'}

    for key, value in server_sig.items():
        if key in server:
            technologies.append(value)

    if 'CF_RAY' in headers:
        technologies.append('Cloudflare')

    if 'react' in html:
        technologies.append('React')
    if 'bootstrap' in html:
        technologies.append('Bootstrap')
    if 'wp_content' in html:
        technologies.append('WordPress')
    
    technologies = list(set(technologies))
    return technologies
    