import time
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from requests import get, head

url = "https://olamovies.wtf/download/?key=q84dMFiC0FYTVJoS5frBQSEqpFUgODxFinhNFysPVAvi4BuIx%2BQ%3D&id=e80cb9b8088e5aebb0998aa2caf32122"

def ola(url) :
    soup = "None"
    client = cloudscraper.create_scraper(allow_brotli=False)
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': url,
            'Alt-Used': 'olamovies.ink',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
    while 'rocklinks.net' not in soup and "try2link.com" not in soup:
            res = client.get(url, headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            print(soup)
            soup = soup.findAll("a")[0].get("href")
            if soup != "":
                   if "rocklinks.net" in soup:
                        url = soup
                        link = try2link_bypass(url)
                        print(link) 
                   elif "try2link.com" in soup:
                        url = soup
                        link = rocklinksbyapss(url)
                        print(link)
            time.sleep(10)

def try2link_bypass(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    
    url = url[:-1] if url[-1] == '/' else url
    
    params = (('d', int(time.time()) + (60 * 4)),)
    r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
    
    soup = BeautifulSoup(r.text, 'html.parser')
    inputs = soup.find(id="go-link").find_all(name="input")
    data = { input.get('name'): input.get('value') for input in inputs }    
    time.sleep(7)
    
    headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
    
    bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
    return bypassed_url.json()["url"]

def rocklinksbyapss(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle="
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("
print(ola(url))