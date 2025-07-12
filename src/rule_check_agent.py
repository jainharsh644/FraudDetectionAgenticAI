from langchain_groq import ChatGroq

llm = ChatGroq(model="llama3-8b-8192", api_key="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")

def rule_check_agent(state):
    generated_rules = state.get("suggestion").content
    review = llm.invoke(
        f"""Please review the following Python fraud detection rules for correctness, efficiency,
        and suggest improvements as needed:\n\n{generated_rules}"""
    )
    state["review"] = review
    print("✅ RuleCheckAgent review complete.")
    return state
