from categorization import init_db, add_url, list_urls, delete_url

# Step 1: Initialize DB
init_db()

# Step 2: Clear old URLs
for row in list_urls():
    delete_url(row[1])

# Step 3: Popular URLs to ALLOW
allow_urls = [
    "http://www.google.com",
    "http://www.youtube.com",
    "http://www.facebook.com",
    "http://www.wikipedia.org",
    "http://www.twitter.com",
    "http://www.instagram.com",
    "http://www.linkedin.com",
    "http://www.reddit.com",
    "http://www.amazon.com",
    "http://www.netflix.com",
    "http://www.apple.com",
    "http://www.microsoft.com",
    "http://www.stackoverflow.com",
    "http://www.bbc.com",
    "http://www.nytimes.com"
]

# Step 4: Fake/Malicious-looking URLs to BLOCK
block_urls = [
    "http://malicious-site1.com",
    "http://phishing-site2.com",
    "http://virus-download3.com",
    "http://hacker-portal4.com",
    "http://dangerous-content5.com",
    "http://malware-zone6.com",
    "http://ransomware7.com",
    "http://spyware8.com",
    "http://darkweb-access9.com",
    "http://fake-login10.com",
    "http://banned-content11.com",
    "http://suspicious-url12.com",
    "http://illegal-content13.com",
    "http://botnet-control14.com",
    "http://trojan-upload15.com"
]

# Step 5: Add to DB
for url in allow_urls:
    add_url(url, "ALLOW")

for url in block_urls:
    add_url(url, "BLOCK")

print("proxy_db.sqlite updated with 15 ALLOW and 15 BLOCK URLs.")
