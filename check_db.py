from db import count_articles, list_articles, get_sources, get_categories

print('='*50)
print('DATABASE CHECK')
print('='*50)

categories = get_categories()
print(f'\n✓ Categories: {len(categories)} items')

sources = get_sources()
print(f'✓ Sources: {len(sources)} items')
for s in sources[:3]:
    print(f'  - {s["source_name"]}')

articles = count_articles()
print(f'\n✓ Total articles in DB: {articles}')

if articles > 0:
    articles_page1 = list_articles(1, 5)
    print(f'\n✓ First 5 articles:')
    for i, a in enumerate(articles_page1, 1):
        status = 'New' if a['status'] == 0 else 'Content Fetched'
        print(f'  {i}. [{status}] {a["title"][:50]}...')
        
print('\n✓ Database is working correctly!')
