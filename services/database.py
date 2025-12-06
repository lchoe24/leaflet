import sqlite3
from datetime import datetime
from typing import Optional, List, Dict

DB_FILE = "journal.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            turn_order INTEGER NOT NULL,
            FOREIGN KEY (entry_id) REFERENCES entries(id) ON DELETE CASCADE
        )
    ''')
    
    c.execute('CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_messages_entry ON messages(entry_id)')
    
    conn.commit()
    conn.close()


def save_entry(date_str: str, mood: str, messages: List[Dict]) -> Optional[int]:
    conn = get_connection()
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    try:
        c.execute(
            'INSERT INTO entries (date, mood, created_at) VALUES (?, ?, ?)',
            (date_str, mood, now)
        )
        entry_id = c.lastrowid
        
        for i, msg in enumerate(messages):
            c.execute(
                'INSERT INTO messages (entry_id, role, content, turn_order) VALUES (?, ?, ?, ?)',
                (entry_id, msg['role'], msg['content'], i + 1)
            )
        
        conn.commit()
        return entry_id
    except sqlite3.Error:
        conn.rollback()
        return None
    finally:
        conn.close()


def get_entry_by_date(date_str: str) -> Optional[Dict]:
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM entries WHERE date = ? LIMIT 1', (date_str,))
    entry = c.fetchone()
    
    if not entry:
        conn.close()
        return None
    
    c.execute(
        'SELECT role, content FROM messages WHERE entry_id = ? ORDER BY turn_order',
        (entry['id'],)
    )
    messages = [{'role': m['role'], 'content': m['content']} for m in c.fetchall()]
    
    conn.close()
    return {
        'id': entry['id'],
        'date': entry['date'],
        'mood': entry['mood'],
        'messages': messages,
        'created_at': entry['created_at']
    }


def get_all_entries() -> List[Dict]:
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT * FROM entries ORDER BY date DESC, id DESC')
    entries = c.fetchall()
    
    result = []
    for entry in entries:
        c.execute(
            'SELECT role, content FROM messages WHERE entry_id = ? ORDER BY turn_order',
            (entry['id'],)
        )
        messages = [{'role': m['role'], 'content': m['content']} for m in c.fetchall()]
        
        result.append({
            'id': entry['id'],
            'date': entry['date'],
            'mood': entry['mood'],
            'messages': messages,
            'created_at': entry['created_at']
        })
    
    conn.close()
    return result


init_db()
