from playwright.sync_api import sync_playwright
import os
import re
from dotenv import load_dotenv
import requests
from openai import OpenAI

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def clean_text(text):
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def scrape_linkedin_profile(profile_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", LINKEDIN_EMAIL)
        page.fill("input#password", LINKEDIN_PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_timeout(5000)

        page.goto(profile_url, timeout=60000)
        page.wait_for_timeout(5000)

        profile_text = clean_text(page.inner_text("body"))
        browser.close()
        return profile_text

def run_openai_summary(text):
    prompt = f"""
You are a professional business analyst helping a sales team.

Given the following raw LinkedIn profile text of a prospect, write a smart, concise summary highlighting:
- The prospect's current role, background, and expertise
- Their likely decision-making power or influence
- Any signals that suggest they're a good lead

Only output the plain summary. No intro or formatting.

{text}
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You analyze sales prospects."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return res.choices[0].message.content.strip()

if __name__ == "__main__":
    linkedin_url = input("Enter LinkedIn profile URL: ").strip()
    raw_text = scrape_linkedin_profile(linkedin_url)

    os.makedirs("scraped", exist_ok=True)
    with open("scraped/message.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)

    summary = run_openai_summary(raw_text)
    with open("scraped/prospect.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("Scraped and saved: message.txt and prospect.txt")
