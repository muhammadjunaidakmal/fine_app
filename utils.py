
import bcrypt
import uuid
import csv
import io
from typing import List, Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_unique_filename(prefix: str, extension: str) -> str:
    """Generate unique filename"""
    unique_id = uuid.uuid4().hex[:8]
    return f"{prefix}_{unique_id}.{extension}"

def export_to_csv(data: List[Dict]) -> str:
    """Export data to CSV format"""
    if not data:
        return ""
    
    output = io.StringIO()
    
    # Get fieldnames from first record
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data
    for row in data:
        writer.writerow(row)
    
    return output.getvalue()

def send_email_notification(to_email: str, subject: str, body: str, smtp_config: Dict = None):
    """Send email notification (optional feature)"""
    if not smtp_config:
        # Default SMTP configuration (for demonstration)
        smtp_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email': 'your-email@gmail.com',
            'password': 'your-app-password'
        }
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = smtp_config['email']
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
        server.starttls()  # Enable TLS
        server.login(smtp_config['email'], smtp_config['password'])
        
        # Send email
        text = msg.as_string()
        server.sendmail(smtp_config['email'], to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def validate_cnic(cnic: str) -> bool:
    """Validate CNIC format"""
    # Remove any spaces or dashes
    cnic_clean = cnic.replace('-', '').replace(' ', '')
    
    # Check if it's 13 digits
    if len(cnic_clean) != 13 or not cnic_clean.isdigit():
        return False
    
    return True

def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate file type"""
    if not filename:
        return False
    
    file_extension = filename.split('.')[-1].lower()
    return file_extension in [t.lower() for t in allowed_types]

def format_currency(amount: int) -> str:
    """Format amount as currency"""
    return f"Rs. {amount:,}/-"

def calculate_fine_amount(base_amount: int, days_overdue: int = 0) -> int:
    """Calculate fine amount with late fee"""
    late_fee_per_day = 10  # Rs. 10 per day
    late_fee = days_overdue * late_fee_per_day
    return base_amount + late_fee
