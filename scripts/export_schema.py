import sqlite3
from pathlib import Path

db_path = Path("patents.db")  # adjust if inside another folder
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all table creation SQL
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")

schema_statements = cursor.fetchall()

output_file = Path("schema.sql")

with open(output_file, "w", encoding="utf-8") as f:
    for statement in schema_statements:
        if statement[0]:
            f.write(statement[0] + ";\n\n")

conn.close()

print("schema.sql generated successfully!")