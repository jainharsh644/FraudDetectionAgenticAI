def apply_rules(df):
    df['rule_flag'] = (
        ((df['amount'] > 5000) & (df['country'].isin(["RU","NG","CN","PK"]))) |
        ((df['night_txn'] == 1) & (df['amount'] > 2000)) |
        (df['txn_count_24h'] > 5) |
        (df['geo_mismatch'] == 1) |
        ((df['risky_category'] == 1) & (df['device_usage_count'] > 3))
    ).astype(int)
    return df
