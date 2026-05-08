import sqlite3
import pandas as pd
import os

DB_PATH = "data/patents.db"

def run_database_build():
    
    os.makedirs("data", exist_ok=True)

   
    tables = {
        "patents": "data/clean/patents.csv",
        "inventors": "data/clean/inventors.csv",
        "companies": "data/clean/companies.csv",
        "patent_inventor": "data/clean/patent_inventor.csv"
    }

    for table_name, csv_path in tables.items():
        print(f"Processing {table_name}...")
        
        with sqlite3.connect(DB_PATH) as conn:
            pd.read_csv(csv_path, dtype=str).to_sql(
                table_name, conn, if_exists="replace", index=False
            )
        print(f"{table_name} loaded and connection closed.")

    
    print("\nCreating indexes and summaries...")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Performance Tuning
        cursor.execute("PRAGMA synchronous = OFF")
        
        # Primary Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pat_id ON patents(patent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_inv_id ON inventors(inventor_id)")
        
        # Bridge Table 
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pi_pat ON patent_inventor(patent_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pi_inv ON patent_inventor(inventor_id)")
        
        # Inventor Summary Table
        cursor.execute("DROP TABLE IF EXISTS inventor_summary")
        cursor.execute("""
            CREATE TABLE inventor_summary AS
            SELECT inventor_id, MIN(name) AS name, COUNT(*) AS patents
            FROM inventors
            GROUP BY inventor_id
        """)

        # Yearly Trends Table
        cursor.execute("DROP TABLE IF EXISTS yearly_trends")
        cursor.execute("""
            CREATE TABLE yearly_trends AS
            SELECT year, COUNT(*) AS patents
            FROM patents
            WHERE year BETWEEN 1900 AND 2025
            GROUP BY year
        """)
        
        # 
        cursor.execute("ANALYZE")
        conn.commit()

    print("All indexes and summaries created.")
    print("\nDATABASE READY: No active locks.")

if __name__ == "__main__":
    run_database_build()