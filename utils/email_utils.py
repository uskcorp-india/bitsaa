import io
import os
import smtplib
from email.message import EmailMessage
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

def send_welcome_email(recipient_email: str, first_name: str, order_id: str, ticket_count: int):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = recipient_email
    message["Subject"] = "🎉 Welcome to BGM 2026 – Let’s Get You Settled!"
    message['X-Priority'] = '1'
    message['X-MSMail-Priority'] = 'High'
    message['Importance'] = 'High'
    print(f"welcome message sent to  {message}")
    body = f"""
    <!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Welcome to BGM 2026</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
  <p>Hi {first_name},</p>

  <p>Congratulations – your registration for <strong>BITSAA Global Meet 2026</strong> is confirmed! 🎊</p>

  <p>We’re thrilled to have you on board for three unforgettable days of connection, inspiration, and nostalgia at the <strong>BITS Hyderabad Campus from January 9–11, 2026</strong>.</p>

  <p>Now that you've taken the first step, it's time to complete your BGM journey by booking your accommodation. To make this process smooth, please follow the simple steps below:</p>
  <hr>
  <h3>🛏️ How to Book Your Accommodation:</h3>

<p style="margin-bottom: 12px;">
<strong>STEP 1</strong>: REGISTER YOUR STAY<br>
   Fill out the check-in and check-out dates from the dropdown in the form.
</p>
<p style="margin-bottom: 12px;">
<strong>STEP 2</strong>: CHOOSE YOUR ACCOMMODATION<br>
  Choose your preferred hotel and room type based on comfort, group size, or preference.<br>
   Each room includes one extra bed facility for added convenience.
</p>
<p>
 <strong>STEP 3</strong>:CONFIRM YOUR BOOKING<br>
  Specify the number of rooms required <br>
  Enter registration id for each and click “Submit” to finalise yo  ur booking.
</p>
  <hr>
  <p>Following these steps will ensure that your stay is comfortably arranged and you're all set to experience the magic of BGM hassle-free.</p>
  <p>If you have any questions or need help, don’t hesitate to reach out to us at 
    <a href="mailto:bgm-communications@bitsaa.org">bgm-communications@bitsaa.org</a>.
  </p><br>
  
  <a href="https://booking.d9events.in/bookings/?order_id={order_id}&ticket_count={ticket_count}" 
   style=" 
     display: inline-block;
     padding: 12px 24px;
     background-color: #007BFF;
     color: white;
     text-decoration: none;
     border-radius: 8px;
     font-size: 16px;
     width: 180px;
     text-align: center;">
  Book now
</a>
  <p>See you in Hyderabad!</p>
  <p>
    Warm regards,<br>
    <strong style="font-size: 14px";>Team BGM 2026</strong><br>
    <em>Network • Navigate • Nostalgia</em>
  </p>
</body>
</html>
    """
    message.add_alternative(body, subtype="html")

    try:
        with smtplib.SMTP_SSL(os.getenv("IMAP_SERVER"), 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(message)
            print(f"Confirmation email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")


def num2words(num: int) -> str:
    """Convert number to words (simplified for INR)."""
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
             "Seventeen", "Eighteen", "Nineteen"]

    n = int(num)
    if n < 10:
        return units[n]
    elif n < 20:
        return teens[n - 10]
    elif n < 100:
        return tens[n // 10] + ("" if n % 10 == 0 else " " + units[n % 10])
    elif n < 1000:
        return units[n // 100] + " Hundred " + ("" if n % 100 == 0 else num2words(n % 100))
    elif n < 100000:
        return num2words(n // 1000) + " Thousand " + ("" if n % 1000 == 0 else num2words(n % 1000))
    else:
        return str(n)


def add_page_border(canvas, _doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(1.5)
    margin = 30
    canvas.rect(margin, margin, A4[0] - 2 * margin, A4[1] - 2 * margin)
    canvas.restoreState()


def generate_invoice_pdf_bytes(reservation_data: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30,
        title="Invoice - D9 Events"
    )
    styles = getSampleStyleSheet()
    style_n = ParagraphStyle("Normal", parent=styles["Normal"], fontSize=10, leading=14)
    style_b = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=12, spaceAfter=6)
    content = []
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "logo", "d9_EVENTS_LOGO.webp"), "rb") as f:
        img_bytes = f.read()
    img_stream = io.BytesIO(img_bytes)
    logo = Image(img_stream, width=100, height=100)
    logo_table = Table([[logo]], colWidths=[doc.width])
    logo_table.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    content.append(logo_table)
    content.append(Spacer(1, 12))

    gst_number = "36BRPPS8791F1ZV"

    # Invoice header
    invoice_info = [
        Paragraph("<b>TAX INVOICE</b>", style_b),
        Paragraph(f"Invoice No: {reservation_data['id']}", style_n),
        Paragraph(f"Date of Invoice: {datetime.now().strftime('%d-%m-%Y')}", style_n),
    ]
    gst_info = [
        Paragraph("<b>GSTIN:</b> " + gst_number, style_n),
        Paragraph("<b>State:</b> Telangana", style_n),
        Paragraph("<b>Place of Supply:</b> Hyderabad", style_n),
    ]
    header_table = Table([[invoice_info, gst_info]], colWidths=[doc.width * 0.65, doc.width * 0.35])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
    ]))
    content.append(header_table)
    content.append(Spacer(1, 12))

    # Reservation info
    check_in = datetime.strptime(reservation_data["check_in"], "%Y-%m-%d")
    check_out = datetime.strptime(reservation_data["check_out"], "%Y-%m-%d")
    registrant = reservation_data["registration"][0]
    content.append(Paragraph(f"<b>Invoice To:</b> {registrant['registrantName'].title()}", style_n))
    content.append(Paragraph(f"Check-In: {check_in.strftime('%d-%m-%Y')}", style_n))
    content.append(Paragraph(f"Check-Out: {check_out.strftime('%d-%m-%Y')}", style_n))
    content.append(Spacer(1, 12))
    total_cost = int(reservation_data["total_cost"].strip('"').strip())
    room_count = reservation_data["room_count"]
    per_day_price = reservation_data["resort"]["price_per_day"]
    days = (check_out - check_in).days or 1
    gst_rate = 0.05 if per_day_price <= 5999 else 0.18
    service_rate = 0.10
    base_total = round(per_day_price * room_count * days, 2)
    service_charge = round(base_total * service_rate, 2)
    gst_amount = round((base_total + service_charge) * gst_rate, 2)
    total_amount = base_total + service_charge + gst_amount
    resort_text = Paragraph(
        f"Hotel: {reservation_data['resort']['name']} - {reservation_data['resort']['category']}",
        style_n,
    )
    item_data = [
        ["Resort", "Rooms", "Per Day", "Service Charge 10%", "Total Amount (Incl.GST)"],
        [
            resort_text,
            str(room_count),
            f"Rs. {per_day_price:.2f}",
            f"Rs. {service_charge:.2f}",
            f"Rs. {total_amount:.2f}",
        ],
    ]
    fixed_widths = [60, 80, 100, 120]
    resort_width = doc.width - sum(fixed_widths) - 25
    col_widths = [resort_width] + fixed_widths
    res_table = Table(item_data, colWidths=col_widths)
    res_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    content.append(res_table)
    content.append(Spacer(1, 12))
    cgst = sgst = gst_amount / 2
    tax_data = [
        ["Taxes", "Rate", "Amount"],
        ["CGST", f"{(gst_rate * 100 / 2.0)}%", f"Rs. {cgst:.2f}"],
        ["SGST", f"{(gst_rate * 100 / 2.0)}%", f"Rs. {sgst:.2f}"],
        ["Total Taxes", "", f"Rs. {gst_amount:.2f}"],
    ]
    tax_table = Table(tax_data, colWidths=[200, 80, 100])
    tax_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    content.append(tax_table)
    content.append(Spacer(1, 12))
    guest_data = [["Registration ID", "Guest Name"]]
    for guest in reservation_data.get("registration", []):
        guest_name = guest["registrantName"].title() if guest.get("registrantName") else ""
        guest_data.append([guest["id"], guest_name])
    guest_table = Table(guest_data, colWidths=[250, 250])
    guest_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    content.append(Paragraph("<b>Guest Details</b>", style_b))
    content.append(guest_table)
    content.append(Spacer(1, 12))
    content.append(Paragraph(f"<b>Invoice Total:</b> Rs. {total_amount:,.2f}", style_b))
    content.append(Paragraph(f"Invoice total in words: <i>{num2words(total_amount)} Rupees Only</i>", style_n))
    content.append(Spacer(1, 12))
    content.append(Paragraph("<b>Note*</b> - Additional Beds will be chargeable", style_n))
    content.append(Spacer(1, 24))
    content.append(Paragraph("This is a computer-generated invoice. No signature required.", style_n))
    doc.build(content, onFirstPage=add_page_border, onLaterPages=add_page_border)
    buffer.seek(0)
    return buffer.read()

def send_booking_confirmation_email(reservation_data: dict):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_USER")
    recipient_email = reservation_data.get('registration')[0]['registrantEmail']
    message["To"] = ", ".join([recipient_email, "bgm-vendor@bitsaa.org", "Info.d9events@gmail.com"])
    message["Subject"] = "🏨 Your BGM 2026 Hotel Booking is Confirmed!"
    total_cost = int(reservation_data['total_cost'].strip('"').strip())
    formatted_cost = f"₹{total_cost:,.0f}"
    registration_data = reservation_data.get('registration', [])
    group_info = ""
    if len(registration_data) >= 1:
        group_members = [reg.get('registrantName', '').strip() for reg in registration_data]
        members_list = f"<li> {group_members[0]} (Registrant) </li>"
        others = "\n".join(f"<li> {name} </li>" for name in group_members[1:])
        group_info = f"<li><b>Group Members:</b></li><ul style='list-style-type: circle'>{members_list}{others}</ul>"

    body = f"""
    <html>
    <body>
    <div style="text-align: left; margin-bottom: 10px;">
      <img src="https://booking.d9events.in/wp-content/uploads/2025/08/d9_EVENTS_LOGO.png" alt="BGM 2026 Logo" style="max-height:100px;">
    </div>
    <p>Hi {registration_data[0]['registrantName']},</p>
    <p>We’re delighted to let you know that your <strong>accommodation for BITSAA Global Meet 2026</strong> has been successfully booked! 🥳</p>
    <h3>📌 Reservation Summary</h3>
    <ul>
        <li><b>Registrant Name:</b> {registration_data[0]['registrantName']}</li>
        {group_info}
        <li><b>Reservation ID:</b> {reservation_data['id']}</li>
        <li><b>Payment Ref:</b> {reservation_data['transaction_id']}</li>
        <li><b>Total Rooms Booked:</b> {reservation_data['room_count']}</li>
        <li><b>Hotel Name:</b> {reservation_data['resort']['name']}</li>
        <li><b>Room Type(s):</b> {reservation_data['resort']['category']}</li>
        <li><b>Check-In Date:</b> {reservation_data['check_in']}</li>
        <li><b>Check-Out Date:</b> {reservation_data['check_out']}</li>
        <li><b>Total cost:</b> {formatted_cost}</li>
    </ul>
    <p>Warm regards,<br><b>Team BGM 2026</b><br><i>Network • Navigate • Nostalgia</i></p>
    </body>
    </html>
    """
    message.add_alternative(body, subtype="html")

    pdf_bytes = generate_invoice_pdf_bytes(reservation_data)
    message.add_attachment(
        pdf_bytes,
        maintype="application",
        subtype="pdf",
        filename=f"Invoice_{reservation_data['id']}.pdf"
    )

    try:
        with smtplib.SMTP_SSL(os.getenv("IMAP_SERVER"), 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(message)
            print(f"Booking Confirmation email with invoice sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send booking confirmation email: {e}")

