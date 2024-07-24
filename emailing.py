import smtplib
import imghdr
import time
from email.message import EmailMessage

PASSWORD = "lyumymaqxmijipqu"
SENDER = "kanadaaryan9@gmail.com"
RECEIVER = "kanadaaryan9@gmail.com"


def send_email(image_path):
    print("st mail")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we saw a new coustmer!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()
    print("end ma")


if __name__ == "__main__":
    send_email(image_path="images/19.png")