from crawler import crawl_all_sources, crawl_pending_articles
from db import count_articles, list_articles

print("Starting test crawl...")
print("\n=== Phase 1: Crawl all sources ===")
links = crawl_all_sources()
print(f"\nTotal links saved: {links}")

print("\n=== Phase 2: Crawl pending articles ===")
updated = crawl_pending_articles(limit=5)
print(f"\nTotal articles updated: {updated}")

print("\n=== Verify database ===")
total = count_articles()
print(f"Total articles: {total}")
if total > 0:
    articles = list_articles(1, 3)
    for i, a in enumerate(articles, 1):
        status = "New" if a["status"] == 0 else "Complete"
        print(f"{i}. [{status}] {a['title'][:60]}...")
