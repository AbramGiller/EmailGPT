import os
import email
from email import policy
from bs4 import BeautifulSoup

def parse_emails(directory, keywords):
    emails = []
    for filename in os.listdir(directory):
        if filename.endswith(".eml"):
            with open(os.path.join(directory, filename), "r") as file:
                raw_email = file.read()
                email_message = email.message_from_string(raw_email, policy=policy.default)
                
                parsed_email = {}
                parsed_email["Subject"] = email_message["Subject"]
                parsed_email["From"] = email_message["From"]
                parsed_email["To"] = email_message["To"]
                
                # Initialize text_content and html_content
                text_content = ""
                html_content = ""

                # Get the email body
                if email_message.is_multipart():
                    for part in email_message.iter_parts():
                        if part.get_content_type() == 'text/plain':
                            text_content = part.get_content()
                        elif part.get_content_type() == 'text/html':
                            html_content = part.get_content()
                else:
                    text_content = email_message.get_content()
                
                # If there is HTML content and no text content
                if not text_content and html_content:
                    soup = BeautifulSoup(html_content, "html.parser")
                    text_content = soup.get_text()

                # Only include the email if one of the keywords is in the body
                if any(keyword.lower() in text_content.lower() for keyword in keywords):
                    parsed_email["Body"] = text_content
                    emails.append(parsed_email)

    return emails

# Usage
directory = input("Enter the directory path: ").strip()
keywords = input("Enter the keywords, separated by commas: ").split(",")
keywords = [keyword.strip() for keyword in keywords]  # Remove whitespace
emails = parse_emails(directory, keywords)
for email in emails:
    print(email)