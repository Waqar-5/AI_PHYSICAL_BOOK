import asyncio
import time
import re
from typing import List, Set, Dict, Optional
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

from .config import Config


class URLCrawler:
    """
    Crawler specifically designed for Docusaurus sites that extracts URLs and content
    """

    def __init__(self, config: Config):
        self.config = config
        self.session = self._create_session()
        self.visited_urls: Set[str] = set()
        self.url_content_map: Dict[str, str] = {}

        # Configure logging
        logging.basicConfig(level=getattr(logging, self.config.log_level))
        self.logger = logging.getLogger(__name__)

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry strategy and headers"""
        session = requests.Session()

        # Set up retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set headers
        session.headers.update({
            'User-Agent': self.config.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })

        return session

    def _is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid for crawling"""
        try:
            parsed = urlparse(url)
            # Only crawl URLs from the same domain
            base_domain = urlparse(self.config.base_url).netloc
            return (
                parsed.netloc == base_domain
                and not url.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe'))
                and not any(skip in url for skip in ['/api/', '/assets/', '/static/'])
            )
        except Exception:
            return False

    def _normalize_url(self, url: str) -> str:
        """Normalize URL to avoid duplicates"""
        parsed = urlparse(url)
        # Remove fragments and normalize
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def _extract_urls_from_page(self, url: str, html_content: str) -> List[str]:
        """Extract all valid URLs from a page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        urls = []

        # Find all links
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            normalized_url = self._normalize_url(full_url)

            if self._is_valid_url(normalized_url):
                urls.append(normalized_url)

        return urls

    def _extract_content_from_page(self, html_content: str) -> str:
        """Extract clean text content from HTML page, specifically for Docusaurus"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
            script.decompose()

        # Try to find main content area (Docusaurus specific selectors)
        content_selectors = [
            'article',  # Common content container
            '.main-wrapper',  # Docusaurus main content
            '.container',  # Container for content
            '.theme-doc-markdown',  # Docusaurus markdown content
            '.markdown',  # Markdown content
            'main',  # Main content area
            '.doc-content',  # Documentation content
            '.docs-content',  # Alternative documentation content
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        if content_element:
            # Remove sidebar and navigation elements that might be inside the content
            for nav in content_element.select('.sidebar, .navigation, .menu'):
                nav.decompose()

            text = content_element.get_text(separator=' ')
        else:
            # Fallback to body content
            body = soup.body
            if body:
                text = body.get_text(separator=' ')
            else:
                text = soup.get_text(separator=' ')

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text

    def crawl_single_url(self, url: str) -> Optional[str]:
        """Crawl a single URL and return its content"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            content = self._extract_content_from_page(response.text)

            # Add URL and content to maps
            self.visited_urls.add(url)
            self.url_content_map[url] = content

            self.logger.info(f"Crawled URL: {url}")
            return content

        except Exception as e:
            self.logger.error(f"Error crawling {url}: {str(e)}")
            return None

    def crawl_urls(self, start_urls: List[str], max_pages: Optional[int] = None) -> Dict[str, str]:
        """Crawl multiple URLs breadth-first"""
        urls_to_visit = set(start_urls)
        pages_crawled = 0

        while urls_to_visit and (max_pages is None or pages_crawled < max_pages):
            current_url = urls_to_visit.pop()

            if current_url in self.visited_urls:
                continue

            content = self.crawl_single_url(current_url)

            if content:
                # Extract more URLs from the current page
                try:
                    response = self.session.get(current_url, timeout=10)
                    new_urls = self._extract_urls_from_page(current_url, response.text)

                    for new_url in new_urls:
                        if new_url not in self.visited_urls and len(self.visited_urls) < (max_pages or float('inf')):
                            urls_to_visit.add(new_url)

                except Exception as e:
                    self.logger.error(f"Error extracting URLs from {current_url}: {str(e)}")

            pages_crawled += 1
            time.sleep(self.config.request_delay)  # Be respectful to the server

        return self.url_content_map

    def get_all_urls_from_sitemap(self) -> List[str]:
        """Try to get URLs from sitemap if available"""
        sitemap_url = urljoin(self.config.base_url, '/sitemap.xml')

        try:
            response = self.session.get(sitemap_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'xml')  # Use xml parser for sitemap
            loc_tags = soup.find_all('loc')

            urls = []
            for loc in loc_tags:
                url = loc.text.strip()
                if self._is_valid_url(url):
                    urls.append(url)

            return urls

        except Exception as e:
            self.logger.warning(f"Could not fetch sitemap: {str(e)}")
            # Fallback to getting URLs from main page
            try:
                response = self.session.get(self.config.base_url, timeout=10)
                response.raise_for_status()
                urls = self._extract_urls_from_page(self.config.base_url, response.text)
                return urls
            except Exception as e:
                self.logger.error(f"Error getting URLs from main page: {str(e)}")
                return [self.config.base_url]