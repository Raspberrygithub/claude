#!/usr/bin/env python3
"""
Jay W. Richards Article Scraper
================================
Run this script locally (with internet access) to fetch full article text
from all known Jay Richards author archive pages and individual articles.

Requirements:
    pip install requests beautifulsoup4 lxml

Usage:
    python scraper.py
"""

import os
import re
import time
import json
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

OUTPUT_DIR = "individual"
COMBINED_FILE = "jay_richards_complete_works.txt"
URLS_LOG = "scraped_urls.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ── Author archive pages (paginated) ──────────────────────────────────────
AUTHOR_ARCHIVES = [
    # (base_url, page_pattern, max_pages)
    ("https://stream.org/author/jayrichards/", "https://stream.org/author/jayrichards/page/{}/", 15),
    ("https://stream.org/author/robisonrichards/", "https://stream.org/author/robisonrichards/page/{}/", 5),
    ("https://stream.org/author/jay-richards-and-john-zmirak/", "https://stream.org/author/jay-richards-and-john-zmirak/page/{}/", 3),
    ("https://stream.org/author/jonathanwittjayrichards/", "https://stream.org/author/jonathanwittjayrichards/page/{}/", 3),
    ("https://thefederalist.com/author/jay-richards/", "https://thefederalist.com/author/jay-richards/page/{}/", 5),
    ("https://thefederalist.com/author/richardsaxebriggs/", "https://thefederalist.com/author/richardsaxebriggs/page/{}/", 3),
    ("https://thefederalist.com/author/richardseckert/", "https://thefederalist.com/author/richardseckert/page/{}/", 3),
    ("https://www.nationalreview.com/author/jay-w-richards/", "https://www.nationalreview.com/author/jay-w-richards/page/{}/", 5),
    ("https://www.nationalreview.com/author/jay-richards/", "https://www.nationalreview.com/author/jay-richards/page/{}/", 5),
    ("https://crisismagazine.com/author/jay-richards", "https://crisismagazine.com/author/jay-richards/page/{}", 5),
    ("https://www.thepublicdiscourse.com/author/jay-w-richards/", "https://www.thepublicdiscourse.com/author/jay-w-richards/page/{}/", 3),
    ("https://www.dailysignal.com/author/jrichards/", "https://www.dailysignal.com/author/jrichards/page/{}/", 10),
    ("https://blog.acton.org/archives/author/jay_richards", "https://blog.acton.org/archives/author/jay_richards/page/{}", 5),
]

# ── Known individual article URLs ─────────────────────────────────────────
KNOWN_ARTICLES = [
    # Heritage Foundation
    "https://www.heritage.org/antisemitism/commentary/what-zionism-what-christian-zionism",
    "https://www.heritage.org/marriage-and-family/report/saving-america-saving-the-family-foundation-the-next-250-years",
    "https://www.heritage.org/parental-rights/commentary/how-mount-religious-liberty-challenge-childhood-vaccine-mandate",
    "https://www.heritage.org/gender/report/states-must-refuse-define-abuse-raising-child-according-his-or-her-sex",
    "https://www.heritage.org/education/report/gender-ideology-state-education-policy",
    "https://www.heritage.org/gender/commentary/rikers-rape-case-shows-female-prisoners-are-the-voiceless-victims-gender-ideology",
    "https://www.heritage.org/gender/commentary/what-gender-ideology",
    "https://www.heritage.org/gender/commentary/why-states-must-define-sex-precisely",
    "https://www.heritage.org/education/commentary/the-battle-over-parents-rights-education-just-getting-started",
    "https://www.heritage.org/gender/commentary/san-franciscos-perverse-incentive-identify-transgender",
    "https://www.heritage.org/education/commentary/floridas-parental-rights-education-bill-hits-target-gender-ideology-harms-kids",
    "https://www.heritage.org/gender/commentary/democrats-erase-women-through-budget-reconciliation",
    "https://www.heritage.org/gender/report/the-white-house-plan-make-gender-ideology-central-theme-the-american-experiment",
    "https://www.heritage.org/gender/commentary/will-lefts-gender-agenda-fall-flat-minorities-and-working-americans",
    # The Stream
    "https://stream.org/fight-the-good-fight-excerpt-open-war-whether-you-would-risk-it-or-not/",
    "https://stream.org/fight-the-good-fight-excerpt-the-toxic-witchs-brew-of-wokeness/",
    "https://stream.org/dont-miss-solar-eclipse/",
    "https://stream.org/crusade-myths/",
    "https://stream.org/fight-the-good-fight-available-now/",
    "https://stream.org/perfect-eclipses-coincidence-or-conspiracy/",
    "https://stream.org/democrats-are-trying-to-sneak-gender-dogma-into-bill-on-family-violence/",
    "https://stream.org/dont-fear-the-robots-fear-the-robot-philosophers/",
    "https://stream.org/bidens-national-mask-mandate-is-absurd-and-despotic/",
    "https://stream.org/why-covid-19-may-be-less-deadly-than-we-thought/",
    "https://stream.org/of-course-wearing-a-mask-will-reduce-your-chances-of-contracting-covid-19/",
    "https://stream.org/2022-the-year-the-conspiracy-theory-became-conspiracy-fact/",
    "https://stream.org/cleaning-up-the-right/",
    "https://stream.org/lets-make-lent-great-together/",
    "https://stream.org/jesus-fast-forty-days-forty-nights/",
    "https://stream.org/weve-mostly-abandoned-the-advent-fast-but-its-not-too-late-to-start/",
    "https://stream.org/fasting-time-restricted-eating/",
    "https://stream.org/ai-chatbot-claude-passed-my-sex-and-gender-test-im-impressed/",
    "https://stream.org/authentic-intelligence-new-ai/",
    "https://stream.org/lets-recover-ember-days-fasts/",
    "https://stream.org/how-total-solar-eclipses-point-to-purpose-and-divine-design-in-the-universe/",
    "https://stream.org/stand-together-for-freedom/",
    "https://stream.org/congresss-ban-child-sex-robots-start/",
    "https://stream.org/medical-ethicist-warns-beware-the-idolatry-of-a-covid-19-vaccine/",
    # The Federalist
    "https://thefederalist.com/2014/04/30/how-cosmos-does-religious-history-badly/",
    "https://thefederalist.com/2022/08/01/democrats-fixate-on-gay-marriage-while-the-country-crumbles/",
    "https://thefederalist.com/2022/10/14/in-the-sex-reassignment-surgery-market-business-is-booming/",
    "https://thefederalist.com/2018/06/15/heres-message-young-americans-need-hear-dont-follow-passion/",
    "https://thefederalist.com/2020/10/19/herd-immunity-to-covid-is-not-reckless-it-would-protect-the-vulnerable/",
    "https://thefederalist.com/2020/11/02/only-science-deniers-believe-in-a-national-mask-mandate/",
    "https://thefederalist.com/2022/01/03/u-s-military-uses-religious-test-against-service-members-to-enforce-vaccine-mandate/",
    "https://thefederalist.com/2023/03/30/pumping-gender-bending-drugs-into-kids-is-even-more-dangerous-than-we-thought/",
    # Discovery Institute
    "https://www.discovery.org/a/u-s-military-uses-religious-test-against-service-members-to-enforce-vaccine-mandate/",
    # Public Discourse
    "https://www.thepublicdiscourse.com/2023/03/88194/",
    "https://www.thepublicdiscourse.com/2026/01/99905/",
    # Acton
    "https://blog.acton.org/archives/125224-a-future-fit-for-conservatives.html",
    "https://blog.acton.org/archives/66648-libertarians-shouldnt-atheists.html",
    # Science and Culture
    "https://scienceandculture.com/2024/04/to-understand-the-meaning-of-a-solar-eclipse/",
]

session = requests.Session()
session.headers.update(HEADERS)


def fetch_page(url, retries=3):
    """Fetch a page with retries and exponential backoff."""
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 404:
                return None
            else:
                print(f"  HTTP {resp.status_code} for {url}")
        except requests.RequestException as e:
            print(f"  Error fetching {url}: {e}")
        time.sleep(2 ** attempt)
    return None


def extract_article_links_generic(html, base_url):
    """Extract article links from an archive page."""
    soup = BeautifulSoup(html, "lxml")
    links = set()
    domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        parsed = urlparse(href)
        # Skip pagination, author, category, tag, and home links
        if parsed.netloc != domain:
            continue
        path = parsed.path.rstrip("/")
        skip_patterns = ["/author/", "/category/", "/tag/", "/page/", "/feed"]
        if any(pat in path for pat in skip_patterns):
            continue
        if path in ("", "/"):
            continue
        # Must look like an article path (has at least 2 segments or a date pattern)
        segments = [s for s in path.split("/") if s]
        if len(segments) >= 2 or re.search(r"\d{4}/\d{2}", path):
            links.add(href)

    return links


def extract_article_text(html, url):
    """Extract article title, date, and body text from an article page."""
    soup = BeautifulSoup(html, "lxml")

    # Remove script, style, nav, footer, sidebar elements
    for tag in soup.find_all(["script", "style", "nav", "footer", "aside",
                               "iframe", "noscript"]):
        tag.decompose()

    # Try to find title
    title = ""
    for sel in ["h1.entry-title", "h1.article-title", "h1.post-title",
                "h1.page-title", "article h1", ".headline h1", "h1"]:
        el = soup.select_one(sel)
        if el:
            title = el.get_text(strip=True)
            break

    # Try to find date
    date = ""
    for sel in ["time", ".date", ".post-date", ".entry-date", ".published",
                ".article-date", '[class*="date"]']:
        el = soup.select_one(sel)
        if el:
            date = el.get_text(strip=True)
            if el.get("datetime"):
                date = el["datetime"]
            break

    # Try to find article body
    body = ""
    for sel in ["article .entry-content", ".article-body", ".post-content",
                ".entry-content", "article .content", ".article-content",
                ".story-body", ".field-body", "article", ".post-body",
                "#article-body", ".commentary__body", ".report__body"]:
        el = soup.select_one(sel)
        if el:
            # Preserve paragraph structure
            paragraphs = []
            for p in el.find_all(["p", "h2", "h3", "h4", "blockquote", "li"]):
                text = p.get_text(strip=True)
                if text:
                    if p.name in ("h2", "h3", "h4"):
                        paragraphs.append(f"\n## {text}\n")
                    elif p.name == "blockquote":
                        paragraphs.append(f'> {text}')
                    elif p.name == "li":
                        paragraphs.append(f"- {text}")
                    else:
                        paragraphs.append(text)
            body = "\n\n".join(paragraphs)
            break

    if not body:
        # Fallback: get all paragraph text
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)]
        body = "\n\n".join(paragraphs)

    return title, date, body


def safe_filename(title, url):
    """Generate a safe filename from title or URL."""
    if title:
        name = re.sub(r'[^\w\s-]', '', title)
        name = re.sub(r'[\s]+', '_', name).strip('_')
        name = name[:100]
    else:
        name = hashlib.md5(url.encode()).hexdigest()[:16]
    return name + ".txt"


def scrape_archive_pages():
    """Crawl all author archive pages to discover article URLs."""
    all_urls = set()

    for base_url, page_pattern, max_pages in AUTHOR_ARCHIVES:
        print(f"\n📄 Scraping archive: {base_url}")
        # Page 1
        html = fetch_page(base_url)
        if html:
            links = extract_article_links_generic(html, base_url)
            all_urls.update(links)
            print(f"  Page 1: found {len(links)} links")

        # Subsequent pages
        for page_num in range(2, max_pages + 1):
            page_url = page_pattern.format(page_num)
            html = fetch_page(page_url)
            if not html:
                print(f"  Page {page_num}: no more pages")
                break
            links = extract_article_links_generic(html, base_url)
            if not links:
                break
            all_urls.update(links)
            print(f"  Page {page_num}: found {len(links)} links")
            time.sleep(1)  # Be polite

    return all_urls


def scrape_heritage_staff_page():
    """Scrape Heritage Foundation staff page for article links."""
    url = "https://www.heritage.org/staff/jay-w-richards-phd"
    print(f"\n📄 Scraping Heritage staff page: {url}")
    all_links = set()

    for page in range(0, 10):
        page_url = f"{url}?page={page}" if page > 0 else url
        html = fetch_page(page_url)
        if not html:
            break
        soup = BeautifulSoup(html, "lxml")
        links = set()
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            if "heritage.org" in href and ("/commentary/" in href or "/report/" in href):
                links.add(href)
        if not links:
            break
        all_links.update(links)
        print(f"  Page {page + 1}: found {len(links)} links")
        time.sleep(1)

    return all_links


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Collect all article URLs
    print("=" * 60)
    print("STEP 1: Discovering article URLs from archives")
    print("=" * 60)

    discovered_urls = scrape_archive_pages()
    heritage_urls = scrape_heritage_staff_page()
    discovered_urls.update(heritage_urls)

    # Add known individual articles
    all_urls = discovered_urls.union(set(KNOWN_ARTICLES))
    print(f"\n✅ Total unique URLs to fetch: {len(all_urls)}")

    # Step 2: Fetch each article
    print("\n" + "=" * 60)
    print("STEP 2: Fetching article content")
    print("=" * 60)

    articles = []
    failed = []

    for i, url in enumerate(sorted(all_urls), 1):
        print(f"\n[{i}/{len(all_urls)}] {url}")
        html = fetch_page(url)
        if not html:
            failed.append(url)
            print("  ❌ Failed to fetch")
            continue

        title, date, body = extract_article_text(html, url)
        if not body or len(body) < 100:
            failed.append(url)
            print(f"  ⚠️  Body too short ({len(body)} chars), skipping")
            continue

        # Save individual file
        filename = safe_filename(title, url)
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Handle duplicate filenames
        counter = 1
        while os.path.exists(filepath):
            base, ext = os.path.splitext(filename)
            filepath = os.path.join(OUTPUT_DIR, f"{base}_{counter}{ext}")
            counter += 1

        article_text = f"TITLE: {title}\nDATE: {date}\nSOURCE: {url}\n{'=' * 60}\n\n{body}\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(article_text)

        articles.append({
            "title": title,
            "date": date,
            "url": url,
            "filepath": filepath,
            "body": body,
        })

        print(f"  ✅ Saved: {filepath} ({len(body)} chars)")
        time.sleep(0.5)  # Be polite

    # Step 3: Create combined document
    print("\n" + "=" * 60)
    print("STEP 3: Creating combined document")
    print("=" * 60)

    # Sort by date (best effort) then by title
    articles.sort(key=lambda a: (a.get("date", ""), a.get("title", "")))

    with open(COMBINED_FILE, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("THE COMPLETE COLLECTED WRITINGS OF JAY W. RICHARDS, Ph.D.\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total articles collected: {len(articles)}\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("TABLE OF CONTENTS\n")
        f.write("-" * 40 + "\n")
        for i, a in enumerate(articles, 1):
            f.write(f"{i:3d}. [{a.get('date', 'N/A')}] {a['title']}\n")
            f.write(f"     Source: {a['url']}\n")
        f.write("\n" + "=" * 80 + "\n\n")

        for i, a in enumerate(articles, 1):
            f.write("\n" + "█" * 80 + "\n")
            f.write(f"ARTICLE {i} of {len(articles)}\n")
            f.write(f"TITLE: {a['title']}\n")
            f.write(f"DATE: {a.get('date', 'N/A')}\n")
            f.write(f"SOURCE: {a['url']}\n")
            f.write("█" * 80 + "\n\n")
            f.write(a["body"])
            f.write("\n\n")

    print(f"\n✅ Combined document: {COMBINED_FILE}")
    print(f"   Articles included: {len(articles)}")
    print(f"   Failed URLs: {len(failed)}")

    # Save metadata
    with open(URLS_LOG, "w", encoding="utf-8") as f:
        json.dump({
            "total_discovered": len(all_urls),
            "total_scraped": len(articles),
            "total_failed": len(failed),
            "articles": [{"title": a["title"], "date": a["date"], "url": a["url"],
                          "file": a["filepath"]} for a in articles],
            "failed_urls": failed,
        }, f, indent=2)

    print(f"\n📊 Summary saved to {URLS_LOG}")
    print("\nDone! 🎉")


if __name__ == "__main__":
    main()
