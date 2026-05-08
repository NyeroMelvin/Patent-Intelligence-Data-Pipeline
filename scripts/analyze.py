import sqlite3
import pandas as pd

DB_PATH = "data/patents.db"

def run_report():

    conn = sqlite3.connect(DB_PATH)
    

    conn.execute("PRAGMA cache_size = -64000")
    conn.execute("PRAGMA temp_store = MEMORY")

    print("\n" + "="*80)
    print("                    OFFICIAL PATENT ANALYSIS REPORT")
    print("="*80 + "\n")

    try:
        # Q1: TOP INVENTORS
        print("Q1: Top 10 Inventors (Most Patents)")
        query1 = "SELECT name, patents FROM inventor_summary ORDER BY patents DESC LIMIT 10"
        print(pd.read_sql(query1, conn).to_string(index=False), "\n")

        # Q2: TOP COMPANIES
        print("Q2: Top 10 Companies according to portfolio size")
        query2 = "SELECT name, patents FROM company_summary ORDER BY patents DESC LIMIT 10"
        print(pd.read_sql(query2, conn).to_string(index=False), "\n")

        # Q4: TRENDS OVER TIME
        print("Q4: Patenting Trends (Recent 5 Years)")
        query4 = "SELECT year, patents FROM yearly_trends ORDER BY year DESC LIMIT 5"
        print(pd.read_sql(query4, conn).to_string(index=False), "\n")

        # Q5: JOIN QUERY
        print("Q5: JOIN Query")
        # DISTINCT prevents the same inventor appearing multiple times for one patent
        query5 = """
            SELECT DISTINCT
                p.patent_id, 
                p.title, 
                i.name as inventor, 
                c.name as company
            FROM patents p
            JOIN patent_inventor pi ON p.patent_id = pi.patent_id
            JOIN inventors i ON pi.inventor_id = i.inventor_id
            JOIN companies c ON p.patent_id = c.patent_id
            LIMIT 10
        """
        print(pd.read_sql(query5, conn).to_string(index=False), "\n")

        # Q6: CTE QUERY 
        print("Q6: CTE Query")
        query6 = """
            WITH ProlificInventors AS (
                SELECT name, patents 
                FROM inventor_summary 
                WHERE patents > 1000
            )
            SELECT * FROM ProlificInventors ORDER BY patents DESC LIMIT 5
        """
        print(pd.read_sql(query6, conn).to_string(index=False), "\n")

        # Q7: RANKING QUERY
        print("Q7: Ranking Inventors")
        query7 = """
            SELECT 
                name, 
                patents,
                RANK() OVER (ORDER BY patents DESC) as global_rank
            FROM inventor_summary
            LIMIT 10
        """
        print(pd.read_sql(query7, conn).to_string(index=False), "\n")

    except Exception as e:
        print(f" Error during analysis: {e}")
    
    finally:
        conn.close()
        print("="*80)
        print("                REPORT COMPLETE ")
        print("="*80 + "\n")

if __name__ == "__main__":
    run_report()