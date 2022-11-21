import cloudscraper
from bs4 import BeautifulSoup
import re
import time
import json

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

def ez4(url):
    
    client = cloudscraper.create_scraper(allow_brotli=False)
      
    DOMAIN = "https://ez4short.com"
     
    ref = "https://techmody.io/"
    
    h = {"referer": ref}
  
    resp = client.get(url,headers=h)
    
    soup = BeautifulSoup(resp.content, "html.parser")
    
    inputs = soup.find_all("input")
   
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("

def olamovies(url):
    
    print("this takes time, you might want to take a break.")
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

    client = cloudscraper.create_scraper()
    res = client.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.findAll("div", class_="wp-block-button")
   
    outlist = []
    for ele in soup:
        outlist.append(ele.find("a").get("href"))

    slist = []
    for ele in outlist:
        try:
            key = ele.split("?key=")[1].split("&id=")[0].replace("%2B","+").replace("%3D","=").replace("%2F","/")
            id = ele.split("&id=")[1]
        except:
            continue
        
        count = 3
        params = { 'key': key, 'id': id}
        soup = "None"
        print("trying","https://olamovies.wtf/download/&key="+key+"&id="+id)
        
        url = "https://olamovies.wtf/download/&key="+key+"&id="+id
        while 'rocklinks.net' not in soup and "try2link.com" not in soup and "ez4short.com" not in soup:
         
            res = client.get("https://olamovies.ink/download/", params=params, headers=headers)
            jack = res.text
            rose = jack.split('url = "')[-1]
            soup = rose.split('";')[0]
            
            if soup != "":
                if "try2link.com" in soup or 'rocklinks.net' in soup or "ez4short.com" in soup:
                    print("added", soup)
                    slist.append(soup)
                else:
                    print(soup, "not addded")
            else:
                if count == 0:
                    print('moving on')
                    break
                else:
                    count -= 1
                    print("retrying")
                
            print("waiting 10 secs")
            time.sleep(10)

    #print(slist)
    final = []
    for ele in slist:
        if "rocklinks.net" in ele:
            final.append(rocklinksbyapss(ele))
        elif "try2link.com" in ele:
            final.append(try2link_bypass(ele))
        elif ""ez4short.com" in ele:
            final.append(ez4(ele))
        else:
            print(ele)
    #print(final)
    links = ""
    for ele in final:
        links = links + ele + "\n"
    print("Bypassed Links")
    print(links)
    return links

url = "https://olamovies.cyou/total-dhamaal-2019-hindi/"
olamovies(url)
