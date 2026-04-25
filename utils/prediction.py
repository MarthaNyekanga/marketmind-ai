def predict_demand(df, product):
    product_data = df[df["product"] == product]

    if len(product_data) < 3:
        return "Not enough data"

    return round(product_data["quantity_sold"].rolling(3).mean().iloc[-1], 2)