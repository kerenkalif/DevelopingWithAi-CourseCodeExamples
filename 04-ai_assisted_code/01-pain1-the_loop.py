import smtplib

def send_email(to, subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("me@gmail.com", "mypassword")
    server.sendmail("me@gmail.com", to, f"Subject: {subject}\n\n{body}")
    server.quit()

send_email("student@gmail.com", "hi", "this is a test email")