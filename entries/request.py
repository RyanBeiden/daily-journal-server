import sqlite3
import json

from models.entries import JournalEntry
from models.moods import Mood
from models.tags import Tag

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

            db_cursor.execute("""
            SELECT
                t.id,
                t.name,
                et.id,
                et.entry_id,
                et.tag_id
            FROM EntryTags et
            JOIN Tags t
                ON t.id = et.tag_id
            WHERE et.entry_id = ?
            """, ( row['id'], ))

            tags = []
            tagset = db_cursor.fetchall()

            for one_tag in tagset:
                tag = Tag(one_tag['id'], one_tag['name'])
                tags.append(tag.__dict__)
            
            entry.tags = tags
    
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

def create_journal_entry(new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO JournalEntries
            ( concept, entry, date, moodId )
        VALUES
            ( ?, ?, ?, ? )
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId']))

        id = db_cursor.lastrowid
        new_entry['id'] = id

        if new_entry['tags']:
            for tag in new_entry['tags']:
                db_cursor.execute("""
                INSERT INTO EntryTags
                    ( entry_id, tag_id )
                VALUES 
                    ( ?, ? )
                """, (id, tag))

    json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE JournalEntries
            SET
                concept = ?,
                entry = ?,
                date = ?,
                moodId = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['date'], new_entry['moodId'], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True