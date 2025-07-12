import shap
import matplotlib.pyplot as plt

def explain_model(model, df):
    X = df[["amount","txn_hour","txn_count_24h","device_usage_count","geo_mismatch","night_txn","risky_category"]]
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    
    # BAR PLOT
    plt.figure()
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.savefig("outputs/shap_summary_bar.png")
    plt.close()

    # CLASSIC BEESWARM PLOT
    plt.figure()
    shap.summary_plot(shap_values, X, plot_type="dot", show=False)
    plt.savefig("outputs/shap_summary_beeswarm.png")
    plt.close()
