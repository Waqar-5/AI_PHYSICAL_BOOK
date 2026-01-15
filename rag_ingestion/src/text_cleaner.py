import re
from typing import List, Dict
import logging
from .config import Config


class TextCleaner:
    """
    Text cleaning and preprocessing pipeline for book content
    """

    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def clean_text(self, text: str) -> str:
        """Clean raw text by removing noise and standardizing format"""
        if not text:
            return ""

        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters that might interfere with processing
        # Keep letters, numbers, punctuation, and common symbols
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\'\"\/\@\#\$\%\&\*\+\=\<\>\|]', ' ', text)

        # Remove extra spaces again after cleaning
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def extract_structured_content(self, raw_html: str, url: str = "") -> Dict[str, str]:
        """
        Extract structured content from raw HTML, preserving document hierarchy
        """
        # This would be implemented based on the specific HTML structure
        # For now, we'll return a basic structure
        return {
            "url": url,
            "title": self._extract_title(raw_html),
            "content": self.clean_text(raw_html),
            "metadata": {"source_url": url}
        }

    def _extract_title(self, html: str) -> str:
        """Extract title from HTML content"""
        # Simple regex to extract title - in practice, you might use BeautifulSoup
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()

        # Look for h1 tags as title
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE)
        if h1_match:
            return re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()

        return "Untitled Document"

    def chunk_text(self, text: str, url: str = "", title: str = "") -> List[Dict[str, str]]:
        """
        Split text into overlapping chunks while preserving sentence boundaries
        """
        if len(text) <= self.config.chunk_size:
            return [{
                "content": text,
                "url": url,
                "title": title,
                "metadata": {"source_url": url, "chunk_id": 0, "total_chunks": 1}
            }]

        chunks = []
        sentences = re.split(r'(?<=[.!?]) +', text)

        current_chunk = ""
        chunk_id = 0

        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.config.chunk_size and current_chunk:
                # Add current chunk to results
                if len(current_chunk.strip()) >= self.config.min_chunk_size:
                    chunks.append({
                        "content": current_chunk.strip(),
                        "url": url,
                        "title": title,
                        "metadata": {"source_url": url, "chunk_id": chunk_id, "total_chunks": len(chunks) + 1}
                    })

                # Start new chunk with overlap
                if self.config.chunk_overlap > 0:
                    # Get the end of current chunk for overlap
                    overlap_start = max(0, len(current_chunk) - self.config.chunk_overlap)
                    current_chunk = current_chunk[overlap_start:] + " " + sentence
                else:
                    current_chunk = sentence
                chunk_id += 1
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        # Add the final chunk
        if current_chunk.strip() and len(current_chunk.strip()) >= self.config.min_chunk_size:
            chunks.append({
                "content": current_chunk.strip(),
                "url": url,
                "title": title,
                "metadata": {"source_url": url, "chunk_id": chunk_id, "total_chunks": len(chunks) + 1}
            })

        # Update total_chunks for all chunks
        for i, chunk in enumerate(chunks):
            chunk["metadata"]["total_chunks"] = len(chunks)
            chunk["metadata"]["chunk_id"] = i

        return chunks

    def preprocess_content(self, content_map: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Preprocess all content from crawled URLs into chunks ready for embedding
        """
        all_chunks = []

        for url, content in content_map.items():
            if content and len(content.strip()) >= self.config.min_chunk_size:
                # Clean the content
                cleaned_content = self.clean_text(content)

                # Create chunks
                chunks = self.chunk_text(cleaned_content, url)
                all_chunks.extend(chunks)

                self.logger.info(f"Processed {len(chunks)} chunks from {url}")

        self.logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks