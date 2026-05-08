import pandas as pd
import os

CHUNK_SIZE = 200000
OUTPUT_FILE = "data/raw/patents_full.csv"

def extract_patents():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    first = True

    usecols = [
        "patent_id",
        "patent_title",
        "patent_date"
    ]

    for chunk in pd.read_csv(
        "data/raw/g_patent.tsv.zip",
        sep="\t",
        compression="zip",
        chunksize=CHUNK_SIZE,
        usecols=usecols,
        dtype=str,
        engine="python",
        on_bad_lines="skip"
    ):
        chunk.to_csv(
            OUTPUT_FILE,
            mode="a",
            index=False,
            header=first
        )
        first = False
        print(f"Processed {len(chunk)} rows...")

    print("Full patents extracted")


if __name__ == "__main__":
    extract_patents()