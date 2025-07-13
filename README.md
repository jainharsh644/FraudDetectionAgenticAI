# 🚀 Agentic AI for Fraud Detection

---

## 📌 Problem Statement

Traditional fraud detection systems often rely on rigid, static rules that fail to adapt as fraud patterns evolve. Fraudsters continually change tactics, causing businesses to lose millions.

We need:
- A fraud detection system that blends static rules and dynamic learning.
- The ability to automatically propose and refine fraud detection strategies as patterns change.
- Memory to keep track of suspicious transactions over time.
- Full transparency and explainability to satisfy compliance and risk teams.

---

## 🎯 Goals & Objectives

✅ Build an **end-to-end fraud detection system** that:
- Cleans and prepares transaction data.
- Performs feature engineering to surface hidden fraud patterns.
- Applies initial rule-based checks to detect suspicious activity.
- Trains a machine learning model to predict fraud probability.
- Uses SHAP to explain why the model makes certain decisions.
- Employs **Agentic AI** to:
  - Generate new fraud detection rules automatically.
  - Review and refine these rules for correctness and efficiency.
- Maintains a memory of suspicious transactions across runs to learn over time.

---

## 🛠️ Approach & Solution

This project is built around a **multi-agent control plane (MCP) architecture**, implemented using `LangGraph`. Each stage of the pipeline acts as an intelligent agent responsible for a specific step:

- **Data Cleaning:** Removes duplicates and handles missing data.
- **Feature Engineering:** Creates fraud-focused features like transaction frequency, night-time indicators, geo mismatches, and device usage anomalies.
- **Feature Scaling:** Standardizes numerical features for effective ML training.
- **Rule Engine:** Applies initial hard-coded rules to flag suspicious transactions.
- **Memory:** Maintains a JSON-based long-term memory of flagged suspicious transactions across multiple runs.
- **ML Modeling:** Trains a RandomForest classifier to predict fraud likelihood.
- **Explainability:** Generates SHAP summary plots to visualize which features drive fraud predictions.
- **Agentic Rule Tuning:** Uses a language model (via Groq) to generate new Python fraud detection rules based on recent suspicious transactions.
- **Agentic Rule Review:** Passes these rules to another agent to review for code quality, efficiency, style, and adds type hints & docstrings.

---

## 📈 Outputs & What to Expect

After running the pipeline, you will see:

- ✅ **CSV output:**  
  A file with final fraud predictions and probabilities, saved in `outputs/final_predictions.csv`.

- ✅ **JSON memory:**  
  A file `outputs/memory.json` that accumulates flagged suspicious transactions across multiple runs, giving the system long-term memory.

---

## 🚀 Future Enhancements

- ➕ Replace the RandomForest with gradient boosting models like **XGBoost** or **LightGBM** to capture more complex fraud patterns.
- ➕ Use a vector store to let your agents retrieve historical fraud examples, creating even more sophisticated rule sets.
