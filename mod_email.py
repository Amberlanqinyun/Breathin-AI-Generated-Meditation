import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


def send_email( receiver_email, subject, body_message, payment_amount=None, invoice_number=None, payment_date=None, isPayment= False):
    sender_email = 'darfieldcentre@gmail.com'
    #loginpassword = CenterAdmin12!
    sender_password = 'tjmx ojae rxvm vray'
    payment_receipt_image_path = 'static/logo.png'
    

    # Create a MIME object for the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body_message, 'plain'))
    if isPayment:
        # Attach payment receipt image (optional)
        if payment_receipt_image_path:
            with open(payment_receipt_image_path, 'rb') as attachment:
                img = MIMEImage(attachment.read(), _subtype="jpg")
                img.add_header('Content-Disposition', 'attachment',
                           filename=payment_receipt_image_path)
                msg.attach(img)

        # Payment receipt information
        payment_details = f"Payment Amount: ${payment_amount}\nInvoice Number: {invoice_number}\nPayment Date: {payment_date}"

        # Attach payment receipt information
        msg.attach(MIMEText(payment_details, 'plain'))

    # Establish a connection to the SMTP server (in this case, Gmail's SMTP server)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Email could not be sent. Error: {str(e)}")

    finally:
        # Close the SMTP server connection
        server.quit()


# Example usage

# receiver_email = 'chenyuechong@hotmail.com'
# payment_amount = 100.00
# invoice_number = 'INV12345'
# payment_date = '2023-10-15'
# subject = 'Payment Receipt'
# body_message = 'Thank you for your payment. Your payment receipt is attached.'

#send_email(receiver_email,subject,body_message, payment_amount, invoice_number, payment_date)
