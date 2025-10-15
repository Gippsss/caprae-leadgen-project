# enrich.py
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; CapraeLeadGen/1.0)'}
EMAIL_RE = re.compile(r'[a-zA-Z0-9.\-+_]+@[a-zA-Z0-9.\-+_]+\.[a-zA-Z]+')

def fetch_html(url, timeout=8):
    """Fetch page HTML safely."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None

def extract_emails(text):
    return list(set(EMAIL_RE.findall(text or '')))

def find_contact_links(soup, base_url):
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href'].lower()
        if any(k in href for k in ('contact', 'about', 'team', 'connect', 'get-in-touch')):
            links.add(urljoin(base_url, a['href']))
    return list(links)

def infer_industry(text):
    t = (text or '').lower()
    if any(k in t for k in ['saas', 'software', 'platform', 'api']):
        return 'SaaS / Software'
    if any(k in t for k in ['marketplace']):
        return 'Marketplace'
    if any(k in t for k in ['consult', 'agency', 'services']):
        return 'Services'
    return 'Unknown'

def score_result(found_emails, contact_links, industry):
    score = 0
    if found_emails:
        score += 50
    if contact_links:
        score += 20
    if industry == 'SaaS / Software':
        score += 10
    if not found_emails and not contact_links:
        score -= 10
    return max(0, min(100, score))

def enrich_domain(domain):
    root = domain if domain.startswith('http') else f'https://{domain}'
    html = fetch_html(root)
    result = {'domain': domain, 'industry': 'Unknown',
              'contact_links': [], 'found_emails': [], 'score': 0}

    if not html:
        return result

    soup = BeautifulSoup(html, 'html.parser')
    result['industry'] = infer_industry(html)
    result['found_emails'] = extract_emails(html)
    result['contact_links'] = find_contact_links(soup, root)

    # Crawl first few contact pages for more emails
    for link in result['contact_links'][:3]:
        sub_html = fetch_html(link)
        if sub_html:
            result['found_emails'] += extract_emails(sub_html)

    result['found_emails'] = list(set(result['found_emails']))
    result['score'] = score_result(result['found_emails'],
                                   result['contact_links'],
                                   result['industry'])
    return result

def enrich_from_csv(input_csv, output_csv='output/enriched.csv'):
    df = pd.read_csv(input_csv)
    results = []
    for domain in df['website'].astype(str):
        print(f'🔍 Processing {domain}')
        results.append(enrich_domain(domain))
    out = pd.DataFrame(results)
    out.to_csv(output_csv, index=False)
    return out
