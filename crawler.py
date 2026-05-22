import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import HEADERS
from db import get_sources, insert_article_link, get_pending_articles, update_article_content


class CrawlError(Exception):
    pass


def fetch_html(url, timeout=12):
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        raise CrawlError(f"Lỗi khi tải {url}: {exc}") from exc


def normalize_url(base_url, link):
    if not link:
        return None
    normalized = urljoin(base_url, link.strip())
    parsed = urlparse(normalized)
    if parsed.scheme not in ("http", "https"):
        return None
    return normalized.split('#')[0].rstrip('/')


def extract_links(url, html):
    soup = BeautifulSoup(html, "html.parser")
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    anchors = []

    if "vnexpress.net" in domain:
        anchors = soup.select("h3.title-news a, h2.title-news a, article.item-news a, a.ratio-thumb")
    elif "tuoitre.vn" in domain:
        anchors = soup.select("h3.title-news a, .news-item__content a, .box-news a")
    else:
        anchors = soup.select("article a, h3 a, h2 a, .title a")

    links = []
    for a in anchors:
        href = a.get("href")
        title = a.get_text(strip=True)
        if not title or not href:
            continue
        full_url = normalize_url(url, href)
        if not full_url:
            continue
        if urlparse(full_url).netloc != parsed.netloc:
            continue
        if full_url in [item["url"] for item in links]:
            continue
        links.append({"title": title, "url": full_url})
        if len(links) >= 40:
            break

    if not links:
        # fallback generic anchor scan
        for a in soup.select("a[href]"):
            href = a.get("href")
            title = a.get_text(strip=True)
            full_url = normalize_url(url, href)
            if not full_url or parsed.netloc not in full_url:
                continue
            if len(title) < 10:
                continue
            if full_url in [item["url"] for item in links]:
                continue
            links.append({"title": title, "url": full_url})
            if len(links) >= 40:
                break

    return links


def extract_article_detail(url, html):
    soup = BeautifulSoup(html, "html.parser")
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    title = None
    summary = None
    content = None

    if "vnexpress.net" in domain:
        title = soup.select_one("h1.title_news_detail, h1.title-detail")
        summary = soup.select_one(".description, .short_intro")
        content_block = soup.select_one("article.fck_detail, .fck_detail")
    elif "tuoitre.vn" in domain:
        title = soup.select_one("h1.title, .title-news")
        summary = soup.select_one(".sapo, .description")
        content_block = soup.select_one(".fck_detail, .area_detail")
    else:
        title = soup.select_one("h1, h2")
        summary = soup.select_one(".summary, .sapo, p")
        content_block = soup.select_one("article, .content, .main-content")

    title_text = title.get_text(strip=True) if title else None
    summary_text = summary.get_text(strip=True) if summary else None

    if content_block:
        paragraphs = [p.get_text(strip=True) for p in content_block.select("p") if p.get_text(strip=True)]
        content_text = "\n\n".join(paragraphs)
    else:
        paragraphs = [p.get_text(strip=True) for p in soup.select("p") if p.get_text(strip=True)]
        content_text = "\n\n".join(paragraphs[:20])

    if not content_text:
        raise CrawlError(f"Không tìm được nội dung cho {url}")

    return {
        "title": title_text or "(Không có tiêu đề)",
        "summary": summary_text or content_text[:250],
        "content": content_text,
    }


def crawl_source(source):
    try:
        html = fetch_html(source["url"])
    except CrawlError as exc:
        print(f"[ERROR] Không tải được nguồn {source['source_name']}: {exc}")
        return 0

    links = extract_links(source["url"], html)
    saved_count = 0
    for item in links:
        saved = insert_article_link(source["id"], source["category_id"], item["title"], item["url"])
        if saved:
            saved_count += 1
    return saved_count


def crawl_all_sources():
    sources = get_sources()
    total = 0
    for source in sources:
        count = crawl_source(source)
        print(f"[{source['source_name']}] Thêm được {count} link mới")
        total += count
        time.sleep(2)
    print(f"Tổng link mới được lưu: {total}")
    return total


def crawl_pending_articles(limit=20):
    pending = get_pending_articles(limit=limit)
    updated = 0
    for item in pending:
        try:
            html = fetch_html(item["url"])
            article = extract_article_detail(item["url"], html)
            update_article_content(item["id"], article["summary"], article["content"])
            updated += 1
            print(f"Cập nhật nội dung cho bài #{item['id']}")
        except CrawlError as exc:
            print(f"[ERROR] Không lấy nội dung {item['url']}: {exc}")
    print(f"Tổng bài viết đã cập nhật: {updated}")
    return updated
