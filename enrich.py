# enrich.py
def enrich_from_csv(input_data):
    """
    Accepts either a file path (str) or a DataFrame.
    Returns enriched DataFrame.
    """
    if isinstance(input_data, str):
        df = pd.read_csv(input_data)
    else:
        df = input_data.copy()

    # ... your enrichment logic ...
    # For example:
    df['Score'] = range(1, len(df) + 1)

    return df
