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
    print(f"Preparing to send email with job links...{job_links}")
    if not job_links:
        job_links = ["No job openings found today."]

    # Create HTML content
    html_links = ''.join(f'<li><a href="{link}" target="_blank">{link}</a></li>' for link in job_links)
    html_content = f"""
    <html>
        <body>
            <h2>🔎 Daily Job Openings - {datetime.now().strftime('%Y-%m-%d')}</h2>
            <p>Here are the top job links matching your search:</p>
            <ul>
                {html_links}
            </ul>
            <hr>
            <p style="font-size: 12px; color: #888;">This is an automated email sent by your job search bot.</p>
        </body>
    </html>
    """

    msg = MIMEText(html_content, "html")
    msg['Subject'] = f"💼 Job Alerts - {datetime.now().strftime('%Y-%m-%d')}"
    msg['From'] = sender
    msg['To'] = receiver

    # Use Gmail with TLS
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(sender, password)
        smtp.send_message(msg)

    # Save to local file for logging
    with open("job_results.html", "w", encoding="utf-8") as f:
        f.write(html_content)


if __name__ == "__main__":
    jobs = search_jobs()
    send_email(jobs)
