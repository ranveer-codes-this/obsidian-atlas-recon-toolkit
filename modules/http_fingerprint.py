import requests


def fingerprint_http(domain):

    url = None
    response = None

    try:
        url = f"https://{domain}"
        response = requests.get(url,timeout=5)

    except requests.RequestException:
        try:
            url = f"http://{domain}"
            response = requests.get(url,timeout=5)
        except requests.RequestException:
            return None
    status_code = response.status_code
    server = response.headers.get("Server")
    response_time = response.elapsed.total_seconds()
    content_type = response.headers.get("Content-Type")
    redirect_url= response.url
    cookies = response.cookies.get_dict()
    headers = dict(response.headers)

    fingerprint = {"status_code": status_code, 
                   "server": server, 
                   "response_time": response_time,
                   "content_type": content_type,
                   "redirect_url": redirect_url, 
                   "cookies": cookies, 
                   "headers": headers,
                   "html" : response.text}
    
    return fingerprint