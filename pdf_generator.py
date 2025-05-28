
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime, timedelta
import io
from typing import Dict

def generate_challan_pdf(challan_data: Dict) -> bytes:
    """Generate PDF challan with 4 copies in 1x4 grid layout (single column, 4 rows)"""
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)
    page_w, page_h = A4
    
    # Calculate current date and challan number
    current_date = datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')
    challan_number = "2517381134"
    valid_till = (datetime.now() + timedelta(days=3)).strftime('%d/%m/%Y')
    
    # Define copy types
    copy_types = ["Bank Copy", "Accounts Copy", "Department Copy", "Student Copy"]
    
    # Page dimensions and margins
    margin = 20
    copy_width = page_w - (2 * margin)
    copy_height = (page_h - (2 * margin)) / 4 - 10  # 10pt gap between copies
    
    # Generate 4 copies (1x4 grid - one column, four rows)
    for i, copy_type in enumerate(copy_types):
        # Calculate position for each copy
        x = margin
        y = page_h - margin - (i * (copy_height + 10)) - copy_height
        
        # Draw copy border
        c.rect(x, y, copy_width, copy_height)
        
        # Current Y position for content (start from top of the copy)
        current_y = y + copy_height - 15
        
        # Header section - Copy type
        c.setFont('Helvetica-Bold', 12)
        c.drawCentredString(x + copy_width/2, current_y, copy_type)
        c.line(x + 10, current_y - 5, x + copy_width - 10, current_y - 5)
        current_y -= 20
        
        # University header
        c.setFont('Helvetica-Bold', 10)
        c.drawString(x + 10, current_y - 12, 'The Islamia University of Bahawalpur')
        current_y -= 12
        
        c.setFont('Helvetica', 8)
        c.drawString(x + 10, current_y, 'F.T.N: 9020017-1')
        current_y -= 30
        
        # Updated Bank details section
        c.setFont('Helvetica', 7)
        bank_details = [
            "Account No: 00250025026967210000",
            "First Women Bank",
            "Account Title:",
            "DEPARTMENT OF",
            "ARTIFICIAL",
            "INTELLIGENCE"
        ]
        
        for detail in bank_details:
            c.drawString(x + 10, current_y, detail)
            current_y -= 8
        
        current_y -= 10
        
        # Separator line
        c.line(x + 10, current_y, x + copy_width - 10, current_y)
        current_y -= 15
        
        # Date and challan info
        c.setFont('Helvetica', 8)
        c.drawCentredString(x + copy_width/2, current_y, current_date)
        current_y -= 12
        
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(x + copy_width/2, current_y, f"Challan No: {challan_number}")
        current_y -= 15
        
        # Valid till
        c.setFont('Helvetica-Bold', 8)
        c.drawCentredString(x + copy_width/2, current_y, f"Challan Valid Till: {valid_till}")
        current_y -= 20
        
        # Student details
        c.setFont('Helvetica', 8)
        student_details = [
            f"Name: {challan_data['student_name']}",
            f"CNIC / Other: {challan_data['id_card_number']}",
            f"App #: {challan_data['roll_number']}",
            f"App Title: {challan_data['reason']}"
        ]
        
        for detail in student_details:
            c.drawString(x + 10, current_y, detail)
            current_y -= 10
        
        current_y -= 10
        
        # Amount table
        table_y = current_y
        table_height = 40
        
        # Table border
        c.rect(x + 10, table_y - table_height, copy_width - 20, table_height)
        
        # Table headers with background
        header_y = table_y - 10
        c.setFillColorRGB(0.9, 0.9, 0.9)  # Light gray background
        c.rect(x + 10, header_y, copy_width - 20, -12, fill=1, stroke=1)
        c.setFillColorRGB(0, 0, 0)  # Reset to black
        
        # Vertical line for table columns
        c.line(x + copy_width - 80, table_y - table_height, x + copy_width - 80, table_y)
        
        # Header text
        c.setFont('Helvetica-Bold', 8)
        c.drawString(x + 15, header_y - 8, 'Particular')
        c.drawString(x + copy_width - 75, header_y - 8, 'Amount (Rs)')
        
        # Table content
        content_y = header_y - 22
        c.setFont('Helvetica', 8)
        c.drawString(x + 15, content_y, challan_data['reason'])
        c.drawString(x + copy_width - 75, content_y, f"Rs. {challan_data['amount']}/-")
        
        # Total row with dark background
        total_y = content_y - 12
        c.setFillColorRGB(0, 0, 0)  # Black background
        c.rect(x + 10, total_y, copy_width - 20, -12, fill=1, stroke=1)
        c.setFillColorRGB(1, 1, 1)  # White text
        c.setFont('Helvetica-Bold', 8)
        c.drawString(x + 15, total_y - 8, 'Total Amount to Pay')
        c.drawString(x + copy_width - 75, total_y - 8, f"Rs. {challan_data['amount']}/-")
        c.setFillColorRGB(0, 0, 0)  # Reset to black
    
    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    
    return pdf_buffer.getvalue()
