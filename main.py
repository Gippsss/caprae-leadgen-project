import os
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from enrich import enrich_domain

# Configurable parameters
MAX_WORKERS = 10        # Adjust based on your system
RETRY_LIMIT = 2         # Retry failed domains up to 2 times
SAVE_INTERVAL = 100     # Save progress every 100 domains
OUTPUT_FILE = "output/enriched.csv"
FAILED_FILE = "output/failed_domains.csv"

def enrich_with_retry(domain):
    """Run enrichment with retries for robustness."""
    for attempt in range(RETRY_LIMIT + 1):
        try:
            result = enrich_domain(domain)
            if result and result.get("score", 0) >= 0:
                return result
        except Exception as e:
            print(f"⚠️ Error on {domain} (attempt {attempt+1}): {e}")
        time.sleep(1)
    # Return a consistent empty entry if all retries fail
    return {"domain": domain, "industry": "Unknown", "contact_links": [], "found_emails": [], "score": 0}

def run_enrichment_parallel(df_input, max_workers=MAX_WORKERS, timeout=30, progress_callback=None):
    """
    Run domain enrichment in parallel with progress updates.
    Now compatible with Streamlit (returns DataFrame directly).
    """
    os.makedirs("output", exist_ok=True)

    if "website" not in df_input.columns:
        raise ValueError("CSV must contain a 'website' column")

    processed_domains = set()
    if os.path.exists(OUTPUT_FILE):
        existing = pd.read_csv(OUTPUT_FILE)
        processed_domains = set(existing["domain"])
        print(f"🔁 Resuming... Found {len(processed_domains)} domains already processed.")

    to_process = [d for d in df_input["website"].astype(str) if d not in processed_domains]
    total = len(to_process)
    print(f"🚀 Starting enrichment for {total} new domains...")

    results, failed = [], []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_domain = {executor.submit(enrich_with_retry, domain): domain for domain in to_process}

        for i, future in enumerate(as_completed(future_to_domain), 1):
            domain = future_to_domain[future]
            try:
                result = future.result(timeout=timeout)
                results.append(result)
                print(f"✅ {i}/{total} Done: {domain} (Score: {result['score']})")
            except Exception as e:
                print(f"❌ Failed: {domain} ({e})")
                failed.append(domain)

            # 🔹 Stream progress to Streamlit
            if progress_callback:
                progress_callback(i, total)

            # 🔹 Periodic save to prevent data loss
            if i % SAVE_INTERVAL == 0:
                save_partial(results, failed)

    save_partial(results, failed)
    total_time = time.time() - start_time
    print(f"\n🎉 Enrichment complete in {total_time/60:.2f} minutes!")

    # ✅ Return final DataFrame instead of raw list
    return pd.DataFrame(results)

def save_partial(results, failed):
    """Save intermediate results and failed logs."""
    if results:
        pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)
        print(f"💾 Saved {len(results)} results to {OUTPUT_FILE}")
    if failed:
        pd.DataFrame({"domain": failed}).to_csv(FAILED_FILE, index=False)
        print(f"⚠️ Logged {len(failed)} failed domains to {FAILED_FILE}")

if __name__ == "__main__":
    INPUT_CSV = "yc_companies.csv"  # Change this to your input file
    df = pd.read_csv(INPUT_CSV)
    run_enrichment_parallel(df)
