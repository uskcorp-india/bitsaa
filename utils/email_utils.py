import os
import smtplib
from email.message import EmailMessage



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

def send_booking_confirmation_email(reservation_data:dict):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_USER")
    message["To"] = reservation_data.get('registration')[0]['email']
    message["Subject"] = "🏨 Your BGM 2026 Hotel Booking is Confirmed!"


    registration_data = reservation_data.get('registration', [])

    if len(registration_data) > 1:
        group_members = [
            f"{reg.get('first_name', '')} {reg.get('last_name', '')}".strip()
            for reg in registration_data
        ]
        members_list = f"<li> {group_members[0]} (Registrant) </li>"
        others = "\n".join(f" <li> {name} </li> " for i, name in enumerate(group_members[1:]))
        group_info = f"<li><b>Group Members:</b></li> <ul style='list-style-type: circle'>{members_list}{others}</ul>"
    else:
        group_info = ""

    body = f"""
    <html>
    <body>
    <p>Hi {reservation_data.get('registration')[0] ['first_name'] } {reservation_data.get('registration')[0] ['last_name']},</p>

<p>We’re delighted to let you know that your <strong>accommodation for BITSAA Global Meet 2026</strong><br> has been successfully booked! 🥳<br>&nbsp;Your stay is now secured, and you're one step closer to experiencing an exciting and <br>memorable three-day celebration at the <strong>BITS Hyderabad Campus from January 9–11, 2026</strong>.
</p>
<p style="margin-top: 10px;">Here are your hotel reservation details:</p>
<hr>
   <div style="line-height: 1.9;">
<h3><b>📌 Reservation Summary</b></h3>
<ul>
    <li><b>Registrant Name:</b> {registration_data[0]['first_name']} {registration_data[0]['last_name']}</li>
    <li><b>Group Members:</b></li>
     <ul style="list-style-type: circle">
        {group_info}
    </ul>
    <li><b>Total Rooms Booked:</b>{reservation_data['room_count']}</li>
    <li><b>Hotel Name:</b> {reservation_data['resort']['name']}</li>
    <li><b>Room Type(s):</b>{reservation_data['resort']['category']}</li>
    <li><b>Check-In Date:</b> {reservation_data['check_in']}</li>
    <li><b>Check-Out Date:</b>{reservation_data['check_out']}</li><br>
    </ul>
    </div>
    <hr><br>
    Your hotel team will be informed of your arrival, and further details regarding check-in <br> procedures will be shared closer to the event.<br>
<hr>
    We can’t wait to welcome you to Hyderabad for a weekend full of networking and BITSian spirit!<br><br>
    
    Warm regards,<br>
    <b>Team BGM 2026</b><br>
   <i>Network • Navigate • Nostalgia</i>
    </body>
    </html>
    """
    message.add_alternative(body, subtype="html")

    try:
        with smtplib.SMTP_SSL(os.getenv("IMAP_SERVER"), 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(message)
            print(f"Booking Confirmation email sent to { reservation_data.get('registration')[0]['email']}")
    except Exception as e:
        print(f"Failed to send booking confirmation email: {e}")



