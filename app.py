import streamlit as st
import pandas as pd
import os
from openai import OpenAI

from utils.cleaner import clean_data
from utils.analysis import sales_summary
from utils.prediction import predict_demand

# 🔑 API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="MarketMind AI", layout="centered")

st.title("📊 MarketMind AI Assistant")
st.markdown("### Upload your sales file to get insights, predictions, and AI advice")

st.divider()

# Upload file
file = st.file_uploader("Upload your sales data", type=["csv", "xlsx", "xls"])

if file:
    # 📂 Read file
    file_type = file.name.split(".")[-1]

    try:
        if file_type == "csv":
            df = pd.read_csv(file)
        elif file_type in ["xlsx", "xls"]:
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type")
            st.stop()

        # 🧹 Clean data
        df = clean_data(df)

    except Exception:
        st.error("Error processing file. Please check format.")
        st.stop()

    # 🧹 Show cleaned data
    st.subheader("🧹 Cleaned Data Preview")
    st.write(df.head())

    st.subheader("📋 Detected Columns")
    st.write(df.columns)

    # 💾 Download cleaned data
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download cleaned data",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )

    st.divider()

    # ✅ Check required columns
    required_columns = ["product", "quantity_sold", "price"]

    if all(col in df.columns for col in required_columns):

        # 📊 Sales Summary
        total_sales, best_product = sales_summary(df)

        st.subheader("📈 Sales Overview")

        col1, col2 = st.columns(2)
        col1.metric("Total Revenue", f"{total_sales:,.2f}")
        col2.metric("Best Product", best_product)

        st.divider()

        # 📊 Graph
        st.subheader("📊 Sales by Product")
        product_sales = df.groupby("product")["quantity_sold"].sum()
        st.bar_chart(product_sales)

        st.divider()

        # 🔮 Prediction
        st.subheader("🔮 Demand Prediction")
        product = st.selectbox("Select product", df["product"].unique())

        prediction = predict_demand(df, product)
        st.write(f"Predicted demand: {prediction}")

        st.divider()

        # 🤖 Auto AI Insights
        st.subheader("🤖 AI Business Insights")

        try:
            sample_data = df.head(10).to_string()

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{
                    "role": "user",
                    "content": f"""
Analyze this sales data and give:
- 3 key insights
- 2 actionable recommendations

Data:
{sample_data}

Keep it simple and practical.
"""
                }]
            )

            insights = response.choices[0].message.content
            st.write(insights)

        except Exception as e:
            st.warning("AI insights temporarily unavailable")

        st.divider()

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

Give simple, practical advice.
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

    else:
        st.warning("⚠️ Your file is missing required columns.")
        st.write("Detected columns:")
        st.write(df.columns)
        st.info("We expect: product, quantity_sold, price")

else:
    st.info("Please upload a sales data file to continue.")