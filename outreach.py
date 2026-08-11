import asyncio
import aiohttp
import time
import sqlite3
from urllib.parse import urlparse

# إعداد قاعدة البيانات لتخزين النتائج
def init_db():
    conn = sqlite3.connect("growth_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audits (
            domain TEXT PRIMARY KEY,
            latency REAL,
            status_code INTEGER,
            has_cache INTEGER,
            score INTEGER,
            audit_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# دالة فحص موقع واحد بشكل غير متزامن (Async)
async def audit_site(session, url, app_base_url):
    formatted_url = url if url.startswith("http") else f"https://{url}"
    domain = urlparse(formatted_url).netloc or url
    
    start_time = time.time()
    try:
        async with session.get(formatted_url, timeout=5, allow_redirects=True) as response:
            latency = round(time.time() - start_time, 2)
            status_code = response.status
            headers = response.headers
            
            cache_header = headers.get("Cache-Control", "") or headers.get("cache-control", "")
            has_cache = 1 if cache_header else 0
            
            # احتساب التقييم
            score = 100
            if latency > 1.0: score -= 25
            if not has_cache: score -= 25
            if status_code != 200: score -= 50
            score = max(score, 0)
            
            audit_url = f"{app_base_url}/?target={formatted_url}"
            
            return (domain, latency, status_code, has_cache, score, audit_url)
    except Exception:
        return (domain, 0.0, 500, 0, 0, f"{app_base_url}/?target={formatted_url}")

# محرك الفحص الجماعي (Mass Scanner)
async def process_urls(urls, app_base_url, max_concurrent=50):
    connector = aiohttp.TCPConnector(limit=max_concurrent, ssl=False)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GrowthEngine/2.0"}
    
    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        tasks = [audit_site(session, url, app_base_url) for url in urls]
        results = await asyncio.gather(*tasks)
        
    # حفظ النتائج في قاعدة البيانات
    conn = sqlite3.connect("growth_data.db")
    cursor = conn.cursor()
    cursor.executemany('''
        INSERT OR REPLACE INTO audits (domain, latency, status_code, has_cache, score, audit_url)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', results)
    conn.commit()
    conn.close()
    return len(results)

if __name__ == "__main__":
    init_db()
    
    # رابط تطويق التطبيق الخاص بك على Streamlit
    APP_URL = "https://growthengine-9btijzf8jcjty9hfqufsbu.streamlit.app"
    
    # قائمة نطاقات تجريبية للفحص الضخم
    target_domains = [
        "https://www.gymshark.com",
        "https://www.woocommerce.com",
        "https://www.allbirds.com",
        "https://www.github.com",
        "https://www.shopify.com"
    ]
    
    print("🚀 Starting High-Concurrency Outreach Engine...")
    asyncio.run(process_urls(target_domains, APP_URL))
    print("✅ Mass Scanning & Database Sync Completed.")
