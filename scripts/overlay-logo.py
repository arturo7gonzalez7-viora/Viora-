#!/usr/bin/env python3
"""Overlay Casa Mariachi logo onto gift card designs."""
import sys
from PIL import Image

def overlay_logo(base_path, logo_path, output_path, logo_width=400, opacity=0.9, position='center'):
    # Load images
    base = Image.open(base_path).convert('RGBA')
    logo = Image.open(logo_path).convert('RGBA')
    
    # Resize logo
    aspect = logo.height / logo.width
    logo = logo.resize((logo_width, int(logo_width * aspect)), Image.Resampling.LANCZOS)
    
    # Adjust opacity
    alpha = logo.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    logo.putalpha(alpha)
    
    # Calculate position
    if position == 'center':
        x = (base.width - logo.width) // 2
        y = (base.height - logo.height) // 2
    elif position == 'bottom-center':
        x = (base.width - logo.width) // 2
        y = base.height - logo.height - 60
    
    # Composite
    base.paste(logo, (x, y), logo)
    
    # Convert back to RGB for saving as PNG/JPEG
    final = Image.new('RGB', base.size, (255, 255, 255))
    final.paste(base, (0, 0), base)
    final.save(output_path, 'PNG', quality=95)
    print(output_path)

if __name__ == '__main__':
    base_path = sys.argv[1]
    logo_path = sys.argv[2]
    output_path = sys.argv[3]
    logo_width = int(sys.argv[4]) if len(sys.argv) > 4 else 400
    opacity = float(sys.argv[5]) if len(sys.argv) > 5 else 0.9
    position = sys.argv[6] if len(sys.argv) > 6 else 'center'
    overlay_logo(base_path, logo_path, output_path, logo_width, opacity, position)
