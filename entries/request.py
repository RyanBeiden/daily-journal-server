import sqlite3
import json

from models.entries import JournalEntry
from models.moods import Mood

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
            e.moodId,
            m.id,
            m.label
        FROM JournalEntries e
        JOIN Moods m
            ON m.id = e.moodId
        """)

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = JournalEntry(row["id"], row["concept"], row["entry"], row["date"], row["moodId"])
            mood = Mood(row["id"], row["label"])

            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
    
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM JournalEntries e
        WHERE e.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

        entry = JournalEntry(data["id"], data["concept"], data["entry"], data["date"], data["moodId"])

    return json.dumps(entry.__dict__)

def get_entry_by_word(q):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.moodId
        FROM JournalEntries e
        WHERE e.entry LIKE "%"||?||"%"
        """, (q, ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = JournalEntry(row["id"], row["concept"], row["entry"], row["date"], row["moodId"])
            entries.append(entry.__dict__)

    return json.dumps(entries)

def delete_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM JournalEntries
        WHERE id = ?
        """, (id, ))
