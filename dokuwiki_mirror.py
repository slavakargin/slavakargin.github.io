#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mirror the BU DocuWiki namespace people:kargin into static HTML pages
for GitHub Pages hosting (slavakargin.github.io).

- Crawls the namespace index (…/people/kargin/start?do=index)
- For each page URL under /p/people/kargin/, fetches clean HTML:
    1) prefer ?do=export_xhtml (if enabled)
    2) else fetch normal page and extract main content
- Downloads linked media (CV PDFs, images under lib/exe/fetch.php, etc.)
- Rewrites internal links to relative links
- Wraps content with a simple HTML template (MathJax + minimal CSS)
"""

import os, re, hashlib, urllib.parse, sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from email.utils import formatdate


BASE = "https://www2.math.binghamton.edu"
NS_ROOT = "/p/people/kargin"
SITEMAP_URL = f"{BASE}{NS_ROOT}/start?do=index"
OUTDIR = Path(".")  # write into repo root
ASSET_DIR = OUTDIR / "assets"
HEAD_HTML = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<style>
:root{{--max:900px}}
body{{font:16px/1.55 system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, Arial; margin:0; padding:0;}}
header,main,footer{{max-width:var(--max); margin:0 auto; padding:1rem;}}
header h1{{margin:.2rem 0 0 0; font-size:1.35rem;}}
nav a{{margin-right:.8rem}}
main{{padding-top:0.25rem}}
main img{{max-width:100%; height:auto}}
code,pre{{font-family:ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace}}
hr{{border:none; border-top:1px solid #ddd; margin:1.5rem 0}}
small.muted{{color:#666}}
</style>
<script>
window.MathJax={{tex:{{inlineMath:[['$','$'],['\\\\(','\\\\)']]}}}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
</head><body>
<header>
  <h1><a href="/index.html" style="text-decoration:none;color:inherit;">Vladislav Kargin</a></h1>
  <nav>
    <a href="/index.html">Home</a>
    <a href="/kargin_publications/index.html">Publications</a>
    <a href="/letterinfo/index.html">Letters</a>
  </nav>
</header>
<main>
"""
FOOT_HTML = """
<hr>
<p class="muted"><small class="muted">
Mirrored from the Binghamton University Math &amp; Stats DocuWiki (people:kargin).
Original pages © their authors; wiki license CC BY-NC-SA 3.0.
Source: <a href="{source}">{source}</a>
</small></p>
</main>
<footer><p><small>Last mirrored: {stamp}</small></p></footer>
</body></html>
"""

session = requests.Session()
session.headers.update({"User-Agent":"Mozilla/5.0 (mirroring script)"})


def normalize_external_url(u: str) -> str:
    pu = urllib.parse.urlsplit(u)
    host = pu.netloc.lower()
    # Fix legacy domains
    if host == "www-history.mcs.st-andrews.ac.uk":
        host = "mathshistory.st-andrews.ac.uk"
    # Prefer HTTPS when possible
    scheme = "https" if pu.scheme in ("", "http") else pu.scheme
    return urllib.parse.urlunsplit((scheme, host, pu.path, pu.query, pu.fragment))

def get(url, **kw):
    r = session.get(url, timeout=30, **kw)
    r.raise_for_status()
    return r

def safe_slug(url_path: str) -> str:
    # /p/people/kargin/math457_fall2025 -> math457_fall2025
    name = url_path.rstrip("/").split("/")[-1]
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name)

def list_namespace_pages():
    print(f"Fetching sitemap: {SITEMAP_URL}")
    html = get(SITEMAP_URL).text
    soup = BeautifulSoup(html, "lxml")
    pages = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # Capture only pages under /p/people/kargin/
        if href.startswith(NS_ROOT) or href.startswith(f"{BASE}{NS_ROOT}"):
            full = urllib.parse.urljoin(BASE, href)
            # Normalize by stripping ?… params
            full = full.split("?")[0]
            # Only actual pages, not the /start?do=index itself
            if "/start" in full and "do=index" in href:
                continue
            pages.add(full)
    # Ensure the front page is first
    pages = {f"{BASE}{NS_ROOT}/start"} | pages
    return sorted(pages)

def fetch_clean_html(page_url: str) -> str:
    # Prefer DocuWiki exporter (if enabled)
    export_url = f"{page_url}?do=export_xhtml"
    try:
        r = get(export_url)
        text = r.text.strip()
        # exporter often returns a full minimal HTML; that's perfect
        if "<html" in text.lower() or "<div" in text.lower():
            return text
    except Exception:
        pass

    # Fallback: grab normal page and extract content area
    r = get(page_url)
    soup = BeautifulSoup(r.text, "lxml")
    # Try common content containers
    candidates = [
        "#dokuwiki__content",    # default DokuWiki layout
        "div.page",              # older Dokuwiki skins
        "#content", "article"
    ]
    content = None
    for sel in candidates:
        content = soup.select_one(sel)
        if content: break
    if not content:
        # fallback to body
        content = soup.body or soup
    # Return inner HTML
    return str(content)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def save_page(out_dir: Path, title: str, body_html: str, source_url: str):
    ensure_dir(out_dir)
    html = HEAD_HTML.format(title=title) + body_html + FOOT_HTML.format(source=source_url, stamp=formatdate(usegmt=True))
    (out_dir / "index.html").write_text(html, encoding="utf-8")

def download_asset(url: str) -> str:
    """Download to assets/ and return relative path; on failure, return normalized external URL."""
    ensure_dir(ASSET_DIR)
    # normalize first in case the caller passes an old-domain HTTP link
    url = normalize_external_url(url)
    try:
        h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
        parsed = urllib.parse.urlparse(url)
        ext = Path(parsed.path).suffix or ".bin"
        fn = ASSET_DIR / f"{h}{ext}"
        if not fn.exists():
            print(f"  asset: {url} -> {fn}")
            with get(url, stream=True) as r:
                r.raise_for_status()
                with open(fn, "wb") as f:
                    for chunk in r.iter_content(8192):
                        f.write(chunk)
        return "/" + str(fn.relative_to(OUTDIR)).replace(os.sep, "/")
    except Exception as e:
        print(f"  [warn] asset fetch failed: {url} ({e}); linking externally")
        return normalize_external_url(url)

def rewrite_links(html: str, page_url: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    def normalize_or_same(u: str) -> str:
        try:
            return normalize_external_url(u)
        except Exception:
            return u

    # --- anchors (<a href=...>) ---
    for a in soup.find_all("a"):
        href = a.get("href")
        if not href:
            continue  # no href to fix

        # Keep pure in-page anchors like "#section"
        if href.startswith("#"):
            continue

        try:
            href_abs = urllib.parse.urljoin(page_url, href)
        except Exception:
            # If even urljoin fails, leave as-is
            a["href"] = href
            continue

        # Internal page under your namespace
        if href_abs.startswith(f"{BASE}{NS_ROOT}/"):
            slug = safe_slug(urllib.parse.urlparse(href_abs).path)
            a["href"] = "/" if slug == "start" else f"/{slug}/"
            continue

        # Dokuwiki media fetches (may wrap external URLs)
        if "/lib/exe/fetch.php" in href_abs:
            qs = urllib.parse.parse_qs(urllib.parse.urlsplit(href_abs).query)
            media = qs.get("media", [None])[0]
            if media and media.startswith(("http://", "https://")):
                a["href"] = normalize_or_same(media)
            else:
                a["href"] = download_asset(href_abs)
            continue

        # Everything else: external → normalize to https/new host
        a["href"] = normalize_or_same(href_abs)

    # --- src/href on assets (img/link/script) ---
    def fix_src(tag: str, attr: str):
        for t in soup.find_all(tag):
            url = t.get(attr)
            if not url:
                continue
            try:
                src_abs = urllib.parse.urljoin(page_url, url)
            except Exception:
                # leave as-is if join breaks
                continue

            if src_abs.startswith(f"{BASE}/lib/exe/"):
                qs = urllib.parse.parse_qs(urllib.parse.urlsplit(src_abs).query)
                media = qs.get("media", [None])[0]
                if media and media.startswith(("http://", "https://")):
                    t[attr] = normalize_or_same(media)
                else:
                    t[attr] = download_asset(src_abs)

            elif src_abs.startswith(f"{BASE}{NS_ROOT}/"):
                t[attr] = download_asset(src_abs)

            else:
                t[attr] = normalize_or_same(src_abs)

    fix_src("img", "src")
    fix_src("link", "href")
    fix_src("script", "src")

    return str(soup)


def title_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    h1 = soup.find(["h1","h2","h3"])
    return h1.get_text(strip=True) if h1 else "Page"

def main():
    pages = list_namespace_pages()
    print(f"Found {len(pages)} pages under {NS_ROOT}")
    for url in pages:
        print(f"\n=== {url}")
        raw = fetch_clean_html(url)
        cleaned = rewrite_links(raw, url)
        title = title_from_html(cleaned)
        slug = safe_slug(urllib.parse.urlparse(url).path)
        outdir = OUTDIR / ("" if slug=="start" else slug)
        save_page(outdir, title, cleaned, url)
    print("\nDone. Commit & push to publish on GitHub Pages.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
