from playwright.sync_api import sync_playwright
import re
import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def clean_text(text):
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_structured_sections(page):
    sections = page.locator("section")
    structured = []
    for i in range(sections.count()):
        try:
            section_text = sections.nth(i).inner_text(timeout=3000)
            section_text = clean_text(section_text)
            if len(section_text.split()) >= 10:
                structured.append(section_text)
        except:
            continue
    return structured

def scrape_company_website(url):
    print(f"Scraping company website: {url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        company_name = page.title()
        body_text = page.inner_text("body")
        structured_sections = extract_structured_sections(page)
        browser.close()

        full_text = clean_text(body_text)
        return {
            "company_name": company_name,
            "url": url,
            "raw_text": full_text,
            "structured_sections": structured_sections
        }

def scrape_linkedin(linkedin_url):
    print(f"Scraping LinkedIn page: {linkedin_url}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", LINKEDIN_EMAIL)
        page.fill("input#password", LINKEDIN_PASSWORD)
        page.click("button[type='submit']")
        page.wait_for_timeout(5000)

        page.goto(linkedin_url, timeout=60000)
        page.wait_for_timeout(5000)

        profile_text = page.inner_text("body")
        structured_sections = extract_structured_sections(page)

        posts = []
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(3000)

        post_elements = page.locator("div.feed-shared-update-v2")
        for i in range(min(5, post_elements.count())):
            try:
                post_text = post_elements.nth(i).inner_text(timeout=3000)
                posts.append(clean_text(post_text))
            except:
                continue

        logo_url = ""
        try:
            logo = page.locator("img.org-top-card-primary-content__logo").first
            logo_url = logo.get_attribute("src")
            if logo_url:
                os.makedirs("scraped", exist_ok=True)
                img_data = requests.get(logo_url).content
                with open("scraped/logo.png", "wb") as handler:
                    handler.write(img_data)
        except:
            pass

        browser.close()

        return {
            "linkedin_url": linkedin_url,
            "linkedin_profile_text": clean_text(profile_text),
            "linkedin_sections": structured_sections,
            "linkedin_posts": posts,
            "logo_url": logo_url
        }

def save_combined_data(company_data, linkedin_data):
    combined = {**company_data, **linkedin_data}
    os.makedirs("scraped", exist_ok=True)
    with open("scraped/prospect.json", "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    print("Saved all data to scraped/prospect.json")

if __name__ == "__main__":
    company_url = input("Enter company website URL: ").strip()
    linkedin_url = input("Enter LinkedIn company page URL: ").strip()
    company_data = scrape_company_website(company_url)
    linkedin_data = scrape_linkedin(linkedin_url)
    save_combined_data(company_data, linkedin_data)
