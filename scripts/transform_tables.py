import pandas as pd
import os

CHUNK_SIZE = 200000
os.makedirs("data/clean", exist_ok=True)

# =========================
# PATENTS
# =========================
print("Cleaning patents...")

out_file = "data/clean/patents.csv"
first = True
total = 0

for chunk in pd.read_csv(
    "data/raw/g_patent.tsv.zip",
    sep="\t",
    compression="zip",
    dtype=str,
    chunksize=CHUNK_SIZE,
    low_memory=False,
    on_bad_lines="skip"
):
    chunk = chunk[["patent_id", "patent_title", "patent_date"]]

    chunk["year"] = chunk["patent_date"].str[:4]
    chunk.rename(columns={"patent_title": "title"}, inplace=True)

    chunk.to_csv(out_file, mode="w" if first else "a", index=False, header=first)
    first = False

    total += len(chunk)
    if total % 200000 == 0:
        print(f"Processed {total:,} rows...")

print("patents cleaned")


# =========================
# INVENTORS
# =========================
print("Cleaning inventors...")

inv = pd.read_csv(
    "data/raw/g_inventor_disambiguated.tsv.zip",
    sep="\t",
    compression="zip",
    dtype=str
)

inv["name"] = (
    inv["disambig_inventor_name_first"].fillna("") + " " +
    inv["disambig_inventor_name_last"].fillna("")
).str.strip()

inv[["inventor_id", "name"]].to_csv("data/clean/inventors.csv", index=False)

print("inventors cleaned")


# =========================
# PATENT-INVENTOR RELATIONSHIP
# =========================
print("Creating patent-inventor relationships...")

out_file = "data/clean/patent_inventor.csv"
first = True
total = 0

for chunk in pd.read_csv(
    "data/raw/g_inventor_disambiguated.tsv.zip",
    sep="\t",
    compression="zip",
    dtype=str,
    chunksize=CHUNK_SIZE
):
    chunk = chunk[["patent_id", "inventor_id"]]

    chunk.to_csv(out_file, mode="w" if first else "a", index=False, header=first)
    first = False

    total += len(chunk)
    if total % 200000 == 0:
        print(f"Processed {total:,} rows...")

print("patent-inventor relationships created")


# =========================
# COMPANIES
# =========================
print("Cleaning companies...")

comp = pd.read_csv(
    "data/raw/g_assignee_disambiguated.tsv.zip",
    sep="\t",
    compression="zip",
    dtype=str
)

comp["name"] = comp["disambig_assignee_organization"].fillna("Unknown")

comp[["patent_id", "name"]].to_csv("data/clean/companies.csv", index=False)

print("companies cleaned")

print("\nTRANSFORM COMPLETE")