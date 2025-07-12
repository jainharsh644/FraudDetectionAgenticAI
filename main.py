import pandas as pd
from langgraph.graph import StateGraph, END
from src.cleaning import clean_data
from src.feature_engineering import engineer_features
from src.scaling import scale_features
from src.rules import apply_rules
from src.ml_pipeline import train_ml
from src.shap_explain import explain_model
from src.agent_mcp import rule_tuner_agent
from src.memory_agent import memory_agent
from src.rule_check_agent import rule_check_agent

# -------------------------
# Define agents (nodes)
# -------------------------

def cleaner_agent(state):
    df = state["df"]
    state["df"] = clean_data(df)
    print(f"✅ After CleanerAgent: shape {state['df'].shape}")
    return state

def feature_engineer_agent(state):
    df = state["df"]
    state["df"] = engineer_features(df)
    print(f"✅ After FeatureEngineerAgent: columns {list(state['df'].columns)}")
    return state

def scaler_agent(state):
    df = state["df"]
    features = ["amount","txn_hour","txn_count_24h","device_usage_count"]
    state["df"] = scale_features(df, features)
    print(f"✅ After ScalerAgent: scaled features {features}")
    return state

def rule_engine_agent(state):
    df = state["df"]
    state["df"] = apply_rules(df)
    print(f"✅ After RuleEngineAgent: fraud flags sum = {state['df']['rule_flag'].sum()}")
    return state

def ml_model_agent(state):
    df = state["df"]
    df, model = train_ml(df)
    state["df"] = df
    state["model"] = model
    print(f"✅ After MLModelAgent: trained model, fraud preds sum = {df['ml_pred'].sum()}")
    return state

def shap_agent(state):
    explain_model(state["model"], state["df"])
    print("✅ After SHAPAgent: saved SHAP summary plots")
    return state

# -------------------------
# Build LangGraph pipeline
# -------------------------

graph = StateGraph(dict)

graph.add_node("CleanerAgent", cleaner_agent)
graph.add_node("FeatureEngineerAgent", feature_engineer_agent)
graph.add_node("ScalerAgent", scaler_agent)
graph.add_node("RuleEngineAgent", rule_engine_agent)
graph.add_node("MemoryAgent", memory_agent)
graph.add_node("MLModelAgent", ml_model_agent)
graph.add_node("SHAPAgent", shap_agent)
graph.add_node("RuleTunerAgent", rule_tuner_agent)
graph.add_node("RuleCheckAgent", rule_check_agent)

graph.set_entry_point("CleanerAgent")
graph.add_edge("CleanerAgent", "FeatureEngineerAgent")
graph.add_edge("FeatureEngineerAgent", "ScalerAgent")
graph.add_edge("ScalerAgent", "RuleEngineAgent")
graph.add_edge("RuleEngineAgent", "MemoryAgent")
graph.add_edge("MemoryAgent", "MLModelAgent")
graph.add_edge("MLModelAgent", "SHAPAgent")
graph.add_edge("SHAPAgent", "RuleTunerAgent")
graph.add_edge("RuleTunerAgent", "RuleCheckAgent")
graph.add_edge("RuleCheckAgent", END)

pipeline = graph.compile()

# -------------------------
# Run the pipeline
# -------------------------

result = pipeline.invoke({
    "df": pd.read_csv("data/fraud_dataset.csv", encoding='latin1', on_bad_lines='skip')
})

# Save predictions
result["df"].to_csv("outputs/final_predictions.csv", index=False)
print("✅ Saved final predictions to outputs/final_predictions.csv")

# -------------------------
# Print agent outputs
# -------------------------

print("\n✅ Agent suggests new rules:\n")
print(result["suggestion"].content)

print("\n✅ Code review by AI on the new rules:\n")
print(result["review"].content)
