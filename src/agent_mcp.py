# src/agent_mcp.py
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

llm = ChatGroq(model="llama3-8b-8192", api_key="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")

def rule_tuner_agent(state):
    df = state["df"]
    suspicious = df[df["rule_flag"]==1].head(5).to_dict(orient="records")
    suggestion = llm.invoke(
        f"""Given these flagged transactions: {suspicious},
        propose improved Python fraud detection rules as code snippets."""
    )
    state["suggestion"] = suggestion
    return state
