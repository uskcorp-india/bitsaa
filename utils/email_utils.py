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
    print(f"Welcome message  {message}")
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
  
  <a href="https://bitsaa.d9events.in/?order_id={order_id}&ticket_count={ticket_count}" 
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
    message["From"] =  os.getenv("EMAIL_USER")
    recipient_email = reservation_data.get('registration')[0]['registrantEmail']
    message["To"] = ", ".join([recipient_email, message["From"]])
    message["Subject"] = "🏨 Your BGM 2026 Hotel Booking is Confirmed!"
    total_cost = int(reservation_data['total_cost'].strip('"').strip())
    formatted_cost = f"₹{total_cost:,.0f}"


    registration_data = reservation_data.get('registration', [])

    if len(registration_data) >= 1:
        group_members = [
            f"{reg.get('registrantName', '')}".strip()
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
     <!-- Logo -->
    <div style="text-align: left; margin-bottom: 10px;">
      <img src="https://bitsaa.d9events.in/wp-content/uploads/2025/08/d9_EVENTS_LOGO.png"  alt="BGM 2026 Logo" style="max-height:100px;">
    </div>
    
    <p>Hi {reservation_data.get('registration')[0]['registrantName'] },</p>

<p>We’re delighted to let you know that your <strong>accommodation for BITSAA Global Meet 2026</strong><br> has been successfully booked! 🥳<br>&nbsp;Your stay is now secured, and you're one step closer to experiencing an exciting and <br>memorable three-day celebration at the <strong>BITS Hyderabad Campus from January 9–11, 2026</strong>.
</p>
<p style="margin-top: 10px;">Here are your hotel reservation details:</p>
<hr>
   <div style="line-height: 1.9;">
<h3><b>📌 Reservation Summary</b></h3>
<ul>
    <li><b>Registrant Name:</b> {registration_data[0]['registrantName']}</li>
    {group_info}
    <li><b>Reservation id:</b> {reservation_data['id']}</li>
    <li><b>Payment Ref:</b> {reservation_data['transaction_id']}</li>
    <li><b>Total Rooms Booked:</b> {reservation_data['room_count']}</li>
    <li><b>Hotel Name:</b> {reservation_data['resort']['name']}</li>
    <li><b>Room Type(s):</b> {reservation_data['resort']['category']}</li>
    <li><b>Check-In Date:</b> {reservation_data['check_in']}</li>
    <li><b>Check-Out Date:</b> {reservation_data['check_out']}</li>
    <li><b>Total cost:</b> {formatted_cost}</li><br>
    </ul>
    </div>
    <hr><br>
    Your hotel team will be informed of your arrival, and further details regarding check-in <br> procedures will be shared closer to the event.<br>
<hr>
    We can’t wait to welcome you to Hyderabad for a weekend full of networking and BITSian spirit!<br><br>
    
    Warm regards,<br>
    <b>Team BGM 2026</b><br>
   <i>Network • Navigate • Nostalgia</i>
   <p>Contact Us Anytime<br>
   Phone: <a href="tel: +919700242473">+919700242473</a> / <a href="tel:+919898476944">+919898476944</a></p>
    </body>
    </html>
    """
    message.add_alternative(body, subtype="html")

    try:
        with smtplib.SMTP_SSL(os.getenv("IMAP_SERVER"), 465) as server:
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(message)
            print(f"Booking Confirmation email sent to { reservation_data.get('registration')[0]['registrantEmail']}")
    except Exception as e:
        print(f"Failed to send booking confirmation email: {e}")
