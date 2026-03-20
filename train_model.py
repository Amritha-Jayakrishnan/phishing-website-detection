import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

print("\n🚀 TRAINING PHISHING DETECTION MODELS\n")

# ── Load dataset ──────────────────────────────────────────
print("📂 Loading dataset...")
df = pd.read_csv("DataFiles/dataset_phishing.csv")
print("✅ Dataset loaded successfully")
print(f"   Shape: {df.shape}")

# ── Features and labels ───────────────────────────────────
X = df.drop(columns=["status", "url"])
y = df["status"].map({"legitimate": 0, "phishing": 1}).astype(int)

# Ensure all features are numeric
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

# ── Train / test split ────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ── Feature scaling (for Logistic Regression only) ────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── Train models ──────────────────────────────────────────
print("\n🔄 Training models...")

rf_model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

xgb_model = XGBClassifier(
    n_estimators=200, max_depth=6, learning_rate=0.1,
    eval_metric="logloss", random_state=42, verbosity=0
)
xgb_model.fit(X_train, y_train)

log_model = LogisticRegression(max_iter=2000, solver="lbfgs")
log_model.fit(X_train_scaled, y_train)

lgb_model = LGBMClassifier(n_estimators=200, learning_rate=0.1,
                            random_state=42, verbose=-1)
lgb_model.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────
rf_acc  = accuracy_score(y_test, rf_model.predict(X_test))
xgb_acc = accuracy_score(y_test, xgb_model.predict(X_test))
log_acc = accuracy_score(y_test, log_model.predict(X_test_scaled))
lgb_acc = accuracy_score(y_test, lgb_model.predict(X_test))

print("\n📊 MODEL PERFORMANCE SUMMARY\n")
print(f"   🌲 Random Forest        : {rf_acc  * 100:.2f}%")
print(f"   ⚡ XGBoost              : {xgb_acc * 100:.2f}%")
print(f"   🧠 Logistic Regression  : {log_acc * 100:.2f}%")
print(f"   🚀 LightGBM             : {lgb_acc * 100:.2f}%")

# ── Save models ───────────────────────────────────────────
joblib.dump(rf_model,  "rf_model.pkl")
joblib.dump(xgb_model, "xgb_model.pkl")
joblib.dump(log_model, "log_model.pkl")
joblib.dump(lgb_model, "lgb_model.pkl")
joblib.dump(scaler,    "scaler.pkl")

print("\n✅ All models trained and saved successfully!\n")
