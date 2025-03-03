import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
import tempfile

from app.recursive_zoom import generate_recursive_zoom

# Streamlit UI
st.set_page_config(page_title="Recursive Zoom App", layout="wide")

st.title("🔍 Recursive Zoom Effect Generator")

# Sidebar for controls
st.sidebar.header("⚙️ Settings")

uploaded_file = st.sidebar.file_uploader("📤 Upload an Image", type=["jpg", "png", "jpeg"])

depth = st.sidebar.slider("🔁 Zoom Depth", min_value=1, max_value=10, value=5)
scale = st.sidebar.slider("🔍 Zoom Scale", min_value=0.1, max_value=0.9, value=0.5, step=0.1)

# Create a directory for processed images
output_dir = "static/images"
os.makedirs(output_dir, exist_ok=True)

# Processing the image
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

    # Load image to get dimensions
    image = cv2.imread(image_path)
    if image is None:
        st.error("❌ Error: Invalid image file.")
    else:
        height, width, _ = image.shape

        # Safe limits for x and y positions
        x_position = st.sidebar.slider("📍 X Position", min_value=0, max_value=width-50, value=50)
        y_position = st.sidebar.slider("📍 Y Position", min_value=0, max_value=height-50, value=50)

        # Display original image
        col1, col2 = st.columns(2)

        with col1:
            st.image(image_path, caption="Original Image", use_container_width=True)

        # Apply Recursive Zoom Effect
        with st.spinner("Processing... Please wait ⏳"):
            output_image = generate_recursive_zoom(image_path, depth, scale, (x_position, y_position))

        # Save and Display Processed Image
        output_path = os.path.join(output_dir, "output_zoomed.jpg")
        cv2.imwrite(output_path, output_image)

        if os.path.exists(output_path):
            with col2:
                st.image(output_path, caption="Processed Image", use_container_width=True)
        else:
            st.error("❌ Error: Processed image could not be saved.")

        # Download Option
        with open(output_path, "rb") as file:
            st.sidebar.download_button("📥 Download Image", data=file, file_name="recursive_zoom.jpg")

        # Video Animation Feature
        if st.sidebar.button("🎥 Generate Animation"):
            st.sidebar.write("⏳ Creating animation... Please wait.")

            def generate_animation(image_path, depth=5, scale=0.5, position=(50, 50)):
                """ Generate frames and create a zoom animation while ensuring boundaries. """
                frames = []
                image = cv2.imread(image_path)

                for _ in range(depth):
                    new_width = int(image.shape[1] * scale)
                    new_height = int(image.shape[0] * scale)
                    x, y = position

                    # Boundary check
                    if new_width > image.shape[1] or new_height > image.shape[0] or x + new_width > image.shape[1] or y + new_height > image.shape[0]:
                        st.sidebar.warning(f"⚠️ Skipping iteration: Zoomed image ({new_width}x{new_height}) exceeds original dimensions ({image.shape[1]}x{image.shape[0]}) at ({x}, {y})")
                        break

                    small_image = cv2.resize(image, (new_width, new_height))
                    image[y:y+new_height, x:x+new_width] = small_image
                    frames.append(image.copy())

                # Save as video
                output_video_path = os.path.join(output_dir, "recursive_zoom_animation.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                height, width, _ = image.shape
                video = cv2.VideoWriter(output_video_path, fourcc, 5, (width, height))

                for frame in frames:
                    video.write(frame)

                video.release()
                return output_video_path

            video_path = generate_animation(image_path, depth, scale, (x_position, y_position))

            if os.path.exists(video_path):
                st.sidebar.video(video_path)

                with open(video_path, "rb") as file:
                    st.sidebar.download_button("📥 Download Video", data=file, file_name="recursive_zoom.mp4", mime="video/mp4")
            else:
                st.sidebar.error("❌ Error: Video could not be generated.")

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Tip:** Adjust the sliders for different zoom effects!")
