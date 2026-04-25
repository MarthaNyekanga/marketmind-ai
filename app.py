import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# Import your modules
from utils.analysis import sales_summary
from utils.prediction import predict_demand

# 🔑 Secure API key (better practice)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="MarketMind AI", layout="centered")

st.title("📊 MarketMind AI Assistant")
st.write("Helping small businesses make smarter decisions")

# Upload data
file = st.file_uploader("Upload your sales data", type=["csv"])

if file:
    df = pd.read_csv(file)

    # 📊 Use your analysis function
    total_sales, best_product = sales_summary(df)

    st.subheader("📈 Sales Summary")
    st.write(f"Total Revenue: {total_sales}")
    st.write(f"Best Selling Product: {best_product}")

    # 🔮 Prediction
    st.subheader("🔮 Demand Prediction")
    product = st.selectbox("Select product", df["product"].unique())

    prediction = predict_demand(df, product)
    st.write(f"Predicted demand: {prediction}")

    # 💬 AI Chat
    st.subheader("💬 Ask MarketMind AI")
    question = st.text_input("Ask a business question")

    if question:
        prompt = f"""
You are a helpful assistant for small market traders.

Data summary:
Total sales: {total_sales}
Best product: {best_product}

User question:
{question}

Give simple, practical advice. Avoid complex terms.
Explain your reasoning briefly.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            answer = response.choices[0].message.content
            st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")