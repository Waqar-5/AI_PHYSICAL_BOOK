import requests
from xml.etree import ElementTree as ET
from typing import List
import logging

logger = logging.getLogger(__name__)

def parse_sitemap(sitemap_url: str) -> List[str]:
    """
    Parse a sitemap.xml file and extract all URLs

    Args:
        sitemap_url: URL to the sitemap.xml file

    Returns:
        List of URLs extracted from the sitemap
    """
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML content
        root = ET.fromstring(response.content)

        # Define the namespace used in sitemaps
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        urls = []
        # Find all <loc> elements (URL locations)
        for url_element in root.findall('.//sitemap:url/sitemap:loc', namespace):
            if url_element is not None and url_element.text:
                urls.append(url_element.text.strip())

        logger.info(f"Found {len(urls)} URLs in sitemap")
        return urls

    except Exception as e:
        logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
        raise e

def filter_urls_by_pattern(urls: List[str], include_patterns: List[str] = None, exclude_patterns: List[str] = None) -> List[str]:
    """
    Filter URLs based on include/exclude patterns

    Args:
        urls: List of URLs to filter
        include_patterns: List of patterns that URLs must contain (if provided)
        exclude_patterns: List of patterns that URLs must not contain (if provided)

    Returns:
        Filtered list of URLs
    """
    filtered_urls = urls

    if include_patterns:
        filtered_urls = [
            url for url in filtered_urls
            if any(pattern in url for pattern in include_patterns)
        ]

    if exclude_patterns:
        filtered_urls = [
            url for url in filtered_urls
            if not any(pattern in url for pattern in exclude_patterns)
        ]

    return filtered_urls