# ActionSync Sales Deck Automation

> Proprietary B2B pitch deck automation tool customized for internal use by ActionSync. Developed by Ritij Srivastava (Founder, Vertaflow).

---

## Overview

This project streamlines B2B pitch deck creation by:

* Scraping the company website
* Logging into and scraping the LinkedIn company profile (and logo)
* Using GPT (via OpenAI) to generate slide content
* Inserting that content and logo into a .pptx template

### Bonus:

You can also run `Personalized_Message.py` separately to:

* Scrape a LinkedIn **person's profile**
* Generate a smart outreach summary using GPT

---

## Features

* Fully automated deck generation by running just one command
* Scrapes both website + LinkedIn company page
* Inserts scraped **company logo** into the pitch deck
* Uses `gpt-4o-mini` to create custom slide content
* Outputs a ready-to-send PowerPoint file

---

## Requirements

> Works on **Windows**, **macOS**, or **Linux** (Python 3.9+)

### 1. Clone the Repo

```bash
git clone https://github.com/Ritij-AI-Artisan/ActionSync.git
cd ActionSync
```

### 2. Setup Python Virtual Environment

#### Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

---

## Project Structure

```
ActionSync/
├── app.py                       # Entry point (run this)
├── Scraper.py                   # Scrapes website + LinkedIn + logo
├── LLM_output.py                # Generates JSON slide content using GPT
├── Personalized_Message.py     # (Optional) Scrapes a person's LinkedIn profile
├── ActionSync_details.txt       # Company boilerplate (used in GPT prompt)
├── openai_output.json           # GPT-generated content
├── scraped/                     # Stores scraped JSON, logo.png, message.txt
├── output/                      # Final generated PPT decks
├── .env                         # Store API keys + LinkedIn login
├── requirements.txt             # All dependencies
├── LICENSE                      # Custom license (see below)
```

---

## .env Format

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-openai-key
LINKEDIN_EMAIL=your-email
LINKEDIN_PASSWORD=your-password
```

---

## Run the Full Pipeline

```bash
python app.py
```

You'll be prompted to input:

* Company Website URL
* LinkedIn Company Page URL

The deck will be saved under `output/Final_ActionSync_Deck_<Client>.pptx`

---

## (Optional) Run Prospect Intelligence

```bash
python Personalized_Message.py
```

Enter a LinkedIn **profile URL** and it will output:

* `scraped/message.txt` — full scraped profile text
* `scraped/prospect.txt` — GPT-written summary

---

## requirements.txt

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

> This list includes only required packages. No redundancies.

---

## Updating the Repo

```bash
git add .
git commit -m "Refactor: updated scraping + logo injection"
git push
```

---

## Troubleshooting

* `playwright` errors? ➡ Run `playwright install`
* Deck not generating? ➡ Ensure `.env` and `ActionSync_details.txt` exist
* Logo not inserting? ➡ Make sure the LinkedIn page has a logo image

---

## Licensing

This project is **not open-source**.

> This codebase is the intellectual property of **Ritij Srivastava (Founder, Vertaflow)** and is licensed **solely for internal use by Mr. Tushar Dublish (Founder, ActionSync)**.

* Redistribution, sublicensing, or commercial resale is **strictly prohibited** without **written permission** from Ritij Srivastava.
* The product may not be integrated into a paid/proprietary software platform without prior agreement.
* Violations will result in legal action.

See [LICENSE](LICENSE) for full legal terms.

---

## Built with dedication by [Ritij Srivastava](https://github.com/Ritij-AI-Artisan)

