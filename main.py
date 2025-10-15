# main.py
import pandas as pd
from enrich import enrich_domain  # import the actual domain enrichment function

def run_leadgen(df_input):
    """
    Processes a DataFrame from Streamlit upload and returns the enriched DataFrame.
    Works fully in-memory and keeps your original scoring logic.
    """
    df_input = df_input.copy()
    results = []

    # Use 'website' column for domains (matches your original logic)
    for domain in df_input['website'].astype(str):
        result = enrich_domain(domain)
        results.append(result)

    enriched_df = pd.DataFrame(results)
    return enriched_df
