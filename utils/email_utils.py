import os
import smtplib
from email.message import EmailMessage
import aiosmtplib



def send_welcome_email(recipient_email: str, first_name: str, order_id: str, ticket_count: int):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = recipient_email
    message["Subject"] = "🎉 Welcome to BGM 2026 – Let’s Get You Settled!"
    message['X-Priority'] = '1'
    message['X-MSMail-Priority'] = 'High'
    message['Importance'] = 'High'
    print(f"message++++++  {message}")
    body = f"""
    <!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Welcome to BGM 2026</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
  <p>Hi <strong>{first_name}</strong>,</p>

  <p><strong>Congratulations – your registration for <em>BITSAA Global Meet 2026</em> is confirmed! 🎊</strong></p>

  <p>We’re thrilled to have you on board for three unforgettable days of connection, inspiration, and nostalgia at the <strong>BITS Hyderabad Campus from January 9–11, 2026</strong>.</p>

  <p>Now that you've taken the first step, it's time to complete your BGM journey by booking your accommodation. To make this process smooth, please follow the simple steps below:</p>
  <hr>
  <h3>🛏️ How to Book Your Accommodation:</h3>

  <p style="margin-bottom: 12px;">
  <strong>STEP 1: XYZ</strong><br>
  Fill out the accommodation form with your registration ID.
</p>

<p style="margin-bottom: 12px;">
  <strong>STEP 2: ABC</strong><br>
  Choose your room category based on your group size or preference.
</p>

<p>
  <strong>STEP 3: UPO</strong><br>
  Upload proof of payment or confirm your booking.
</p>
  <hr>
  <p>Following these steps will ensure that your stay is comfortably arranged and you're all set to experience the magic of BGM hassle-free.</p>

  <p>If you have any questions or need help, don’t hesitate to reach out to us at 
    <a href="mailto:bgm-communications@bitsaa.org">bgm-communications@bitsaa.org</a>.
  </p><br>
  
  <a href="https://bgm2026.com/registration/?order_id={order_id}&ticket_count={ticket_count}" 
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
  Click here for booking
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


# 🏨 Hotel Booking Confirmation Email
async def send_booking_confirmation_email(reservation_data: dict):
    message = EmailMessage()
    message["From"] = os.environ.get("EMAIL_USER")
    message["To"] = reservation_data.get('registration')[0]['email']
    message["Subject"] = "🏨 Your BGM 2026 Hotel Booking is Confirmed!"

    registration_data = reservation_data.get('registration', [])

    if len(registration_data) > 1:
        group_members = [
            f"{reg.get('first_name', '')} {reg.get('last_name', '')}".strip()
            for reg in registration_data
        ]
        members_list = f"• <strong>[1]</strong> {group_members[0]} (Registrant)"
        others = "\n".join([f"• <strong>[{i + 2}]</strong> {name}" for i, name in enumerate(group_members[1:])])
        group_info = f"<strong>Group Members:</strong><br>{members_list}<br>{others}"
    else:
        group_info = ""

    body = f"""
    <html>
    <body>
    Hi {reservation_data.get('registration')[0] ['first_name']},<br><br>

    We’re delighted to let you know that your <strong>accommodation for BITSAA Global Meet 2026</strong> has been successfully booked!🥳<br>
    &nbsp;Your stay is now secured, and you're one step closer to experiencing an exciting and memorable three-day celebration at the <strong>BITS Hyderabad Campus from January 9–11, 2026</strong>.<br><br>
    Here are your hotel reservation details:<br><br>
    <strong>📌Reservation Summary</strong><br><br>
    <div style="line-height: 1.8; font-family: sans-serif">
    <strong>Registrant Name:</strong> {registration_data[0]['first_name']} {registration_data[0]['last_name']}<br>
    <strong>Group Members:</strong><br>
    •<strong>[1]</strong> {registration_data[0]['first_name']} {registration_data[0]['last_name']} (Registrant)<br>
    {"".join([f" {reg['first_name']} {reg['last_name']}<br>" for i, reg in enumerate(registration_data[1:])])}
    <strong>Total Rooms Booked:</strong> {reservation_data['room_count']}<br>
    <strong>Hotel Name:</strong> {reservation_data['resort']['name']}<br>
    <strong>Room Type(s):</strong> {reservation_data['resort']['category']}<br>
    <strong>Check-In Date:</strong> {reservation_data['check_in']}<br>
    <strong>Check-Out Date:</strong> {reservation_data['check_out']}
    </div><br>
    Your hotel team will be informed of your arrival, and further details regarding check-in procedures will be shared closer to the event.<br><br>

    We can’t wait to welcome you to Hyderabad for a weekend full of networking and BITSian spirit!<br><br>

    Warm regards,<br>
    <strong>Team BGM 2026</strong><br>
    Network • Navigate • Nostalgia
    </body>
    </html>
    """
    message.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=os.environ["IMAP_SERVER"],
        port=os.environ["IMAP_PORT"],
        username=os.environ["EMAIL_USER"],
        password=os.environ["EMAIL_PASSWORD"]
    )