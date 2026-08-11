def analyze_performance(raw_data):
    """تحليل بيانات الـ HTTP المحصّلة وتحديد Score والمشاكل"""
    headers = raw_data["headers"]
    latency = raw_data["latency"]
    url = raw_data["final_url"]
    
    # فحص التضغط
    encoding = headers.get('Content-Encoding', '').lower()
    has_compression = 'gzip' in encoding or 'br' in encoding or 'deflate' in encoding
    
    # فحص التخزين المؤقت
    cache_control = headers.get('Cache-Control', '').lower()
    has_caching = 'max-age' in cache_control or 'public' in cache_control or 's-maxage' in cache_control
    
    # فحص التشفير
    is_https = url.startswith("https://")
    
    # حساب النتيجة
    score = 100
    issues = []
    
    if latency > 1.2:
        score -= 25
        issues.append(f"Slow initial server response time ({latency}s). Target < 0.8s.")
    if not has_compression:
        score -= 25
        issues.append("HTTP compression (Gzip/Brotli) is disabled on server responses.")
    if not has_caching:
        score -= 25
        issues.append("Browser caching headers (Cache-Control) are missing.")
    if not is_https:
        score -= 25
        issues.append("Insecure connection (HTTPS/SSL encryption is missing).")
        
    return {
        "final_url": url,
        "status_code": raw_data["status_code"],
        "latency": f"{latency}s",
        "score": f"{max(score, 10)}%",
        "has_compression": has_compression,
        "has_caching": has_caching,
        "is_https": is_https,
        "issues": issues
    }
