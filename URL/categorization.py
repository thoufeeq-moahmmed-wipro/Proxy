# categorization.py

class URLCategorization:
    def __init__(self):
        self.allowed_urls = {
            "google.com", "example.com", "wikipedia.org", "netflix.com",
            "github.com", "stackoverflow.com", "reddit.com", "linkedin.com",
            "medium.com", "python.org", "djangoproject.com", "flask.palletsprojects.com",
            "microsoft.com", "apple.com", "mozilla.org"
        }

        self.blocked_urls = {
            "ddos-attack.net", "hacking-tools.com", "malware-download.com",
            "phishing-site.com", "fakebank.com", "virus-downloads.com",
            "trojan-hub.com", "spyware-attack.com", "ransomware-site.com",
            "fraudulent-site.com", "illegal-downloads.com", "pirated-software.com"
        }

    def is_allowed(self, url):
        """Check if the given URL is allowed."""
        return any(url.endswith(allowed) for allowed in self.allowed_urls)

    def is_blocked(self, url):
        """Check if the given URL is blocked."""
        return any(url.endswith(blocked) for blocked in self.blocked_urls)
