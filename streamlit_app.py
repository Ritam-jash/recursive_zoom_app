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
x_position = st.sidebar.slider("📍 X Position", min_value=0, max_value=500, value=50)
y_position = st.sidebar.slider("📍 Y Position", min_value=0, max_value=500, value=50)

# Processing the image
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        image_path = temp_file.name

    # Display original image
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(image_path, caption="Original Image", use_column_width=True)

    # Apply Recursive Zoom Effect
    with st.spinner("Processing... Please wait ⏳"):
        output_image = generate_recursive_zoom(image_path, depth, scale, (x_position, y_position))

    # Save and Display Processed Image
    output_path = "static/images/output_zoomed.jpg"
    cv2.imwrite(output_path, output_image)

    with col2:
        st.image(output_path, caption="Processed Image", use_column_width=True)

    # Download Option
    st.sidebar.download_button("📥 Download Image", data=open(output_path, "rb").read(), file_name="recursive_zoom.jpg")

# Video Animation Feature
if st.sidebar.button("🎥 Generate Animation"):
    st.sidebar.write("⏳ Creating animation... Please wait.")

    def generate_animation(image_path, depth=5, scale=0.5, position=(50, 50)):
        """ Generate frames and create a zoom animation """
        frames = []
        image = cv2.imread(image_path)
        
        for _ in range(depth):
            small_image = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
            x, y = position

            # Boundary check
            if x + small_image.shape[1] > image.shape[1] or y + small_image.shape[0] > image.shape[0]:
                break

            image[y:y+small_image.shape[0], x:x+small_image.shape[1]] = small_image
            frames.append(image.copy())

        # Save as video
        output_video_path = "recursive_zoom_animation.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        height, width, _ = image.shape
        video = cv2.VideoWriter(output_video_path, fourcc, 5, (width, height))

        for frame in frames:
            video.write(frame)

        video.release()
        return output_video_path

    video_path = generate_animation(image_path, depth, scale, (x_position, y_position))
    st.sidebar.video(video_path)

    # Download Video
    st.sidebar.download_button("📥 Download Video", data=open(video_path, "rb").read(), file_name="recursive_zoom.mp4", mime="video/mp4")

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Tip:** Adjust the sliders for different zoom effects!")
