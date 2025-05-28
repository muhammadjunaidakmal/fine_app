
import streamlit as st
import bcrypt
import sqlite3
from db import get_connection

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_admin_user():
    """Create default admin user if not exists"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT username FROM admin_users WHERE username = ?", ("artificial_intelligence",))
    if not cursor.fetchone():
        hashed_password = hash_password("challan_app")
        cursor.execute(
            "INSERT INTO admin_users (username, password_hash, email) VALUES (?, ?, ?)",
            ("artificial_intelligence", hashed_password, "admin@university.edu")
        )
        conn.commit()
    
    conn.close()

def login(username: str, password: str, is_admin_login: bool = False) -> bool:
    """Authenticate user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_admin_login:
        # Admin login with new credentials
        cursor.execute("SELECT password_hash FROM admin_users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result and verify_password(password, result[0]):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.is_admin = True
            conn.close()
            return True
    else:
        # Student login - for demo, accept any roll number with password "student123"
        if password == "student123":
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.is_admin = False
            conn.close()
            return True
        
        # Check if student exists in database
        cursor.execute("SELECT roll_number FROM student_challans WHERE roll_number = ?", (username,))
        if cursor.fetchone() and password == "student123":
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.is_admin = False
            conn.close()
            return True
    
    conn.close()
    return False

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.is_admin = False

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def is_admin() -> bool:
    """Check if user is admin"""
    return st.session_state.get('is_admin', False)

def get_current_user() -> str:
    """Get current username"""
    return st.session_state.get('username', "")

# Create admin user on import
create_admin_user()
