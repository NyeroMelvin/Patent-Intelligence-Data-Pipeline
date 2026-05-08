import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set a professional style
sns.set_theme(style="whitegrid")
DB_PATH = "data/patents.db"

def generate_visuals():
    conn = sqlite3.connect(DB_PATH)

    # --- CHART 1: TOP COMPANIES (Bar Chart) ---
    print("Generating Company Chart...")
    df_comp = pd.read_sql("SELECT name, patents FROM company_summary ORDER BY patents DESC LIMIT 10", conn)
    
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(data=df_comp, x="patents", y="name", palette="viridis")
    plt.title("Top 10 Global Patent Holders", fontsize=16)
    plt.xlabel("Number of Patents")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("outputs/top_companies.png")
    plt.close()

    # --- CHART 2: YEARLY TRENDS (Line Chart) ---
    print("Generating Trends Chart...")
    df_trends = pd.read_sql("SELECT year, patents FROM yearly_trends WHERE year > 2000 ORDER BY year", conn)
    
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df_trends, x="year", y="patents", marker="o", color="teal", linewidth=2.5)
    plt.title("Patent Application Trends (2000 - 2025)", fontsize=16)
    plt.fill_between(df_trends["year"], df_trends["patents"], color="teal", alpha=0.1)
    plt.xlabel("Year")
    plt.ylabel("Total Patents")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("outputs/yearly_trends.png")
    plt.close()

    # --- CHART 3: TOP INVENTORS (Horizontal Bar Chart) ---
    print("Generating Inventor Chart...")
    df_inv = pd.read_sql("SELECT name, patents FROM inventor_summary ORDER BY patents DESC LIMIT 5", conn)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df_inv, x="patents", y="name", color="coral")
    plt.title("Top 5 Prolific Inventors", fontsize=14)
    plt.tight_layout()
    plt.savefig("outputs/top_inventors.png")
    plt.close()

    conn.close()
    print("Visualizations saved to the 'outputs/' folder!")

if __name__ == "__main__":
    import os
    if not os.path.exists("outputs"): os.makedirs("outputs")
    generate_visuals()