# 🔍 Recursive Zoom Image Generator

This project generates a recursive zoom effect by embedding smaller versions of an image inside itself.

/recursive_zoom_app
├── app/
│   ├── __init__.py         # Flask app initialization
│   ├── routes.py           # Flask routes (optional)
│   ├── recursive_zoom.py   # Core function to generate recursive zoom images
│   └── utils.py            # Helper functions for image processing
│
├── static/
│   └── images/             # Folder to store uploaded and processed images
│
├── templates/              # (Not needed if only using Streamlit)
│
├── streamlit_app.py        # Streamlit frontend for user interaction
├── requirements.txt        # Dependencies for Flask, OpenCV, Streamlit, etc.
├── run.py                  # Entry point for running the Flask server (optional)
├── .gitignore              # Ignore unnecessary files
└── README.md               # Project overview and instructions


## 🚀 Features
- Upload an image
- Customize recursion depth, scale, and position
- Preview the output image
- Download the processed image

## 🛠️ Tech Stack
- **Frontend**: Streamlit (for fast UI)
- **Libraries**: OpenCV, NumPy, PIL (Pillow)

## 🔧 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/recursive_zoom_app.git
   cd recursive_zoom_app
