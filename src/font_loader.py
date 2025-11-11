"""
Font Loader Module
Loads TrueType fonts using PIL/Pillow and generates glyph textures.
"""

from PIL import Image, ImageDraw, ImageFont  # type: ignore
from OpenGL.GL import *  # type: ignore
import numpy as np
from typing import Optional
import os
from .font import Font, Glyph


class FontLoader:
    """
    Loads TrueType fonts and generates OpenGL textures for glyphs.
    """
    
    # ASCII printable characters (32-126)
    DEFAULT_CHARSET = ''.join(chr(i) for i in range(32, 127))
    
    @staticmethod
    def load(filepath: str, size: int = 48, charset: Optional[str] = None) -> Optional[Font]:
        """
        Load a TrueType font and generate glyph textures using PIL.
        
        Args:
            filepath: Path to .ttf font file
            size: Font size in pixels (height)
            charset: Characters to load (defaults to ASCII printable)
            
        Returns:
            Font instance if successful, None otherwise
        """
        try:
            if not os.path.exists(filepath):
                print(f"ERROR: Font file not found: {filepath}")
                return None
            
            print(f"Loading font: {filepath} (size {size})")
            
            # Load font with PIL
            pil_font = ImageFont.truetype(filepath, size)
            
            # Create font instance
            font = Font(filepath, size)
            
            # Get font metrics for consistent baseline
            ascent, descent = pil_font.getmetrics()
            font.line_height = ascent + descent
            font.ascent = ascent
            font.descent = descent
            
            # Use default charset if none provided
            if charset is None:
                charset = FontLoader.DEFAULT_CHARSET
            
            # Disable byte-alignment restriction
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            
            # Load each character
            loaded_count = 0
            for char in charset:
                try:
                    # Get character bounding box
                    bbox = pil_font.getbbox(char)
                    if bbox is None:
                        continue
                    
                    # Skip empty glyphs (like space)
                    if bbox[2] - bbox[0] <= 0 or bbox[3] - bbox[1] <= 0:
                        # For space and other whitespace, still track advance
                        if char == ' ':
                            advance = int(pil_font.getlength(char))
                            glyph = Glyph(
                                texture_id=0,
                                width=0,
                                height=0,
                                bearing_x=0,
                                bearing_y=0,
                                advance=advance << 6  # Convert to 1/64 pixels
                            )
                            font.add_glyph(char, glyph)
                            loaded_count += 1
                        continue
                    
                    # Create fixed-height image for consistent alignment
                    # Use font ascent + descent as fixed height for all characters
                    img_width = int(pil_font.getlength(char)) + 4
                    img_height = ascent + descent
                    image = Image.new('L', (img_width, img_height), 0)  # Grayscale
                    draw = ImageDraw.Draw(image)
                    
                    # Draw character at fixed position (baseline at ascent from top)
                    draw.text((2, 0), char, font=pil_font, fill=255, anchor='la')  # Left-aligned, baseline anchor
                    
                    # Flip image vertically (PIL is top-down, OpenGL is bottom-up)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    
                    # Convert to numpy array
                    img_data = np.array(image, dtype=np.uint8)
                    
                    # Generate texture
                    texture_id = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    
                    # Upload texture data
                    glTexImage2D(
                        GL_TEXTURE_2D,
                        0,
                        GL_RED,
                        img_width,
                        img_height,
                        0,
                        GL_RED,
                        GL_UNSIGNED_BYTE,
                        img_data
                    )
                    
                    # Set texture parameters
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    
                    # Calculate metrics
                    # All glyphs now have same height, positioned with baseline at 'ascent' from top
                    bearing_x = 0
                    bearing_y = ascent  # Distance from top of image to baseline
                    
                    # advance: horizontal distance to next character
                    advance = int(pil_font.getlength(char))
                    
                    # Create glyph
                    glyph = Glyph(
                        texture_id=texture_id,
                        width=img_width,
                        height=img_height,
                        bearing_x=bearing_x,
                        bearing_y=bearing_y,
                        advance=advance << 6  # Convert to 1/64 pixels for compatibility
                    )
                    
                    font.add_glyph(char, glyph)
                    loaded_count += 1
                    
                except Exception as e:
                    print(f"WARNING: Failed to load glyph '{char}': {e}")
                    continue
            
            glBindTexture(GL_TEXTURE_2D, 0)
            
            print(f"[OK] Loaded font '{os.path.basename(filepath)}' with {loaded_count} glyphs")
            return font
            
        except Exception as e:
            print(f"ERROR: Failed to load font '{filepath}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def cleanup_font(font: Font):
        """
        Clean up OpenGL resources for a font.
        
        Args:
            font: Font to clean up
        """
        try:
            for glyph in font.glyphs.values():
                if glyph.texture_id:
                    glDeleteTextures([glyph.texture_id])
            font.glyphs.clear()
        except Exception as e:
            print(f"ERROR: Failed to cleanup font: {e}")

