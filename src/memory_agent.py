import json
import os
import pandas as pd

MEMORY_FILE = "outputs/memory.json"

def memory_agent(state):
    df = state["df"]
    flagged = df[df["rule_flag"]==1].to_dict(orient="records")

    # Ensure JSON serializable
    for row in flagged:
        for key, value in row.items():
            if isinstance(value, pd.Timestamp):
                row[key] = value.strftime("%Y-%m-%d %H:%M:%S")

    # Try to load memory
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON detected in memory file. Starting fresh.")
            memory = []
    else:
        memory = []

    # Append new
    memory.extend(flagged)

    # Write back
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

    print(f"✅ MemoryAgent: stored {len(memory)} flagged transactions across runs.")
    state["memory"] = memory
    return state
