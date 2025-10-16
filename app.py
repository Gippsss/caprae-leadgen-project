# app.py
import streamlit as st
import pandas as pd
import time
from main import run_enrichment_parallel  # ✅ correct import

st.set_page_config(page_title="Caprae LeadGen Tool", page_icon="🚀", layout="wide")

st.title("🚀 Caprae LeadGen Project")
st.write("""
This tool identifies and enriches potential leads from company datasets.
Upload your CSV below, and the tool will process it to generate enriched results.
""")

uploaded_file = st.file_uploader("Upload your input CSV (must have a 'website' column)", type="csv")

if uploaded_file is not None:
    df_input = pd.read_csv(uploaded_file)
    st.write("### 📊 Input Preview:")
    st.dataframe(df_input.head())

    st.info(f"Detected **{len(df_input)}** rows in the dataset.")
    max_threads = st.number_input("🧵 Max parallel threads", min_value=1, max_value=50, value=10, step=1)
    timeout_per_task = st.number_input("⏱️ Timeout per website (seconds)", min_value=5, max_value=120, value=30, step=5)

    if st.button("🚀 Run Lead Generation Tool"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        start_time = time.time()
        st.info("Processing your file... this may take a few minutes ⏳")

        try:
            # Stream progress updates
            enriched_df = run_enrichment_parallel(
                df_input,
                max_workers=max_threads,
                timeout=timeout_per_task,
                progress_callback=lambda done, total: progress_bar.progress(done / total)
            )

            elapsed_time = time.time() - start_time
            st.success(f"✅ Lead generation completed in {elapsed_time:.2f} seconds!")

            st.write("### 🧾 Output Preview:")
            st.dataframe(enriched_df.head())

            csv_data = enriched_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Enriched CSV",
                data=csv_data,
                file_name="enriched_results.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
            st.stop()

