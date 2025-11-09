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
import shutil

import re, shutil
from pathlib import Path

CV_CANDIDATE_LOCAL = None

# Much broader: match any filename that includes "cv" or "vitae" before ".pdf"
CV_NAME_RX = re.compile(r'(?i)(?:^|[/:])(?=[^/]*kargin)(?=[^/]*cv)[^/]*\.pdf$')

def remember_cv_candidate(local_web_path: str, media_url: str, anchor_text: str):
    """
    local_web_path: '/bu/assets/abcd1234.pdf' returned by download_asset(...)
    media_url: the 'media=' query value (may be 'people:kargin:cv_2024.pdf', etc.)
    anchor_text: link text (e.g., 'CV (PDF)', 'Curriculum Vitae', etc.)
    """
    global CV_CANDIDATE_LOCAL

    t = (anchor_text or "").lower()
    m = (media_url or "").lower()

    looks_like_cv = ("cv" in t) or ("vitae" in t) or CV_NAME_RX.search(m or "")
    if not looks_like_cv:
        return

    # Convert site path -> local file path
    rel = local_web_path.lstrip("/")          # 'bu/assets/abcd.pdf'
    p = Path(rel)

    # If you’re using a staging dir (bu_next), look there too
    if not p.exists() and rel.startswith("bu/"):
        parts = Path(rel).parts               # ('bu','assets','abcd.pdf', ...)
        alt = Path("bu_next").joinpath(*parts[1:])
        if alt.exists():
            p = alt

    if p.exists():
        CV_CANDIDATE_LOCAL = p
        print(f"  [cv] candidate matched: {p}")



BASE = "https://www2.math.binghamton.edu"
# put this near the top, after the constants
BASE_PREFIX = "/bu"   # "" means root; "/bu" means mirror lives at /bu/
NS_ROOT = "/p/people/kargin"
SITEMAP_URL = f"{BASE}{NS_ROOT}/start?do=index"
OUTDIR = Path(BASE_PREFIX.strip("/")) if BASE_PREFIX else Path(".")
ASSET_DIR = OUTDIR / "assets"
DEFAULT_TITLE = "Vladislav Kargin — Associate Professor, Mathematics & Statistics, Binghamton University"
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
  <a href="{base}/">Home</a>
  <a href="{base}/kargin_publications/">Publications</a>
  <a href="{base}/letterinfo/">Letters</a>
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
    html = (
        HEAD_HTML.replace("{title}", title).replace("{base}", BASE_PREFIX)
        + body_html
        + FOOT_HTML.replace("{source}", source_url).replace("{stamp}", formatdate(usegmt=True))
    )
    path = out_dir / "index.html"
    path.write_text(html, encoding="utf-8")
    print(f"  wrote {path}")

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
        rel = str(fn.relative_to(OUTDIR)).replace(os.sep, "/")
        return f"{BASE_PREFIX}/{rel}"
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
            a["href"] = f"{BASE_PREFIX}/" if slug == "start" else f"{BASE_PREFIX}/{slug}/"
            continue
        
        # Dokuwiki media fetches (may wrap external URLs)
        elif "/lib/exe/fetch.php" in href_abs:
            qs = urllib.parse.parse_qs(urllib.parse.urlsplit(href_abs).query)
            media = qs.get("media", [None])[0]

            # If fetch.php wraps an external URL, just link out
            if media and media.startswith(("http://", "https://")):
                a["href"] = normalize_or_same(media)
            else:
                 # Internal BU media → download and link locally
                local_web = download_asset(href_abs)     # e.g. '/bu/assets/abcd.pdf'
                a["href"] = local_web
                # If this looks like your CV, remember it for /cv.pdf syncing
                remember_cv_candidate(local_web, media, a.get_text())
            continue

        '''
        # Dokuwiki media fetches (may wrap external URLs)
        if "/lib/exe/fetch.php" in href_abs:
            qs = urllib.parse.parse_qs(urllib.parse.urlsplit(href_abs).query)
            media = qs.get("media", [None])[0]
            if media and media.startswith(("http://", "https://")):
                a["href"] = normalize_or_same(media)
            else:
                a["href"] = download_asset(href_abs)
            continue
        '''
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
    h = soup.find(["h1","h2","h3","title"])
    t = h.get_text(strip=True) if h else ""
    return t or DEFAULT_TITLE


def sync_root_cv():
    assets_dir = OUTDIR / "assets"   # OUTDIR is 'bu' when BASE_PREFIX='/bu'
    if not assets_dir.exists():
        return
    pdfs = sorted(assets_dir.glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True)
    if pdfs:
        shutil.copy2(pdfs[0], Path("cv.pdf"))
        print(f"  synced cv.pdf from {pdfs[0].name}")

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
    # After mirroring, sync cv.pdf at repo root if we detected a CV candidate
    if CV_CANDIDATE_LOCAL and Path(CV_CANDIDATE_LOCAL).exists():
        shutil.copy2(CV_CANDIDATE_LOCAL, Path("cv.pdf"))
        print(f"  synced cv.pdf from {CV_CANDIDATE_LOCAL}")
    else:
        print("  [warn] no CV candidate found; leaving cv.pdf unchanged.")
    #sync_root_cv()
    print("\nDone. Commit & push to publish on GitHub Pages.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
