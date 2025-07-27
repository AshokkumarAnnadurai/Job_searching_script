import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()
sender = os.getenv("EMAIL_USER")
receiver = sender
password = os.getenv("EMAIL_PASS")

def search_jobs():
    query = "Software Developer OR Full MERN Stack Developer OR React Full Stack Developer jobs in Chennai OR Bangalore site:linkedin.com/jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for link in soup.select('a'):
        href = link.get('href')
        if href and 'linkedin.com/jobs' in href:
            cleaned = href.split("&")[0].replace("/url?q=", "")
            results.append(cleaned)
    return list(set(results))[:10]

def send_email(job_links):
    body = "\n".join(job_links) or "No jobs found today."
    msg = MIMEText(body)
    msg['Subject'] = f"Daily Job Openings - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = receiver

    # Use starttls (more reliable on some servers)
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)

    # Optional: Save output
    with open("job_results.txt", "w") as f:
        f.write(body)

if __name__ == "__main__":
    jobs = search_jobs()
    send_email(jobs)
