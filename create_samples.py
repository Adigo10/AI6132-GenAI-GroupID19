#!/usr/bin/env python3
"""Create sample character images for testing."""

import numpy as np
from PIL import Image, ImageDraw
import os

# Create sample_data directory
os.makedirs('sample_data', exist_ok=True)

# Create a simple character - a colorful circle
size = 300
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw a gradient circle
center = size // 2
radius = size // 3

# Create a circular mask
for i in range(radius):
    alpha = int(255 * (radius - i) / radius)
    color_intensity = int(255 * i / radius)
    color = (255, color_intensity, 100, alpha)
    draw.ellipse([center - (radius - i), center - (radius - i),
                  center + (radius - i), center + (radius - i)],
                 fill=color)

img.save('sample_data/character_circle.png')
print("✓ Created: sample_data/character_circle.png")

# Create a star character
img2 = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw2 = ImageDraw.Draw(img2)

# Draw a star
points = []
for i in range(10):
    angle = i * np.pi / 5 - np.pi/2
    r = radius if i % 2 == 0 else radius // 2
    x = center + r * np.cos(angle)
    y = center + r * np.sin(angle)
    points.append((x, y))

draw2.polygon(points, fill=(255, 215, 0, 255), outline=(255, 165, 0, 255))

img2.save('sample_data/character_star.png')
print("✓ Created: sample_data/character_star.png")

# Create a simple background
bg = Image.new('RGB', (1920, 1080), (135, 206, 235))  # Sky blue
bg.save('sample_data/background_sky.jpg')
print("✓ Created: sample_data/background_sky.jpg")

print("\nSample data created successfully!")
