# 📌 Cross-platform application for analyzing liquid droplets with yolo11

## 📌 Description
The application, developed in PyQt5, is designed to count and analyze the distribution of liquid droplets in images using the YOLO11 model.

## 🚀 Functionality
- 🖥 **Graphical interface** for easy interaction
- ⚙ **Flexible configuration of model parameters**
- 📊 **Plotting graphs** to analyze results
- 👁 **Visualization of model operation**
- 📄 **Saving results to a CSV file**

## 📌 Image processing results
After image processing, you can get:
- 🔢 Number of drops in the image
- 📍 Drop location coordinates
- 📏 Drop diameters

---

## 📌 Application requirements
### General requirements:
- Trained model **yolo11n-seg**
- **Python v3.5 and higher** (Python v3.12 recommended)

### System requirements:
- 💻 **Computing power**: undefined. Processing is resource intensive, but parameters can be tuned to optimize performance. - 💾 **Free space**: ~1.5 GB (for a binary project ~600 MB)
- **Supported OS**: Windows, Linux, MacOS

---

## 📌 Installing and running the application
### ⏩ Running the application:
- cloning the repository
- installing Python v3.5 and higher
- creating a virtual environment
- installing dependencies requirements.txt ⚠️ **Note:** For Windows, add `PyQt5-Qt5==5.15.2` to requirements.txt, for MacOS - `PyQt5-Qt5==5.15.16`
- running app.py

## ✅ Examples of application images are located in the [examples/](examples/) folder

## ❓ FAQ (Frequently Asked Questions)
### 🔹 Where is trained model?
💬 The trained model is located in the [model/](model/) folder. You can also train it yourself or contact [mrBoB1k](https://github.com/mrBoB1k), [vladi2007](https://github.com/vladi2007) for help.
### 🔹 How to create a compiled application?
💬 You can use the python library `pyinstaller` to compile the application. To provide an already compiled application, contact [men4ikyura](https://github.com/men4ikyura)
### 🔹 Can the application be used for other purposes?
💬 Yes, but the code will need to be modified to process the model results, etc. In its current form, the application is specialized **only for liquid droplet analysis**.