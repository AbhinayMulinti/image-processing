# Image Proc - Simple Image Processing App

This is a web application built with Python that allows you to upload and edit images using various filters. It uses **Streamlit** for the user interface and **OpenCV** for the image processing.

## 📸 Screenshots

### Landing Page
![Landing Page](Landing%20page.png)

### Image Editing Page
![Image Editing Page](image%20editing%20page.png)

---

## 📽️ Demo Video
Check out the app in action:
[Link to Demo Video](https://drive.google.com/file/d/1VhfvbxFnbKwOsTMTGY3EXZW1c9EP0u5c/view?usp=drive_link)

---

## 🖼️ What it does
You can upload any JPG or PNG image and apply the following effects:

- **Gaussian Blur**: Makes the image blurry.
- **Sharpness**: Makes the details in the image clearer.
- **Brightness**: Makes the image lighter or darker.
- **Contrast**: Increases or decreases the difference between light and dark areas.
- **Edge Detection**: Shows only the edges/outlines of objects in the image.
- **Grayscale**: Turns the image into black and white.

The app also shows you the image resolution and file size in real-time.

---

## 🛠️ How to run it

### 1. Install Python
Make sure you have Python installed on your computer.

### 2. Install Requirements
Open your terminal and run this command to install the necessary libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the App
Start the app by running:
```bash
streamlit run app.py
```

---

## 📁 Files in this project
- `app.py`: The main file that runs the website.
- `filters.py`: Contains the code for all the image filters.
- `utils.py`: Small helper functions for the app.
- `style.css`: The custom styling for the dark theme.
- `landing_page.py`: The code for the starting page.

---
Built with Streamlit Using **OpenCV** by Abhinay
