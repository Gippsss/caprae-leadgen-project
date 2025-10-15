# main.py
import os
import pandas as pd
from enrich import enrich_from_csv  # keep your existing enrichment logic

def run_leadgen(input_file):
    """
    Processes the CSV using enrich_from_csv and returns a DataFrame
    along with the output CSV path.
    """
    output_path = "output/enriched.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Run your existing enrichment function
    df = enrich_from_csv(input_file, output_path)

    return df, output_path  # return both DataFrame and CSV path
