
import streamlit as st
import os
from auth import initialize_session_state, login, logout, is_authenticated, is_admin
from student import student_view
from admin import admin_view
from db import init_database

# Page config
st.set_page_config(
    page_title="Student Fine Challan System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        background: white;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #2563eb 100%);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize database and session state
    init_database()
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 The Islamia University of Bahawalpur</h1>
        <h3>Student Fine Challan Management System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not is_authenticated():
        show_login()
    else:
        # Show appropriate interface based on user role
        if is_admin():
            admin_view()
        else:
            student_view()

def show_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown("### 🔐 Login to Continue")
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username/Roll Number", placeholder="Enter your username or roll number")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("Login as Student")
        with col2:
            admin_login_btn = st.form_submit_button("Login as Admin")
        
        if login_btn or admin_login_btn:
            if username and password:
                is_admin_login = admin_login_btn
                if login(username, password, is_admin_login):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
            else:
                st.error("Please enter both username and password.")
    
    # # Demo credentials info
    # with st.expander("Demo Credentials"):
    #     st.info("""
    #     **Admin Login:**
    #     - Username: artificial_intelligence
    #     - Password: challan_app
        
    #     **Student Login:**
    #     - Username: Any roll number (e.g., 2021-CS-001)
    #     - Password: student123
    #     """)
    
    # st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
