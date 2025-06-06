# ActionSync AI-Powered Sales Deck Generator

Automatically create a personalized sales pitch deck using a client’s website and LinkedIn data, combined with OpenAI-generated slide content and branding elements.

---

## Overview

ActionSync automates the manual, repetitive task of creating personalized B2B sales pitch decks. It scrapes key business information, generates relevant content using GPT, and injects it into a pre-designed PowerPoint template—complete with logos and summaries.

### Core Functionality

* Scrapes **company website** and **LinkedIn company page**
* Downloads and embeds the **company logo**
* Uses **OpenAI GPT (gpt-4o-mini)** to generate tailored slide content
* Populates a .PPTX template with all generated data
* Outputs a client-ready deck with **one command**

### Bonus Feature

* A separate script for scraping a **LinkedIn profile** and generating a smart prospect message

---

## Features

* Automates all steps from data scraping to deck generation
* Scrapes structured content and posts from LinkedIn
* Extracts and places the company’s logo into slide 13
* Summarizes profile data into outreach insights
* Fully command-line operated; no manual edits required
* Cross-platform: **Works on Windows, macOS, and Linux**

---

## Project Structure

```
ActionSync/
├── app.py                       # Entry point – runs scraper, GPT, and slide update
├── Scraper.py                   # Scrapes company site and LinkedIn (with logo)
├── LLM_output.py                # Generates slide content via GPT
├── Personalized_Message.py      # (Optional) Scrapes a LinkedIn person’s profile
├── ActionSync_details.txt       # Boilerplate info used in GPT prompts
├── openai_output.json           # GPT response for slides 1, 13–18
├── scraped/                     # Contains:
│   ├── logo.png                 # Company logo from LinkedIn
│   ├── message.txt              # Raw LinkedIn profile (optional)
│   ├── prospect.txt             # GPT summary of the profile (optional)
│   └── prospect.json            # All scraped input data
├── output/                      # Final deck output
├── .env                         # API and login credentials (not committed)
├── requirements.txt             # Python dependencies
```

---

## Getting Started

> These instructions work for **Windows**, **macOS**, and **Linux**

### Step 1: Clone the Repository

```bash
git clone https://github.com/Ritij-AI-Artisan/ActionSync.git
cd ActionSync
```

### Step 2: Create Virtual Environment

#### On Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers

```bash
playwright install
```

### Step 5: Configure Environment Variables

Create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your_openai_key
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

---

## Running the Automation

### Generate Sales Deck (Full Flow)

```bash
python app.py
```

You’ll be prompted to enter:

* Company Website URL
* LinkedIn Company Page URL

This will generate:

* `scraped/prospect.json` (scraped data)
* `scraped/logo.png` (company logo)
* `openai_output.json` (slide content from GPT)
* `output/Final_ActionSync_Deck_<ClientName>.pptx` (final deck)

### Generate Prospect Summary (Optional)

```bash
python Personalized_Message.py
```

You’ll be prompted to enter a **LinkedIn profile URL** of a person.

This generates:

* `scraped/message.txt` (raw scraped profile)
* `scraped/prospect.txt` (GPT summary)

---

## requirements.txt (Final Cleaned List)

```
aiohttp==3.12.7
anyio==4.9.0
colorama==0.4.6
dotenv==0.9.9
openai==1.84.0
playwright==1.52.0
pillow==11.2.1
python-dotenv==1.1.0
python-pptx==1.0.2
requests==2.32.3
re==0.0.2
```

> This file includes only direct and relevant dependencies for core functionality.

---

## Updating the Repository

```bash
git add .
git commit -m "Updated scraping logic and logo embedding"
git push
```

---

## Troubleshooting

* **playwright.errors**: Run `playwright install`
* **Deck not updating**: Ensure `ActionSync_details.txt` exists and `.env` is filled
* **Missing logo**: LinkedIn logo might not load due to privacy or login restrictions

---

## Author

Made by Ritij Srivastava — [GitHub Profile](https://github.com/Ritij-AI-Artisan)

For enterprise use, contributions, or licensing queries, please open an issue or contact directly.
