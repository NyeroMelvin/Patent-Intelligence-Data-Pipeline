import pandas as pd

# Check inventor file
df = pd.read_csv(
    "data/raw/g_inventor_disambiguated.tsv.zip",
    sep="\t",
    compression="zip",
    nrows=5
)

print("\nCOLUMNS IN INVENTOR FILE:\n")
print(list(df.columns))

print("\nSAMPLE DATA:\n")
print(df.head())

# Check companies file
df = pd.read_csv(
    "data/raw/g_assignee_disambiguated.tsv.zip",
    sep="\t",
    compression="zip",
    nrows=5
)

print("\nCOLUMNS IN COMPANY FILE:\n")
print(list(df.columns))


df = pd.read_csv(
    "data/raw/g_patent.tsv.zip",
    sep="\t",
    compression="zip",
    nrows=5,          # 🔥 only load 5 rows
    dtype=str,
    engine="python"
)

print(df.head())
print("\nColumns:\n", df.columns.tolist())

print("\nSAMPLE DATA:\n")
print(df.head())