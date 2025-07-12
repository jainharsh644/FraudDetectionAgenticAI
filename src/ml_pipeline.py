from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_ml(df):
    X = df[["amount","txn_hour","night_txn","txn_count_24h",
            "geo_mismatch","risky_category","device_usage_count"]]
    y = df["is_fraud"]
    X_train, X_test, y_train, y_test = train_test_split(X,y,stratify=y,test_size=0.3,random_state=42)
    model = RandomForestClassifier(n_estimators=100,random_state=42,class_weight='balanced')
    model.fit(X_train,y_train)
    joblib.dump(model, "outputs/fraud_model.pkl")
    df["ml_pred"] = model.predict(X)
    df["ml_prob"] = model.predict_proba(X)[:,1]
    return df, model
