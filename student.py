import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from db import insert_challan, get_student_challans, update_receipt_upload
from pdf_generator import generate_challan_pdf
from auth import logout, get_current_user
import uuid

def student_view():
    """Student interface"""
    st.markdown("### 👨‍🎓 Student Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**Welcome, {get_current_user()}**")
        if st.button("🚪 Logout"):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Navigation**")
        
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📝 New Challan", "📋 My Challans", "📤 Upload Receipt"])
    
    with tab1:
        new_challan_form()
    
    with tab2:
        view_my_challans()
    
    with tab3:
        upload_receipt()

def new_challan_form():
    """Form to create new challan"""
    st.markdown("#### Create New Fine Challan")

    # State to store PDF buffer and challan info after form submission
    if 'challan_pdf_buffer' not in st.session_state:
        st.session_state.challan_pdf_buffer = None
    if 'challan_download_info' not in st.session_state:
        st.session_state.challan_download_info = None

    with st.form("challan_form"):
        col1, col2 = st.columns(2)

        with col1:
            student_name = st.text_input("Student Name *", placeholder="Enter full name")
            id_card_number = st.text_input("CNIC Number *", placeholder="e.g., 12345-1234567-1")
            roll_number = st.text_input("Roll Number *", value=get_current_user(), disabled=True)

        with col2:
            semester = st.selectbox("Semester *", 
                ["1st Semester", "2nd Semester", "3rd Semester", "4th Semester", 
                 "5th Semester", "6th Semester", "7th Semester", "8th Semester"])
            amount = st.number_input("Fine Amount (Rs) *", min_value=1, step=1, value=500)
            reason = st.text_area("Reason for Fine *", placeholder="Enter reason for fine")

        submit_btn = st.form_submit_button("Generate Challan", use_container_width=True)

        if submit_btn:
            if student_name and id_card_number and roll_number and reason:
                # Create challan data
                challan_data = {
                    'student_name': student_name,
                    'id_card_number': id_card_number,
                    'roll_number': roll_number,
                    'semester': semester,
                    'amount': amount,
                    'reason': reason,
                    'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'valid_till': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                    'status': 'pending'
                }
                # Insert into database
                challan_id = insert_challan(challan_data)
                if challan_id:
                    st.success("✅ Challan created successfully!")
                    # Generate PDF and store in session state
                    st.session_state.challan_pdf_buffer = generate_challan_pdf(challan_data)
                    st.session_state.challan_download_info = {
                        'roll_number': roll_number,
                        'challan_id': challan_id
                    }
                else:
                    st.error("❌ Error creating challan. Please try again.")
            else:
                st.error("❌ Please fill all required fields.")

    # Always show the download button if PDF is ready (outside the form, not conditional on button click)
    if st.session_state.challan_pdf_buffer and st.session_state.challan_download_info:
        info = st.session_state.challan_download_info
        st.download_button(
            label="📥 Download Challan PDF",
            data=st.session_state.challan_pdf_buffer,
            file_name=f"challan_{info['roll_number']}_{info['challan_id']}.pdf",
            mime="application/pdf",
            use_container_width=True,
            on_click=None  # Remove 'ignore', just use default
        )
        # Optionally, clear the buffer after download to avoid repeated downloads
        # st.session_state.challan_pdf_buffer = None
        # st.session_state.challan_download_info = None

def view_my_challans():
    """View student's challans"""
    st.markdown("#### My Challans")
    
    challans = get_student_challans(get_current_user())
    
    if challans:
        df = pd.DataFrame(challans)
        
        # Format the dataframe
        df['created_date'] = pd.to_datetime(df['created_date']).dt.strftime('%Y-%m-%d %H:%M')
        df['amount'] = df['amount'].apply(lambda x: f"Rs. {x:,}")
        
        # Status styling
        def style_status(status):
            colors = {
                'pending': '🟡 Pending',
                'paid': '🟢 Paid',
                'approved': '✅ Approved',
                'rejected': '❌ Rejected'
            }
            return colors.get(status, status)
        
        df['status'] = df['status'].apply(style_status)
        
        # Display table
        st.dataframe(
            df[['id', 'student_name', 'semester', 'amount', 'reason', 'created_date', 'status']],
            use_container_width=True,
            hide_index=True
        )
        
        # Individual challan actions
        st.markdown("#### Challan Actions")
        selected_id = st.selectbox("Select Challan ID for actions:", df['id'].tolist())
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Re-download PDF"):
                challan = next((c for c in challans if c['id'] == selected_id), None)
                if challan:
                    pdf_buffer = generate_challan_pdf(challan)
                    st.download_button(
                        label="Download PDF",
                        data=pdf_buffer,
                        file_name=f"challan_{challan['roll_number']}_{selected_id}.pdf",
                        mime="application/pdf"
                    )
        
        with col2:
            if st.button("📤 Upload Receipt"):
                st.session_state.upload_challan_id = selected_id
                st.rerun()
    else:
        st.info("📭 No challans found. Create your first challan using the 'New Challan' tab.")

def upload_receipt():
    """Upload payment receipt"""
    st.markdown("#### Upload Payment Receipt")
    
    challans = get_student_challans(get_current_user())
    pending_challans = [c for c in challans if c['status'] in ['pending', 'paid']]
    
    if pending_challans:
        # Select challan
        challan_options = {f"ID: {c['id']} - {c['reason']} (Rs. {c['amount']})": c['id'] for c in pending_challans}
        selected_challan = st.selectbox("Select Challan:", list(challan_options.keys()))
        challan_id = challan_options[selected_challan]
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose receipt file",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            help="Upload a clear image or PDF of your payment receipt"
        )
        
        if uploaded_file and st.button("Upload Receipt"):
            # Create uploads directory if not exists
            os.makedirs("uploads/receipts", exist_ok=True)
            
            # Generate unique filename
            file_extension = uploaded_file.name.split('.')[-1]
            filename = f"receipt_{challan_id}_{uuid.uuid4().hex[:8]}.{file_extension}"
            filepath = os.path.join("uploads/receipts", filename)
            
            # Save file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Update database
            if update_receipt_upload(challan_id, filepath):
                st.success("✅ Receipt uploaded successfully! Admin will review it soon.")
            else:
                st.error("❌ Error uploading receipt. Please try again.")
    else:
        st.info("📭 No challans available for receipt upload.")
