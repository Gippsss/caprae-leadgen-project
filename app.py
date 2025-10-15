# app.py
import streamlit as st
import pandas as pd
from main import run_leadgen

st.set_page_config(page_title="Caprae LeadGen Tool", page_icon="🚀", layout="wide")

st.title("🚀 Caprae LeadGen Project")
st.write("""
This tool identifies and enriches potential leads from company datasets.
Upload your CSV below, and the tool will process it to generate enriched results.
""")

uploaded_file = st.file_uploader("Upload your input CSV (e.g., yc_companies.csv)", type="csv")

if uploaded_file is not None:
    # Read uploaded CSV directly
    df_input = pd.read_csv(uploaded_file)
    st.write("### Input Preview:")
    st.dataframe(df_input.head())

    if st.button("Run Lead Generation Tool"):
        with st.spinner("Processing your file... ⏳"):
            try:
                # Run lead generation in-memory
                result_df = run_leadgen(df_input)
                st.success("✅ Lead generation completed!")
                st.write("### Output Preview:")
                st.dataframe(result_df.head())

                # Provide download button
                csv_data = result_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Enriched CSV",
                    data=csv_data,
                    file_name="enriched.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
