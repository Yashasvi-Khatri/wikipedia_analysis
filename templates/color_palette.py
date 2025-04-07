#!/usr/bin/env python3
"""
Color Palette module for Wikipedia Word Cloud visualization.
Provides a base ColorPalette class and several common color palettes.
"""

class ColorPalette:
    """
    Base class for color palettes.
    Each palette contains 6 hex color codes.
    """
    
    def __init__(self, colors=None):
        """
        Initialize a color palette with 6 colors.
        
        Args:
            colors (list): List of 6 hex color codes. If None, uses default colors.
        """
        if colors and len(colors) == 6:
            self.colors = colors
        else:
            # Default to a grayscale palette if no colors provided
            self.colors = ["#000000", "#333333", "#666666", "#999999", "#CCCCCC", "#FFFFFF"]
    
    def get_colors(self):
        """Return the list of colors in the palette."""
        return self.colors
    
    def get_color(self, index):
        """
        Get a specific color by index (with wrapping).
        
        Args:
            index (int): Index of the color to retrieve
            
        Returns:
            str: Hex color code
        """
        return self.colors[index % len(self.colors)]
    
    def __iter__(self):
        """Make the palette iterable."""
        return iter(self.colors)
    
    def __getitem__(self, index):
        """Allow indexing to get colors."""
        return self.get_color(index)


class MaterialPalette(ColorPalette):
    """Google Material Design color palette."""
    
    def __init__(self):
        super().__init__([
            "#F44336",  # Red
            "#2196F3",  # Blue
            "#4CAF50",  # Green
            "#FFC107",  # Amber
            "#9C27B0",  # Purple
            "#FF9800",  # Orange
        ])


class PastelPalette(ColorPalette):
    """Soft pastel color palette."""
    
    def __init__(self):
        super().__init__([
            "#FFB3BA",  # Pastel Red
            "#FFDFBA",  # Pastel Orange
            "#FFFFBA",  # Pastel Yellow
            "#BAFFC9",  # Pastel Green
            "#BAE1FF",  # Pastel Blue
            "#E2BAFF",  # Pastel Purple
        ])


class VibrantPalette(ColorPalette):
    """Vibrant color palette."""
    
    def __init__(self):
        super().__init__([
            "#FF1744",  # Vibrant Red
            "#00E676",  # Vibrant Green
            "#2979FF",  # Vibrant Blue
            "#FFEA00",  # Vibrant Yellow
            "#D500F9",  # Vibrant Purple
            "#FF9100",  # Vibrant Orange
        ])


class EarthtonePalette(ColorPalette):
    """Earthy, natural color palette."""
    
    def __init__(self):
        super().__init__([
            "#795548",  # Brown
            "#8D6E63",  # Light Brown
            "#A1887F",  # Tan
            "#BCAAA4",  # Light Tan
            "#D7CCC8",  # Beige
            "#EFEBE9",  # Off-White
        ])


class OceanPalette(ColorPalette):
    """Ocean-inspired color palette."""
    
    def __init__(self):
        super().__init__([
            "#01579B",  # Deep Blue
            "#0288D1",  # Ocean Blue
            "#29B6F6",  # Sky Blue
            "#81D4FA",  # Light Blue
            "#B3E5FC",  # Very Light Blue
            "#E1F5FE",  # Almost White Blue
        ])


class SunsetPalette(ColorPalette):
    """Sunset-inspired color palette."""
    
    def __init__(self):
        super().__init__([
            "#FF6F00",  # Deep Orange
            "#FF9800",  # Orange
            "#FFC107",  # Amber
            "#FFEB3B",  # Yellow
            "#FFF176",  # Light Yellow
            "#FFF9C4",  # Very Light Yellow
        ])


# Dictionary of available palettes for easy access
PALETTES = {
    "default": ColorPalette(),
    "material": MaterialPalette(),
    "pastel": PastelPalette(),
    "vibrant": VibrantPalette(),
    "earthy": EarthtonePalette(),
    "ocean": OceanPalette(),
    "sunset": SunsetPalette(),
}


def get_palette(name="default"):
    """
    Get a color palette by name.
    
    Args:
        name (str): Name of the palette to retrieve
        
    Returns:
        ColorPalette: The requested color palette
    """
    return PALETTES.get(name.lower(), ColorPalette())