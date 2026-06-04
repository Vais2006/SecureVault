import sqlite3
import pandas as pd

DB = "users.db"

def show_table(table):
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

if __name__ == "__main__":
    print("=== USERS TABLE ===")
    print(show_table("users"))

    print("\n=== USER DATA (Vault) ===")
    print(show_table("user_data"))
