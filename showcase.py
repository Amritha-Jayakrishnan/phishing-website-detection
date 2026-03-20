import pandas as pd
import joblib

print("🔥 RUNNING SHOWCASE")

# =============================
# Load Dataset
# =============================
data = pd.read_csv("DataFiles/dataset_phishing.csv")

X = data.drop(columns=["url", "status"])
y = data["status"].map({"legitimate": 0, "phishing": 1}).astype(int)

# 🔥 IMPORTANT FIX: ensure training data is numeric
X = X.apply(pd.to_numeric, errors="coerce")
X = X.fillna(0)
X = X.astype(float)

# =============================
# Load Models
# =============================
rf_model = joblib.load("rf_model.pkl")
xgb_model = joblib.load("xgb_model.pkl")

# =============================
# Accuracy on Full Dataset
# =============================
rf_preds = rf_model.predict(X)
xgb_preds = xgb_model.predict(X)

print(f"🌲 Random Forest Accuracy: {(rf_preds == y).mean()*100:.2f}%")
print(f"⚡ XGBoost Accuracy:       {(xgb_preds == y).mean()*100:.2f}%")

print("-" * 60)

# =============================
# Predict Sample URLs
# =============================
sample_rows = data.sample(3, random_state=1)

for _, row in sample_rows.iterrows():
    url = row["url"]

    features = row.drop(labels=["url", "status"]).to_frame().T

    # 🔥 CRITICAL FIX: force numeric dtype for prediction
    features = features.apply(pd.to_numeric, errors="coerce")
    features = features.fillna(0)

    rf_pred = rf_model.predict(features)[0]
    rf_conf = rf_model.predict_proba(features)[0].max()

    xgb_pred = xgb_model.predict(features)[0]
    xgb_conf = xgb_model.predict_proba(features)[0].max()

    print(f"URL: {url}")
    print(f"  Random Forest → {'PHISHING' if rf_pred else 'LEGITIMATE'} ({rf_conf:.2f})")
    print(f"  XGBoost       → {'PHISHING' if xgb_pred else 'LEGITIMATE'} ({xgb_conf:.2f})")
    print("-" * 60)
