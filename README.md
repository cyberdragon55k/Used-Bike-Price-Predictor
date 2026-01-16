# 🏍️ Used Bike Price Predictor - https://used-bike-price.streamlit.app/
https://huggingface.co/spaces/AdityaNamdev/bike-price-predictor
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas)

### A Machine Learning-powered dashboard that estimates the fair market value of used motorcycles with **94% accuracy**.

---

## 📌 Problem Statement

Used bike prices in India vary significantly depending on:
- Kilometers driven
- Manufacturing year
- Engine capacity
- Brand perception
- City-wise market demand  

👉 This project solves that problem using **data-driven machine learning predictions** combined with a clean, user-friendly UI.

---

## 🚀 About The Project

Buying or selling a used bike can be tricky. This tool removes the guesswork by using a trained **Linear Regression Model** to predict the accurate market price based on real-world data.

Unlike simple calculators, this app features a **Marketplace Recommender System**—it not only tells you the price but also suggests 5 other real market listings available for that specific budget!

## ✨ Key Features

- 🔍 **Smart Bike Search**
  - Auto-fills brand and engine capacity
  - Displays official brand logo

- 📊 **ML-Based Price Estimation**
  - Predicts fair market value using a trained regression model
  - Shows a realistic confidence range (±10%)

- 🎯 **Modern UI/UX**
  - Dark-themed professional interface
  - Price count-up animation
  - Clear visual hierarchy

- 🔁 **Market Comparison**
  - Displays similar bikes available in the same price range
  - Helps users validate predicted prices

- ⚡ **Optimized Performance**
  - Cached dataset and model loading
  - Fast, responsive user experience

---


## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (for the interactive web UI)
* **Backend:** Python
* **Machine Learning:** Scikit-Learn (Linear Regression Pipeline)
* **Data Processing:** Pandas & NumPy

---

## 📁 Dataset
The model was trained on a comprehensive dataset of **32,648 used bike listings**.
* **Source:** [Kaggle - Used Bikes in India](https://www.kaggle.com/datasets/saisaathvik/used-bikes-prices-in-india)
* **Features:** `kms_driven`, `age`, `engine_capacity`, `brand`, `price`.
* **Preprocessing:** Cleaned outliers and handled missing values using Pandas.

---

## 🧠 Machine Learning Approach
- Real-world used bike listings across Indian cities  
- Features used:
  - `kms_driven`
  - `age`
  - `engine_capacity (cc)`
- Target:
  - `price`
---

### 🧪 Model
- Regression-based machine learning model
- Trained offline using historical data
- Serialized using `pickle` and loaded in Streamlit
---

## 📂 Project Structure

```text
USED_BIKE_PREDICTOR/
│
├── images/                 # 📂 Contains logos for brands (BMW.png, KTM.png, etc.)
├── Used_Bikes.csv          # 📄 Dataset containing 32,000+ bike listings
├── bike_model.pkl          # 🧠 Trained Machine Learning Model
├── app.py                  # 🚀 Main Streamlit Application
├── Used Bike Price.ipynb   # 📓 Jupyter Notebook (Model Training Code)
└── README.md               # 📄 Documentation
