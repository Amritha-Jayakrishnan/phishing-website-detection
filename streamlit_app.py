import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

from URLFeatureExtraction import extract_features

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="PHISHSAFE – Phishing Detection",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 PHISHSAFE")
st.subheader("AI-Powered Phishing Website Detection")
st.write("Enter any URL to check whether it is **LEGITIMATE** or **PHISHING**.")

# ── Load models ───────────────────────────────────────────
@st.cache_resource
def load_models():
    rf   = joblib.load("rf_model.pkl")
    xgb  = joblib.load("xgb_model.pkl")
    log  = joblib.load("log_model.pkl")
    lgb  = joblib.load("lgb_model.pkl")
    sc   = joblib.load("scaler.pkl")
    return rf, xgb, log, lgb, sc

rf_model, xgb_model, log_model, lgb_model, scaler = load_models()

# SHAP explainer (XGBoost)
explainer = shap.TreeExplainer(xgb_model)

# Feature column order (must match training)
data = pd.read_csv("DataFiles/dataset_phishing.csv")
FEATURE_COLUMNS = data.drop(columns=["url", "status"]).columns

# ── URL input ─────────────────────────────────────────────
url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")

# ── Prediction ────────────────────────────────────────────
if st.button("🔍 Analyze URL"):

    if url.strip() == "":
        st.warning("⚠️ Please enter a valid URL.")
        st.stop()

    with st.spinner("Analyzing URL..."):

        # Extract features
        features = extract_features(url)
        df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

        # Scale for logistic regression
        df_scaled = scaler.transform(df)

        # Individual model probabilities (phishing = class 1)
        rf_prob  = rf_model.predict_proba(df)[0][1]
        xgb_prob = xgb_model.predict_proba(df)[0][1]
        log_prob = log_model.predict_proba(df_scaled)[0][1]
        lgb_prob = lgb_model.predict_proba(df)[0][1]

        # Weighted ensemble score
        final_score = (
            0.35 * xgb_prob +
            0.30 * lgb_prob +
            0.20 * rf_prob  +
            0.15 * log_prob
        )

        final_prediction = "PHISHING" if final_score >= 0.5 else "LEGITIMATE"
        confidence = final_score if final_score >= 0.5 else (1 - final_score)

    # ── Results ───────────────────────────────────────────
    st.divider()
    st.subheader("🔍 Final Verdict")

    if final_prediction == "PHISHING":
        st.error(f"🚨 **PHISHING WEBSITE DETECTED**\n\nConfidence: **{confidence:.2f}**")
    else:
        st.success(f"✅ **LEGITIMATE WEBSITE**\n\nConfidence: **{confidence:.2f}**")

    # Risk score meter
    st.subheader("📊 Risk Score")
    st.progress(int(final_score * 100))
    st.caption(f"Phishing risk: {final_score * 100:.1f}%")

    # Model comparison table
    st.subheader("📈 Individual Model Scores")
    st.table({
        "Model": ["Random Forest", "XGBoost", "LightGBM", "Logistic Regression"],
        "Phishing Probability": [
            f"{rf_prob:.4f}",
            f"{xgb_prob:.4f}",
            f"{lgb_prob:.4f}",
            f"{log_prob:.4f}"
        ]
    })

    # SHAP explanation
    st.subheader("🧠 Why did the model decide this?")
    try:
        shap_values = explainer.shap_values(df)
        fig, ax = plt.subplots()
        shap.summary_plot(shap_values, df, plot_type="bar", show=False)
        st.pyplot(fig)
        plt.close()
    except Exception as e:
        st.info("SHAP explanation unavailable for this URL.")

    # How it works
    with st.expander("ℹ️ How does this work?"):
        st.write("""
        - The system extracts **87 URL-based features** (length, special characters,
          domain age, HTTPS usage, suspicious keywords, etc.)
        - Four ML models analyze the features: **Random Forest**, **XGBoost**,
          **LightGBM**, and **Logistic Regression**
        - A **weighted ensemble** combines all four predictions for the final verdict
        - **SHAP values** explain which features influenced the decision most
        - ⚠️ Note: complex legitimate URLs (e.g. long paths with parameters) may
          occasionally be flagged due to structural similarity with phishing patterns
        """)
