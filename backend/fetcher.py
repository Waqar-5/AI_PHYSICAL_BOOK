import requests
from urllib.parse import urlparse
import ipaddress
from typing import Tuple, Dict
from config import REQUEST_TIMEOUT, MAX_RETRIES
import time
import random

class URLFetcher:
    """
    Responsible for fetching web content with security measures
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'URL-Ingestion-Pipeline/1.0'
        })

    def _is_private_ip(self, hostname: str) -> bool:
        """
        Check if hostname resolves to a private IP address to prevent SSRF
        """
        try:
            # Check if hostname is an IP address
            ip = ipaddress.ip_address(hostname)
            return ip.is_private or ip.is_loopback
        except ValueError:
            # Hostname is not an IP, skip private IP check
            return False

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format and security requirements
        """
        try:
            parsed = urlparse(url)

            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False

            # Check if hostname is private IP (basic check)
            if self._is_private_ip(parsed.hostname):
                return False

            # Basic check for localhost
            if parsed.hostname in ['localhost', '127.0.0.1', '::1']:
                return False

            return True
        except Exception:
            return False

    def fetch_content(self, url: str) -> Tuple[str, Dict]:
        """
        Fetch content from URL and return content and metadata

        Args:
            url: The URL to fetch

        Returns:
            Tuple of (content, metadata) where metadata includes:
            - status_code: HTTP status code
            - content_type: Content type of the response
            - title: Page title if available
            - description: Meta description if available
        """
        # Validate URL first
        if not self._validate_url(url):
            raise ValueError(f"Invalid or insecure URL: {url}")

        # Implement retry logic with exponential backoff
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(
                    url,
                    timeout=REQUEST_TIMEOUT,
                    allow_redirects=True
                )

                # Check if request was successful
                response.raise_for_status()

                # Check content type
                content_type = response.headers.get('content-type', '').lower()
                if not any(ct in content_type for ct in ['text/html', 'application/json', 'text/plain']):
                    raise ValueError(f"Unsupported content type: {content_type}")

                # Extract basic metadata from content
                content = response.text
                metadata = {
                    'status_code': response.status_code,
                    'content_type': content_type,
                    'title': self._extract_title(content),
                    'description': self._extract_description(content),
                    'source_domain': urlparse(url).netloc
                }

                return content, metadata

            except requests.exceptions.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise e

                # Exponential backoff: wait 1s, 2s, 4s, etc.
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)

        raise Exception(f"Failed to fetch URL after {MAX_RETRIES} attempts")

    def _extract_title(self, content: str) -> str:
        """
        Extract title from HTML content (basic implementation)
        """
        try:
            start = content.lower().find('<title>')
            if start != -1:
                start += 7  # length of '<title>'
                end = content.lower().find('</title>', start)
                if end != -1:
                    return content[start:end].strip()
        except:
            pass
        return ""

    def _extract_description(self, content: str) -> str:
        """
        Extract meta description from HTML content (basic implementation)
        """
        try:
            # Look for meta description tag
            desc_start = content.lower().find('<meta')
            while desc_start != -1:
                desc_end = content.lower().find('>', desc_start)
                if desc_end != -1:
                    meta_tag = content[desc_start:desc_end+1]
                    if 'name="description"' in meta_tag.lower() or 'property="description"' in meta_tag.lower():
                        content_pos = meta_tag.lower().find('content="')
                        if content_pos != -1:
                            content_start = content_pos + 9  # length of 'content="'
                            remaining = meta_tag[content_start:]
                            content_end = remaining.find('"')
                            if content_end != -1:
                                return remaining[:content_end]

                # Look for next meta tag
                desc_start = content.lower().find('<meta', desc_end)
        except:
            pass
        return ""