import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




def send_order_confirmation_email(email: str,Order ):
    
    order_details = f"Order ID: {Order.id}\n" \
                    f"User ID: {Order.user_id}\n" \
                    f"Product ID: {Order.product_id}\n" \
                    f"Total Amount: {Order.total_amount}\n" \
                  
                    
    sender_email = "budmahek2003@gmail.com"
    receiver_email = email
    password = "ipnobrgzhxskmjwe"
    subject = "Order Confirmation"
    message_text = f"Thank you for your order! Your order details: {order_details}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    
    
    message.attach(MIMEText(message_text, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Mail sent successfully")
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")