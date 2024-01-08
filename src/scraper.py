from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import sys
import smtplib

def compare_files(file01, file02):
    with open(file01, 'r') as file1, open(file02, 'r') as file2:
        for line1, line2 in zip(file1, file2):
            if line1 != line2:
                return False
            
        # Check if one file has more lines than the other
        if file1.readline() or file2.readline():
            return False
            
    return True

# Load env variables
load_dotenv()

# Put the website into a string
website = os.getenv('WEBSITE')

# Validate the env variable
if not website:
    print("Website environment variable not set!!")
    sys.exit(1)

with open(website, 'r', encoding='Shift_JIS') as webdoc:
    htmlContent = webdoc.read()

# Parse the website using Python's html parser
soup = BeautifulSoup(htmlContent, 'html.parser')
#print(soup.prettify())

# Find the safety information notice inside the website
for tag in soup.find_all('b'):
    temp = tag.get_text()
    if temp.find("As of") != -1:
        safetyInfo = temp
        break

# Save safety information string into a file
with open('today.txt', 'w') as out:
    out.write(safetyInfo)

# Compare the safety information from two different days
isEqual = compare_files('today.txt', 'yesterday.txt')

# Send notification if safety information has changed
if not isEqual:
    EMAIL = os.getenv('EMAIL_ADDR')
    PASS = os.getenv('EMAIL_PASS')

    # Validate env variables
    if not EMAIL or not PASS:
        print("Email or Pass environmental variable not set!!")
        sys.exit(1)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL, PASS)

        subject = "Safety information update"
        body = "Safety information has changed:\n" + safetyInfo

        message = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL, EMAIL, message)

    # Update yesterday.txt for tomorrow's new comparison
    with open('yesterday.txt', 'w') as out:
        out.write(safetyInfo)

    print("An email was sent!!")

