"""
Font Module
Handles font data and glyph information.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np


@dataclass
class Glyph:
    """Represents a single character glyph."""
    texture_id: int  # OpenGL texture ID for this glyph
    width: int  # Width of glyph bitmap
    height: int  # Height of glyph bitmap
    bearing_x: int  # Horizontal bearing (offset from baseline to left)
    bearing_y: int  # Vertical bearing (offset from baseline to top)
    advance: int  # Horizontal advance to next glyph


class Font:
    """
    Font class that stores font data and glyph information.
    """
    
    def __init__(self, filepath: str, size: int = 48):
        """
        Initialize Font.
        
        Args:
            filepath: Path to the font file
            size: Font size in pixels
        """
        self.filepath = filepath
        self.size = size
        self.glyphs: Dict[str, Glyph] = {}
        self.line_height = 0
        self.ascent = 0
        self.descent = 0
        
    def add_glyph(self, character: str, glyph: Glyph):
        """
        Add a glyph to the font.
        
        Args:
            character: The character this glyph represents
            glyph: The glyph data
        """
        self.glyphs[character] = glyph
    
    def get_glyph(self, character: str) -> Optional[Glyph]:
        """
        Get glyph for a character.
        
        Args:
            character: The character to get glyph for
            
        Returns:
            Glyph if found, None otherwise
        """
        return self.glyphs.get(character)
    
    def has_glyph(self, character: str) -> bool:
        """
        Check if font has glyph for character.
        
        Args:
            character: The character to check
            
        Returns:
            True if glyph exists, False otherwise
        """
        return character in self.glyphs
    
    def get_text_width(self, text: str) -> int:
        """
        Calculate the width of text in pixels.
        
        Args:
            text: The text to measure
            
        Returns:
            Width in pixels
        """
        width = 0
        for char in text:
            glyph = self.get_glyph(char)
            if glyph:
                width += glyph.advance >> 6  # Advance is in 1/64 pixels
        return width
    
    def __repr__(self) -> str:
        return f"Font(filepath='{self.filepath}', size={self.size}, glyphs={len(self.glyphs)})"

