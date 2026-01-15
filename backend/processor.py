from bs4 import BeautifulSoup
from typing import List, Dict
from config import CHUNK_SIZE, CHUNK_OVERLAP

class TextProcessor:
    """
    Handles cleaning and chunking of text content
    """

    def clean_content(self, content: str, url: str) -> str:
        """
        Clean HTML content and extract plain text

        Args:
            content: Raw HTML content
            url: Source URL for context

        Returns:
            Cleaned plain text
        """
        try:
            soup = BeautifulSoup(content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            raise e

    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[Dict]:
        """
        Split text into chunks with overlap

        Args:
            text: Input text to chunk
            chunk_size: Maximum size of each chunk (uses config default if None)
            overlap: Overlap between chunks (uses config default if None)

        Returns:
            List of chunk dictionaries with 'text', 'index', and 'total' properties
        """
        if chunk_size is None:
            chunk_size = CHUNK_SIZE
        if overlap is None:
            overlap = CHUNK_OVERLAP

        chunks = []
        start = 0
        text_length = len(text)
        index = 0

        while start < text_length:
            # Determine the end position
            end = start + chunk_size

            # If this is not the last chunk, try to break at a sentence or word boundary
            if end < text_length:
                # Look for a good breaking point near the end
                search_start = end - overlap
                break_point = end

                # Look for sentence endings first
                for sep in ['.', '!', '?', '\n', ';', ':', ',']:
                    last_sep = text.rfind(sep, search_start, end)
                    if last_sep != -1:
                        break_point = last_sep + 1
                        break

                # If no good break point found, use the overlap point
                if break_point == end and end - search_start > overlap:
                    break_point = end - overlap

                end = break_point

            # Extract the chunk
            chunk_text = text[start:end].strip()

            # Only add chunk if it meets minimum size requirements
            if len(chunk_text) >= 10:  # Minimum 10 characters
                chunks.append({
                    'text': chunk_text,
                    'index': index,
                    'total': 0  # Will be updated after all chunks are created
                })

            # Move start position
            start = end - overlap if end < text_length and overlap > 0 else end
            index += 1

        # Update total count for each chunk
        for chunk in chunks:
            chunk['total'] = len(chunks)

        return chunks

    def validate_chunk(self, chunk_text: str, min_size: int = 100, max_size: int = 1000) -> bool:
        """
        Validate chunk size is within acceptable bounds

        Args:
            chunk_text: Text to validate
            min_size: Minimum allowed size
            max_size: Maximum allowed size

        Returns:
            True if chunk is valid, False otherwise
        """
        return min_size <= len(chunk_text) <= max_size