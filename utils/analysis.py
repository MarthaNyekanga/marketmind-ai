import pandas as pd

def sales_summary(df):
    df["revenue"] = df["quantity_sold"] * df["price"]
    total_sales = df["revenue"].sum()
    best_product = df.groupby("product")["quantity_sold"].sum().idxmax()
    return total_sales, best_product