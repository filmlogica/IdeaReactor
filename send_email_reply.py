import os
import yagmail
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASS = os.getenv("EMAIL_PASS")

def send_auto_reply(to_email, subject, message_body):
    yag = yagmail.SMTP(EMAIL, PASS)
    yag.send(
        to=to_email,
        subject=subject,
        contents=message_body
    )
    print(f"📬 Replied to {to_email}")

# Example use
if __name__ == "__main__":
    send_auto_reply("example@example.com", "Thanks for your question!", "Hey! We'll get back to you soon about IdeaReactor. Stay awesome.")

