def detect_outliers_grouped(df, column, group_cols):
    df["outlier"] = df.groupby(group_cols)[column].transform(
        lambda x:
            (x < x.quantile(0.25) - 1.5 * (x.quantile(0.75) - x.quantile(0.25))) |
            (x > x.quantile(0.75) + 1.5 * (x.quantile(0.75) - x.quantile(0.25)))
    )
    return df