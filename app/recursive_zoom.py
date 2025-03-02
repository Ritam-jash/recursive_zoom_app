import cv2
import numpy as np

def generate_recursive_zoom(image_path, depth=5, scale=0.5, position=(50, 50)):
    """
    Generates a recursive zoom effect by embedding smaller versions of an image inside itself.

    Parameters:
    - image_path (str): Path to the input image.
    - depth (int): Number of recursive iterations.
    - scale (float): Scaling factor for each recursion.
    - position (tuple): (x, y) coordinates for placement of smaller images.

    Returns:
    - processed_image (numpy array): Image with recursive zoom effect applied.
    """
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Invalid image path or format!")

    height, width, _ = image.shape

    for _ in range(depth):
        # Resize the image based on scale
        small_image = cv2.resize(image, (int(width * scale), int(height * scale)))

        x, y = position  # X, Y placement coordinates

        small_h, small_w, _ = small_image.shape

        # **Boundary check to ensure smaller image fits inside original**
        if x + small_w > width or y + small_h > height:
            print(f"Skipping iteration: Small image ({small_w}x{small_h}) exceeds original dimensions ({width}x{height}) at position ({x}, {y})")
            break  # Stop if the small image goes out of bounds

        # Overlay the smaller image on the original
        image[y:y+small_h, x:x+small_w] = small_image

    return image
