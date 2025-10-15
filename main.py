# main.py
import os
import argparse
from enrich import enrich_from_csv

def main():
    parser = argparse.ArgumentParser(description="Caprae LeadGen Enrichment Tool")
    parser.add_argument('--input', required=True, help='Path to input CSV with column "domain"')
    parser.add_argument('--output', default='output/enriched.csv', help='Path to save output CSV')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df = enrich_from_csv(args.input, args.output)
    print("\n✅ Enrichment complete! Saved to", args.output)
    print(df.head())

if __name__ == "__main__":
    main()
