import sqlite3
import os
from typing import List, Dict, Optional

def get_connection():
    """Get database connection"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/challans.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Student challans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_challans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            id_card_number TEXT NOT NULL,
            semester TEXT NOT NULL,
            amount INTEGER NOT NULL,
            reason TEXT NOT NULL,
            created_date TEXT NOT NULL,
            valid_till TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            receipt_path TEXT,
            admin_comments TEXT,
            updated_date TEXT
        )
    """)
    
    # Admin users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def insert_challan(challan_data: Dict) -> Optional[int]:
    """Insert new challan"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO student_challans 
            (student_name, roll_number, id_card_number, semester, amount, reason, created_date, valid_till, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            challan_data['student_name'],
            challan_data['roll_number'],
            challan_data['id_card_number'],
            challan_data['semester'],
            challan_data['amount'],
            challan_data['reason'],
            challan_data['created_date'],
            challan_data['valid_till'],
            challan_data['status']
        ))
        
        challan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return challan_id
    except Exception as e:
        print(f"Error inserting challan: {e}")
        return None

def get_student_challans(roll_number: str) -> List[Dict]:
    """Get challans for specific student"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM student_challans 
        WHERE roll_number = ? 
        ORDER BY created_date DESC
    """, (roll_number,))
    
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def get_all_challans(limit: Optional[int] = None) -> List[Dict]:
    """Get all challans"""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM student_challans ORDER BY created_date DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def update_challan_status(challan_id: int, status: str, comments: str = "") -> bool:
    """Update challan status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE student_challans 
            SET status = ?, admin_comments = ?, updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, comments, challan_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating challan status: {e}")
        return False

def update_receipt_upload(challan_id: int, receipt_path: str) -> bool:
    """Update receipt path for challan"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE student_challans 
            SET receipt_path = ?, status = 'paid', updated_date = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (receipt_path, challan_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating receipt: {e}")
        return False

def get_challan_stats() -> Dict:
    """Get challan statistics"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total count
    cursor.execute("SELECT COUNT(*) as total FROM student_challans")
    total = cursor.fetchone()['total']
    
    # Status counts
    cursor.execute("""
        SELECT status, COUNT(*) as count 
        FROM student_challans 
        GROUP BY status
    """)
    status_counts = {row['status']: row['count'] for row in cursor.fetchall()}
    
    # Total amount
    cursor.execute("SELECT SUM(amount) as total_amount FROM student_challans")
    total_amount = cursor.fetchone()['total_amount'] or 0
    
    conn.close()
    
    return {
        'total': total,
        'pending': status_counts.get('pending', 0),
        'paid': status_counts.get('paid', 0),
        'approved': status_counts.get('approved', 0),
        'rejected': status_counts.get('rejected', 0),
        'total_amount': total_amount
    }

def ensure_admin_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
