
# Student Fine Challan Management System

A comprehensive Streamlit-based web application for managing student fine challans at The Islamia University of Bahawalpur.

## Features

### Student Interface
- **Fine Registration**: Submit new fine challans with personal details
- **PDF Generation**: Automatic generation of 4-copy challan PDFs
- **Receipt Upload**: Upload payment receipts for verification
- **Status Tracking**: Monitor challan status (pending, paid, approved, rejected)
- **Download History**: Re-download challan PDFs anytime

### Admin Interface
- **Dashboard Overview**: Quick statistics and recent activity
- **Challan Management**: Review, approve, or reject student challans
- **Receipt Verification**: View and verify uploaded payment receipts
- **Filtering & Search**: Advanced filtering by status, semester, name, etc.
- **Export Functionality**: Export data to CSV for external analysis
- **Reporting**: Generate summary and monthly analysis reports

### System Features
- **Role-based Access Control**: Separate interfaces for students and admins
- **PDF Template**: University-branded challan format matching official design
- **Database Storage**: SQLite database for persistent data storage
- **File Management**: Organized storage for PDFs and receipt uploads
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
challan_app/
│
├── app.py                   # Main Streamlit application (router)
├── student.py               # Student interface components
├── admin.py                 # Admin interface components
├── auth.py                  # Authentication and session management
├── db.py                    # Database operations and connections
├── pdf_generator.py         # PDF generation using FPDF
├── utils.py                 # Utility functions and helpers
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
├── /data/
│   └── challans.db         # SQLite database (auto-created)
│
├── /pdfs/                  # Generated challan PDFs (auto-created)
└── /uploads/receipts/      # Uploaded receipt files (auto-created)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Local Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd challan_app
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`

## Usage

### Default Login Credentials

**Admin Access:**
- Username: `admin`
- Password: `admin123`

**Student Access:**
- Username: Any roll number (e.g., `2021-CS-001`)
- Password: `student123`

### Student Workflow

1. **Login** with your roll number and password
2. **Create New Challan**: Fill the form with your details and fine information
3. **Download PDF**: Get the 4-copy challan PDF immediately after creation
4. **Pay Fine**: Make payment using the challan at designated bank
5. **Upload Receipt**: Upload payment receipt for admin verification
6. **Track Status**: Monitor approval status in "My Challans" tab

### Admin Workflow

1. **Login** with admin credentials
2. **Dashboard**: View system statistics and recent activity
3. **Manage Challans**: Review submitted challans and uploaded receipts
4. **Verification**: Approve or reject payments based on receipt verification
5. **Reports**: Generate and export reports for administrative purposes

## Database Schema

### student_challans Table
- `id`: Primary key (auto-increment)
- `student_name`: Student's full name
- `roll_number`: Student's roll number
- `id_card_number`: CNIC number
- `semester`: Current semester
- `amount`: Fine amount in PKR
- `reason`: Reason for fine
- `created_date`: Timestamp of challan creation
- `valid_till`: Challan validity date (3 days from creation)
- `status`: Current status (pending/paid/approved/rejected)
- `receipt_path`: Path to uploaded receipt file
- `admin_comments`: Admin comments on the challan
- `updated_date`: Last update timestamp

### admin_users Table
- `id`: Primary key (auto-increment)
- `username`: Admin username
- `password_hash`: Bcrypt hashed password
- `email`: Admin email address
- `created_date`: Account creation timestamp

## Configuration

### Customization Options

1. **University Details**: Update university information in `pdf_generator.py`
2. **Bank Details**: Modify bank account information in the PDF template
3. **Fine Amounts**: Adjust default fine amounts in the student form
4. **Validity Period**: Change challan validity period (currently 3 days)
5. **File Upload Types**: Modify allowed file types for receipt uploads

### Email Notifications (Optional)

To enable email notifications:

1. Update SMTP configuration in `utils.py`
2. Set your email server details:
   ```python
   smtp_config = {
       'smtp_server': 'your-smtp-server.com',
       'smtp_port': 587,
       'email': 'your-email@domain.com',
       'password': 'your-app-password'
   }
   ```

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. **Push to GitHub**: Upload your code to a GitHub repository
2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the main application file (`app.py`)
3. **Deploy**: Streamlit Cloud will automatically deploy your app

### Other Cloud Platforms

**Heroku:**
1. Create `Procfile`: `web: streamlit run app.py --server.port $PORT`
2. Add `setup.sh` for Streamlit configuration
3. Deploy using Heroku CLI or GitHub integration

**Railway/Render:**
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py`

## Security Considerations

1. **Password Security**: Uses bcrypt for password hashing
2. **Session Management**: Secure session state management
3. **File Upload Security**: Validates file types and sizes
4. **Database Security**: Uses parameterized queries to prevent SQL injection
5. **Access Control**: Role-based access with proper authentication

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Connection Issues**
   - Ensure the `data/` directory exists
   - Check file permissions

3. **PDF Generation Problems**
   - Verify FPDF installation
   - Check font availability

4. **File Upload Failures**
   - Ensure `uploads/receipts/` directory exists
   - Check file size limits

### Error Logs

- Check Streamlit terminal output for detailed error messages
- Database errors are logged to console
- File operation errors include path information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is developed for educational purposes. Please ensure compliance with your institution's policies before deployment.

## Support

For technical support or feature requests:
- Create an issue in the project repository
- Contact the development team
- Refer to Streamlit documentation for framework-specific issues

## Version History

- **v1.0.0**: Initial release with core functionality
- **v1.1.0**: Added receipt upload and admin verification
- **v1.2.0**: Enhanced reporting and export features
- **v1.3.0**: Improved PDF template and mobile responsiveness

---

**The Islamia University of Bahawalpur**  
Department of Artificial Intelligence  
Student Fine Challan Management System
