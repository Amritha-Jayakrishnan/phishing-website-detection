# 🔐 Phishing Website Detection using Machine Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![ML](https://img.shields.io/badge/Machine%20Learning-Ensemble-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> A machine learning-based system that detects phishing websites in real-time by analyzing URL patterns using multiple ML models and ensemble techniques.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [ML Models](#-machine-learning-models)
- [Feature Extraction](#-feature-extraction)
- [Installation](#-installation)
- [Usage](#-usage)
- [Results](#-results)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

Phishing attacks are one of the most prevalent cybersecurity threats, where attackers deceive users into revealing sensitive information through fraudulent websites. This project presents a **machine learning-powered phishing detection system** that analyzes URLs in real time to classify them as:

- ✅ **Legitimate** — Safe to visit
- 🚨 **Phishing** — Malicious / deceptive site

The system combines multiple ML algorithms with an **ensemble voting mechanism** to maximize prediction accuracy and reliability.

---

## 🚀 Features

- 🔍 **URL Feature Extraction** — Extracts structural and lexical features from raw URLs
- 🤖 **Multiple ML Models** — Random Forest, XGBoost, Logistic Regression, LightGBM
- 🧠 **Ensemble Prediction** — Combines model outputs for a robust final decision
- 📊 **Confidence Score** — Returns a probability score alongside each prediction
- 🌐 **Interactive Streamlit UI** — User-friendly interface for real-time URL analysis
- ⚡ **Real-time Analysis** — Instant predictions with no perceptible delay

---

## 📂 Project Structure

```
phishing-detection/
│
├── app/
│   └── streamlit_app.py          # Streamlit web interface
│
├── data/
│   ├── raw/                      # Raw datasets
│   └── processed/                # Cleaned and preprocessed data
│
├── models/
│   ├── random_forest.pkl         # Trained Random Forest model
│   ├── xgboost.pkl               # Trained XGBoost model
│   ├── logistic_regression.pkl   # Trained Logistic Regression model
│   └── lightgbm.pkl              # Trained LightGBM model
│
├── notebooks/
│   ├── 01_EDA.ipynb              # Exploratory Data Analysis
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb   # Model training and evaluation
│
├── src/
│   ├── feature_extraction.py     # URL feature extraction logic
│   ├── ensemble.py               # Ensemble prediction system
│   ├── train.py                  # Model training pipeline
│   └── evaluate.py               # Model evaluation utilities
│
├── tests/
│   └── test_features.py          # Unit tests for feature extraction
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🤖 Machine Learning Models

| Model               | Type                    | Key Strength                          |
|---------------------|-------------------------|---------------------------------------|
| Random Forest       | Ensemble (Bagging)      | Handles non-linear patterns robustly  |
| XGBoost             | Ensemble (Boosting)     | High performance, handles imbalance   |
| Logistic Regression | Linear Classifier       | Fast, interpretable baseline model    |
| LightGBM            | Gradient Boosting       | Speed-optimized for large datasets    |

### 🏆 Ensemble Strategy

All four models vote on each URL. The final prediction is determined by **weighted soft voting**, where each model contributes a probability score. The combined confidence score reflects overall agreement across models.

---

## 🔬 Feature Extraction

The system extracts the following feature categories from each URL:

| Category           | Features                                                           |
|--------------------|--------------------------------------------------------------------|
| **Lexical**        | URL length, number of dots, special characters, digit ratio        |
| **Domain-based**   | Domain age, WHOIS data, IP-based URL, subdomain depth              |
| **Path-based**     | Path length, number of slashes, file extension                     |
| **Security**       | HTTPS presence, SSL certificate validity, redirect count           |
| **Content-based**  | Presence of login forms, external links, favicon mismatch          |

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/phishing-detection.git
cd phishing-detection

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### `requirements.txt`

```
streamlit
scikit-learn
xgboost
lightgbm
pandas
numpy
requests
whois
tldextract
joblib
matplotlib
seaborn
```

---

## 🖥️ Usage

### Run the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

Then open your browser and navigate to `http://localhost:8501`.

### Use the API / Script

```python
from src.feature_extraction import extract_features
from src.ensemble import EnsemblePredictor

predictor = EnsemblePredictor()

url = "http://secure-login.paypa1.com/verify"
features = extract_features(url)
result = predictor.predict(features)

print(f"Prediction : {result['label']}")       # Phishing or Legitimate
print(f"Confidence : {result['confidence']:.2f}%")
```

### Train Models from Scratch

```bash
python src/train.py --data data/processed/dataset.csv --output models/
```

---

## 📊 Results

| Model               | Accuracy | Precision | Recall | F1-Score |
|---------------------|----------|-----------|--------|----------|
| Logistic Regression | 93.1%    | 92.4%     | 91.8%  | 92.1%    |
| Random Forest       | 96.8%    | 97.1%     | 96.3%  | 96.7%    |
| XGBoost             | 97.4%    | 97.6%     | 97.2%  | 97.4%    |
| LightGBM            | 97.2%    | 97.0%     | 97.5%  | 97.2%    |
| **Ensemble**        | **98.1%**| **98.3%** |**97.9%**|**98.1%**|

> ✅ The ensemble model consistently outperforms individual models across all metrics.

---

## 🛠️ Tech Stack

| Layer           | Technology                              |
|-----------------|-----------------------------------------|
| Language        | Python 3.8+                             |
| ML Framework    | scikit-learn, XGBoost, LightGBM         |
| UI              | Streamlit                               |
| Data Processing | Pandas, NumPy                           |
| URL Parsing     | tldextract, urllib                      |
| Visualization   | Matplotlib, Seaborn                     |
| Model Saving    | Joblib                                  |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please make sure to update tests as appropriate and follow the existing code style.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

| Name    | Link                              |
|---------|-----------------------------------|
| GitHub  | [@your-username](https://github.com/your-username) |
| Email   | your.email@example.com            |
| LinkedIn| [your-linkedin](https://linkedin.com/in/your-profile) |

---

<div align="center">
  Made with ❤️ and Python | ⭐ Star this repo if you found it helpful!
</div>
