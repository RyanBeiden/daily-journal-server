import sqlite3
import json

from models.entries import JournalEntry

def get_all_entries():
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM JournalEntries e
        """)

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = JournalEntry(row["id"], row["concept"], row["entry"], row["date"], row["mood_id"])
            entries.append(entry.__dict__)
    
    return json.dumps(entries)