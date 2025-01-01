import numpy as np
from PIL import Image

# The size of the image.
width, height = 1000, 1000

# Create an array that represents the image.
# Each pixel's value will be determined by a quadratic function of its distance to the center.
image_array = np.zeros((height, width, 3), dtype=np.uint8)

# The center of the image.
center_x, center_y = width // 2, height // 2

# Orange color values (you can adjust these to get the exact color you want)
orange = np.array([255, 165, 0], dtype=np.uint8)

# Fill in the pixel values.
for y in range(height):
    for x in range(width):
        dist2 = (x - center_x)**2 / (width**2) + (y - center_y)**2/ (height**2)
        brightness = np.exp(-dist2*10)
        image_array[y, x] = orange * brightness

print(image_array)
# Convert the array to an image and save it.
Image.fromarray(image_array).save('gradient_orange.png')
