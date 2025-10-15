# app.py
import streamlit as st
import pandas as pd
from main import run_leadgen  # import your refactored main function

st.set_page_config(page_title="Caprae LeadGen Tool", page_icon="🚀", layout="wide")

# App title and description
st.title("🚀 Caprae LeadGen Project")
st.write("""
This tool identifies and enriches potential leads from company datasets.
Upload your CSV below, and the tool will process it to generate enriched results.
""")

# File uploader
uploaded_file = st.file_uploader("Upload your input CSV (e.g., yc_companies.csv)", type="csv")

if uploaded_file is not None:
    # Preview uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write("### Input Preview:")
    st.dataframe(df.head())

    if st.button("Run Lead Generation Tool"):
        with st.spinner("Processing your file... ⏳"):
            try:
                # Call the lead generation function
                result_df, output_path = run_leadgen(uploaded_file)

                st.success("✅ Lead generation completed!")
                st.write("### Output Preview:")
                st.dataframe(result_df.head())

                # Download button for output CSV
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="Download Enriched CSV",
                        data=f,
                        file_name="enriched.csv",
                        mime="text/csv"
                    )

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
