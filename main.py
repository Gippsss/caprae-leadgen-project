# main.py
import pandas as pd
from enrich import enrich_from_csv

def run_leadgen(df_input):
    """
    Processes a DataFrame (from uploaded CSV) and returns the enriched DataFrame.
    Completely in-memory; no temp files required.
    """
    # Assume enrich_from_csv can accept a DataFrame instead of a file path
    # If your current enrich_from_csv only accepts file paths, we can create a wrapper
    enriched_df = enrich_from_csv(df_input)

    return enriched_df
