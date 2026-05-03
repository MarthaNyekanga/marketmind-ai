import pandas as pd

def clean_data(df):
    # Convert all column names to lowercase
    df.columns = [col.lower().strip() for col in df.columns]

    # Possible column name variations
    column_map = {
        "product": ["product", "item", "description", "name"],
        "quantity_sold": ["quantity", "qty", "units", "quantity_sold"],
        "price": ["price", "amount", "unit_price", "value"]
    }

    new_df = pd.DataFrame()

    for standard_col, possible_names in column_map.items():
        for name in possible_names:
            if name in df.columns:
                new_df[standard_col] = df[name]
                break

    return new_df