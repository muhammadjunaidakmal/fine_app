
import streamlit as st
import pandas as pd
from datetime import datetime
import os
from db import get_all_challans, update_challan_status, get_challan_stats
from auth import logout, get_current_user
from utils import export_to_csv

def admin_view():
    """Admin interface"""
    st.markdown("### 👨‍💼 Admin Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**Welcome, Admin {get_current_user()}**")
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Quick Stats**")
        stats = get_challan_stats()
        st.metric("Total Challans", stats.get('total', 0))
        st.metric("Pending", stats.get('pending', 0))
        st.metric("Approved", stats.get('approved', 0))
        st.metric("Rejected", stats.get('rejected', 0))
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📋 Manage Challans", "📈 Reports"])
    
    with tab1:
        dashboard_overview()
    
    with tab2:
        manage_challans()
    
    with tab3:
        reports_section()

def dashboard_overview():
    """Dashboard overview"""
    st.markdown("#### Dashboard Overview")
    
    # Statistics cards
    stats = get_challan_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Challans", stats.get('total', 0))
    with col2:
        st.metric("Pending Review", stats.get('pending', 0))
    with col3:
        st.metric("Approved", stats.get('approved', 0))
    with col4:
        st.metric("Rejected", stats.get('rejected', 0))
    
    # Recent challans
    st.markdown("#### Recent Challans")
    challans = get_all_challans(limit=10)
    
    if challans:
        df = pd.DataFrame(challans)
        df['created_date'] = pd.to_datetime(df['created_date']).dt.strftime('%Y-%m-%d %H:%M')
        df['amount'] = df['amount'].apply(lambda x: f"Rs. {x:,}")
        
        st.dataframe(
            df[['id', 'student_name', 'roll_number', 'amount', 'status', 'created_date']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No challans found.")

def manage_challans():
    """Manage all challans"""
    st.markdown("#### Manage Challans")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.selectbox("Filter by Status", 
            ["All", "pending", "paid", "approved", "rejected"])
    with col2:
        semester_filter = st.selectbox("Filter by Semester",
            ["All", "1st Semester", "2nd Semester", "3rd Semester", "4th Semester",
             "5th Semester", "6th Semester", "7th Semester", "8th Semester"])
    with col3:
        search_name = st.text_input("Search by Name")
    with col4:
        search_roll = st.text_input("Search by Roll Number")
    
    # Get filtered challans
    challans = get_all_challans()
    
    if challans:
        df = pd.DataFrame(challans)
        
        # Apply filters
        if status_filter != "All":
            df = df[df['status'] == status_filter]
        if semester_filter != "All":
            df = df[df['semester'] == semester_filter]
        if search_name:
            df = df[df['student_name'].str.contains(search_name, case=False, na=False)]
        if search_roll:
            df = df[df['roll_number'].str.contains(search_roll, case=False, na=False)]
        
        # Format display
        df['created_date'] = pd.to_datetime(df['created_date']).dt.strftime('%Y-%m-%d %H:%M')
        df['amount'] = df['amount'].apply(lambda x: f"Rs. {x:,}")
        
        # Display table
        st.dataframe(
            df[['id', 'student_name', 'roll_number', 'semester', 'amount', 'reason', 'status', 'created_date']],
            use_container_width=True,
            hide_index=True
        )
        
        # Action section
        st.markdown("#### Challan Actions")
        
        if not df.empty:
            selected_id = st.selectbox("Select Challan ID:", df['id'].tolist())
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Approve"):
                    if update_challan_status(selected_id, 'approved'):
                        st.success("Challan approved!")
                        st.rerun()
            
            with col2:
                if st.button("❌ Reject"):
                    if update_challan_status(selected_id, 'rejected'):
                        st.success("Challan rejected!")
                        st.rerun()
        
    else:
        st.info("No challans found.")

def reports_section():
    """Reports and exports"""
    st.markdown("#### Reports & Export")
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export All Challans (CSV)"):
            challans = get_all_challans()
            if challans:
                csv_data = export_to_csv(challans)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"challans_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error("No data to export.")
    
    with col2:
        if st.button("📈 Generate Summary Report"):
            st.markdown("#### Summary Report")
            stats = get_challan_stats()
            
            # Create summary
            summary_data = {
                'Metric': ['Total Challans', 'Pending', 'Approved', 'Rejected', 'Total Amount'],
                'Value': [
                    stats.get('total', 0),
                    stats.get('pending', 0),
                    stats.get('approved', 0),
                    stats.get('rejected', 0),
                    f"Rs. {stats.get('total_amount', 0):,}"
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            st.table(summary_df)
    
    # Monthly report
    st.markdown("#### Monthly Analysis")
    challans = get_all_challans()
    
    if challans:
        df = pd.DataFrame(challans)
        df['created_date'] = pd.to_datetime(df['created_date'])
        df['month'] = df['created_date'].dt.to_period('M')
        
        monthly_stats = df.groupby('month').agg({
            'id': 'count',
            'amount': 'sum'
        }).rename(columns={'id': 'Total Challans', 'amount': 'Total Amount'})
        
        if not monthly_stats.empty:
            st.bar_chart(monthly_stats['Total Challans'])
            st.line_chart(monthly_stats['Total Amount'])
