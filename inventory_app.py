import sqlite3
import sys

def init_db(db_name="inventory.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Categories table (3NF normalization)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            reorder_threshold REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')
    
    # Stock transactions log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            action TEXT CHECK(action IN ('IN', 'OUT')),
            change_amount REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (item_id) REFERENCES items(item_id)
        )
    ''')
    
    conn.commit()
    return conn

def add_item(conn, name, category_name, quantity, unit, threshold):
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
    cursor.execute("SELECT category_id FROM categories WHERE name = ?", (category_name,))
    cat_id = cursor.fetchone()[0]
    
    # Parameterized query to prevent SQL injection
    cursor.execute('''
        INSERT INTO items (name, category_id, quantity, unit, reorder_threshold)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, cat_id, quantity, unit, threshold))
    
    conn.commit()
    print(f"[*] Item '{name}' added successfully.")

def check_low_stock(conn):
    cursor = conn.cursor()
    query = '''
        SELECT i.name, c.name, i.quantity, i.unit, i.reorder_threshold
        FROM items i
        INNER JOIN categories c ON i.category_id = c.category_id
        WHERE i.quantity <= i.reorder_threshold
    '''
    cursor.execute(query)
    low_stock = cursor.fetchall()
    
    print("\n--- Low Stock Alerts ---")
    if not low_stock:
        print("All items are above safety thresholds.")
    for row in low_stock:
        print(f"ALERT: {row[0]} ({row[1]}) -> Current: {row[2]} {row[3]} (Threshold: {row[4]} {row[3]})")

if __name__ == "__main__":
    conn = init_db()
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        add_item(conn, "Hydrochloric Acid 37%", "Acids", 4.5, "L", 5.0)
        add_item(conn, "Sodium Hydroxide Pellets", "Bases", 12.0, "kg", 3.0)
        add_item(conn, "Acetone (AR Grade)", "Solvents", 2.0, "L", 10.0)
    
    check_low_stock(conn)
    conn.close()
