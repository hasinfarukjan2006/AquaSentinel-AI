import os
from PIL import Image, ImageDraw

def create_pwa_icon(size, filename, maskable=False):
    # Create background image
    img = Image.new('RGBA', (size, size), (15, 23, 42, 255)) # #0f172a
    draw = ImageDraw.Draw(img)

    margin = size * 0.15 if maskable else size * 0.1
    center_x, center_y = size / 2, size / 2
    
    # Outer Shield / Circle
    radius = (size - 2 * margin) / 2
    if not maskable:
        # Draw subtle border
        draw.ellipse(
            [center_x - radius, center_y - radius, center_x + radius, center_y + radius],
            fill=(30, 41, 59, 255), # #1e293b
            outline=(37, 99, 235, 255), # #2563eb
            width=max(2, int(size * 0.02))
        )
    else:
        # Maskable full fill background
        draw.rectangle([0, 0, size, size], fill=(15, 23, 42, 255))

    # Water Droplet Shape
    # Droplet top point (center_x, center_y - radius * 0.55)
    # Droplet bottom curve center (center_x, center_y + radius * 0.15), radius_d
    r_d = radius * 0.38
    top_y = center_y - radius * 0.50
    bottom_cy = center_y + radius * 0.15

    # Draw droplet circle bottom
    draw.ellipse(
        [center_x - r_d, bottom_cy - r_d, center_x + r_d, bottom_cy + r_d],
        fill=(37, 99, 235, 255) # #2563eb
    )

    # Draw top triangle for droplet
    points = [
        (center_x, top_y),
        (center_x - r_d * 0.95, bottom_cy),
        (center_x + r_d * 0.95, bottom_cy)
    ]
    draw.polygon(points, fill=(37, 99, 235, 255))

    # Inner Droplet Highlight
    r_h = r_d * 0.3
    draw.ellipse(
        [center_x - r_h * 0.5, bottom_cy - r_h * 0.5, center_x + r_h * 0.5, bottom_cy + r_h * 0.5],
        fill=(96, 165, 250, 255) # #60a5fa
    )

    out_dir = 'frontend/public'
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    img.save(out_path, 'PNG')
    print(f"Generated PWA Icon ({size}x{size}): {out_path}")

if __name__ == '__main__':
    create_pwa_icon(192, 'icon-192.png')
    create_pwa_icon(512, 'icon-512.png')
    create_pwa_icon(512, 'icon-maskable.png', maskable=True)
