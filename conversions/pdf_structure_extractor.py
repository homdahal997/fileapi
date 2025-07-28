"""
Enhanced PDF to text converter with structure preservation and content boundary detection.
"""
import re
import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from io import BytesIO
import logging

logger = logging.getLogger(__name__)


@dataclass
class TextElement:
    """Represents a text element with structural information."""
    text: str
    element_type: str  # 'header', 'subheader', 'paragraph', 'list_item', 'footer', 'table'
    level: int = 0  # For headers (1-6), list nesting level
    font_size: Optional[float] = None
    is_bold: bool = False
    is_italic: bool = False
    bbox: Optional[Tuple[float, float, float, float]] = None  # (x0, y0, x1, y1)
    page_number: int = 1


class StructuredPDFExtractor:
    """Enhanced PDF text extractor with structure detection."""
    
    def __init__(self):
        self.elements: List[TextElement] = []
        self.avg_font_size = 12.0
        self.header_patterns = [
            r'^([A-Z][A-Z\s]{2,})\s*$',  # ALL CAPS headers
            r'^(\d+\.?\s+[A-Z][^.]*)\s*$',  # Numbered sections
            r'^([IVX]+\.?\s+[A-Z][^.]*)\s*$',  # Roman numerals
            r'^([A-Z]\.?\s+[A-Z][^.]*)\s*$',  # Letter sections
        ]
        self.list_patterns = [
            r'^\s*[\•\*\-\+]\s+',  # Bullet points
            r'^\s*\d+[\.\)]\s+',   # Numbered lists
            r'^\s*[a-z][\.\)]\s+', # Letter lists
            r'^\s*[ivx]+[\.\)]\s+', # Roman numeral lists
        ]
    
    def extract_structured_text(self, file_content: bytes, 
                              preserve_structure: bool = True) -> str:
        """
        Extract text from PDF with structure preservation.
        
        Args:
            file_content: PDF file content as bytes
            preserve_structure: Whether to preserve document structure
            
        Returns:
            Formatted text with structure preserved
        """
        try:
            # Try advanced extraction with pdfplumber first
            structured_text = self._extract_with_pdfplumber(file_content)
            if structured_text and preserve_structure:
                return self._format_structured_text()
            
            # Fallback to PyMuPDF if available
            if not structured_text:
                structured_text = self._extract_with_pymupdf(file_content)
                if structured_text and preserve_structure:
                    return self._format_structured_text()
            
            # Final fallback to PyPDF2
            if not structured_text:
                structured_text = self._extract_with_pypdf2(file_content)
            
            return structured_text or "No readable text found in the PDF document."
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            # Final fallback
            return self._extract_with_pypdf2(file_content)
    
    def _extract_with_pdfplumber(self, file_content: bytes) -> str:
        """Extract text using pdfplumber with detailed structure analysis."""
        try:
            import pdfplumber
            
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                self.elements = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract characters with font information
                    chars = page.chars
                    if not chars:
                        continue
                    
                    # Group characters into text blocks
                    text_blocks = self._group_chars_into_blocks(chars)
                    
                    # Analyze each text block for structure
                    for block in text_blocks:
                        element = self._analyze_text_block(block, page_num)
                        if element and element.text.strip():
                            self.elements.append(element)
                
                return "structured_extraction_complete"
                
        except ImportError:
            logger.warning("pdfplumber not available, falling back to other methods")
            return ""
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {e}")
            return ""
    
    def _extract_with_pymupdf(self, file_content: bytes) -> str:
        """Extract text using PyMuPDF with structure analysis."""
        try:
            import fitz  # PyMuPDF
            
            doc = fitz.open(stream=file_content, filetype="pdf")
            self.elements = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Get text with font information
                blocks = page.get_text("dict")
                
                for block in blocks["blocks"]:
                    if "lines" not in block:
                        continue
                    
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if not text:
                                continue
                            
                            element = TextElement(
                                text=text,
                                element_type="paragraph",
                                font_size=span["size"],
                                is_bold="bold" in span["font"].lower(),
                                is_italic="italic" in span["font"].lower(),
                                bbox=span["bbox"],
                                page_number=page_num + 1
                            )
                            
                            # Classify element type
                            element = self._classify_element(element)
                            self.elements.append(element)
            
            doc.close()
            return "structured_extraction_complete"
            
        except ImportError:
            logger.warning("PyMuPDF not available, falling back to PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return ""
    
    def _extract_with_pypdf2(self, file_content: bytes) -> str:
        """Fallback extraction using PyPDF2."""
        try:
            import PyPDF2
            
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if page_text:
                    # Basic structure detection on plain text
                    lines = page_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        element = TextElement(
                            text=line,
                            element_type="paragraph",
                            page_number=page_num + 1
                        )
                        element = self._classify_element_simple(element)
                        self.elements.append(element)
            
            return self._format_structured_text()
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return f"PDF extraction failed: {str(e)}"
    
    def _group_chars_into_blocks(self, chars: List[Dict]) -> List[List[Dict]]:
        """Group characters into logical text blocks."""
        if not chars:
            return []
        
        # Sort characters by position (top to bottom, left to right)
        chars_sorted = sorted(chars, key=lambda c: (c['top'], c['x0']))
        
        blocks = []
        current_block = [chars_sorted[0]]
        
        for char in chars_sorted[1:]:
            last_char = current_block[-1]
            
            # Check if character belongs to current block
            vertical_gap = abs(char['top'] - last_char['top'])
            horizontal_gap = char['x0'] - last_char['x1']
            
            # Start new block if large gap or new line
            if vertical_gap > 5 or horizontal_gap > 20:
                if current_block:
                    blocks.append(current_block)
                current_block = [char]
            else:
                current_block.append(char)
        
        if current_block:
            blocks.append(current_block)
        
        return blocks
    
    def _analyze_text_block(self, block: List[Dict], page_num: int) -> Optional[TextElement]:
        """Analyze a text block to determine its structure."""
        if not block:
            return None
        
        # Combine text from all characters in block
        text = ''.join(char['text'] for char in block)
        text = text.strip()
        
        if not text:
            return None
        
        # Get font information from first character
        first_char = block[0]
        avg_font_size = sum(char.get('size', 12) for char in block) / len(block)
        
        element = TextElement(
            text=text,
            element_type="paragraph",
            font_size=avg_font_size,
            bbox=(first_char['x0'], first_char['top'], 
                  max(char['x1'] for char in block),
                  max(char['bottom'] for char in block)),
            page_number=page_num
        )
        
        return self._classify_element(element)
    
    def _classify_element(self, element: TextElement) -> TextElement:
        """Classify text element based on content and formatting."""
        text = element.text.strip()
        
        # Calculate average font size for comparison
        if not hasattr(self, 'font_sizes'):
            self.font_sizes = []
        if element.font_size:
            self.font_sizes.append(element.font_size)
            self.avg_font_size = sum(self.font_sizes) / len(self.font_sizes)
        
        # Header detection
        if self._is_header(element):
            element.element_type = "header"
            element.level = self._determine_header_level(element)
        
        # List item detection
        elif self._is_list_item(text):
            element.element_type = "list_item"
            element.level = self._determine_list_level(text)
        
        # Footer detection
        elif self._is_footer(text, element.page_number):
            element.element_type = "footer"
        
        # Table detection (basic)
        elif self._is_table_content(text):
            element.element_type = "table"
        
        return element
    
    def _classify_element_simple(self, element: TextElement) -> TextElement:
        """Simple classification for PyPDF2 extracted text."""
        text = element.text.strip()
        
        # Header patterns
        if any(re.match(pattern, text) for pattern in self.header_patterns):
            element.element_type = "header"
            element.level = 1
        
        # List patterns
        elif any(re.match(pattern, text) for pattern in self.list_patterns):
            element.element_type = "list_item"
            element.level = 1
        
        # Short lines might be headers
        elif len(text) < 60 and text.isupper():
            element.element_type = "header"
            element.level = 2
        
        return element
    
    def _is_header(self, element: TextElement) -> bool:
        """Determine if element is a header."""
        text = element.text.strip()
        
        # Font size check
        if element.font_size and element.font_size > self.avg_font_size * 1.2:
            return True
        
        # Bold text that's short
        if element.is_bold and len(text) < 100:
            return True
        
        # Pattern matching
        if any(re.match(pattern, text) for pattern in self.header_patterns):
            return True
        
        # All caps short text
        if text.isupper() and len(text) < 80 and len(text) > 3:
            return True
        
        return False
    
    def _is_list_item(self, text: str) -> bool:
        """Check if text is a list item."""
        return any(re.match(pattern, text) for pattern in self.list_patterns)
    
    def _is_footer(self, text: str, page_number: int) -> bool:
        """Check if text is footer content."""
        # Page numbers
        if re.match(r'^\s*\d+\s*$', text):
            return True
        
        # Common footer patterns
        footer_patterns = [
            r'page\s+\d+',
            r'copyright',
            r'©',
            r'confidential',
            r'proprietary',
        ]
        
        return any(re.search(pattern, text.lower()) for pattern in footer_patterns)
    
    def _is_table_content(self, text: str) -> bool:
        """Basic table content detection."""
        # Multiple tabs or spaces suggesting tabular data
        if '\t' in text or re.search(r'\s{3,}', text):
            return True
        
        # Multiple numbers separated by spaces
        if re.search(r'\d+\s+\d+', text):
            return True
        
        return False
    
    def _determine_header_level(self, element: TextElement) -> int:
        """Determine header level (1-6)."""
        if element.font_size:
            if element.font_size > self.avg_font_size * 2:
                return 1
            elif element.font_size > self.avg_font_size * 1.5:
                return 2
            elif element.font_size > self.avg_font_size * 1.2:
                return 3
            else:
                return 4
        
        # Fallback to text analysis
        text = element.text.strip()
        if re.match(r'^\d+\.?\s+', text):
            return 1
        elif re.match(r'^\d+\.\d+\.?\s+', text):
            return 2
        elif re.match(r'^\d+\.\d+\.\d+\.?\s+', text):
            return 3
        
        return 1
    
    def _determine_list_level(self, text: str) -> int:
        """Determine list nesting level."""
        leading_spaces = len(text) - len(text.lstrip())
        return max(1, leading_spaces // 4 + 1)
    
    def _format_structured_text(self) -> str:
        """Format extracted elements into structured text."""
        if not self.elements:
            return "No readable text found in the PDF document."
        
        output_lines = []
        current_page = 1
        
        for element in self.elements:
            # Page break indicator
            if element.page_number > current_page:
                output_lines.append(f"\n{'='*50}")
                output_lines.append(f"PAGE {element.page_number}")
                output_lines.append(f"{'='*50}\n")
                current_page = element.page_number
            
            # Format based on element type
            if element.element_type == "header":
                prefix = "#" * element.level
                output_lines.append(f"\n{prefix} {element.text}\n")
            
            elif element.element_type == "list_item":
                indent = "  " * (element.level - 1)
                output_lines.append(f"{indent}• {element.text}")
            
            elif element.element_type == "footer":
                output_lines.append(f"\n[FOOTER: {element.text}]\n")
            
            elif element.element_type == "table":
                output_lines.append(f"[TABLE] {element.text}")
            
            else:  # paragraph
                output_lines.append(f"{element.text}\n")
        
        return "\n".join(output_lines)
    
    def get_document_structure(self) -> Dict[str, Any]:
        """Get document structure as JSON."""
        structure = {
            "total_pages": max(e.page_number for e in self.elements) if self.elements else 0,
            "total_elements": len(self.elements),
            "headers": [],
            "outline": [],
            "statistics": {
                "headers": len([e for e in self.elements if e.element_type == "header"]),
                "paragraphs": len([e for e in self.elements if e.element_type == "paragraph"]),
                "lists": len([e for e in self.elements if e.element_type == "list_item"]),
                "tables": len([e for e in self.elements if e.element_type == "table"]),
            }
        }
        
        # Extract headers for outline
        current_outline = []
        for element in self.elements:
            if element.element_type == "header":
                header_info = {
                    "level": element.level,
                    "text": element.text,
                    "page": element.page_number
                }
                structure["headers"].append(header_info)
                current_outline.append(header_info)
        
        structure["outline"] = current_outline
        return structure


# Integration function for the converter
def extract_structured_pdf_text(file_content: bytes, options: Dict[str, Any] = None) -> Tuple[str, Dict]:
    """
    Extract structured text from PDF with preservation of document structure.
    
    Args:
        file_content: PDF file content as bytes
        options: Conversion options
        
    Returns:
        Tuple of (formatted_text, document_structure)
    """
    if options is None:
        options = {}
    
    extractor = StructuredPDFExtractor()
    
    # Extract with structure preservation
    preserve_structure = options.get('preserve_structure', True)
    formatted_text = extractor.extract_structured_text(file_content, preserve_structure)
    
    # Get document structure metadata
    structure = extractor.get_document_structure()
    
    return formatted_text, structure
