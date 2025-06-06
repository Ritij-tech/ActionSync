import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


with open("scraped/prospect.json", "r", encoding="utf-8") as f:
    prospect_data = json.load(f)

with open("ActionSync_details.txt", "r", encoding="utf-8") as f:
    actionsync_details = f.read()


linkedin_text = prospect_data.get("linkedin_profile_text", "")
linkedin_posts = "\n".join(prospect_data.get("linkedin_posts", []))


slide_1_prompt = f"""
You are a senior sales executive at ActionSync, an AI-powered enterprise search platform.

We are currently engaged in the sales outreach process with a prospective company and need to personalize our pitch deck accordingly.

Your task is to update Slide 1 by identifying the client's company name based on the information provided below.

Return only the following plain JSON structure. Do not wrap it in markdown or backticks:
{{
  "Slide 1": {{
    "Client Company Name": "Actual Company Name"
  }}
}}

Company Website:
{prospect_data["raw_text"]}

LinkedIn Profile Summary:
{linkedin_text}
"""

slide_13_to_18_prompt = f"""
You are a senior sales executive at ActionSync, an AI-powered enterprise search platform.

We are preparing a personalized sales deck and need you to fill in content for slides 13 to 18 based on the provided company and product details.

Return the output in the following JSON structure — return FLAT KEYS as shown:

{{
  "Slide 13": {{
    "Slide13_Heading": "Company Snapshot",
    "ClientName": "LedgerUp",
    "Industry": "Software Development",
    "Location": "San Francisco, California, US",
    "Employees": "2-10 employees",
    "ClientSummary": "Brief summary of the client company."
  }},
  "Slide 14": {{
    "Slide14_Heading": "Key Challenges",
    "ClientChallenge1": "...",
    "ClientChallenge2": "...",
    "ClientChallenge3": "...",
    "ChallengeImpact": "..."
  }},
  "Slide 15": {{
    "Slide15_Heading": "ActionSync in Action",
    "ClientApps": "...",
    "ClientDocs": "...",
    "ClientTools": "..."
  }},
  "Slide 16": {{
    "Slide16_Heading": "Use Case Scenarios",
    "ClientUseCaseA": "...",
    "ClientUseCaseB": "...",
    "ClientUseCaseC": "..."
  }},
  "Slide 17": {{
    "Slide17_Heading": "Proposal & POC Plan",
    "PilotProposal": "...",
    "RelevantFeatures": "...",
    "ClientPainPoints": "...",
    "SuccessMetrics": "...",
    "POCTimeline": "..."
  }},
  "Slide 18": {{
    "Slide18_Heading": "Next Steps",
    "CallToAction": "..."
  }}
}}

Use only the data provided below to populate the values. Do NOT nest keys. Do NOT wrap the response in backticks.

ActionSync Product Description:
{actionsync_details}

Client Website Scraped Content:
{prospect_data["raw_text"]}

Client LinkedIn Profile Summary:
{linkedin_text}

Recent LinkedIn Posts:
{linkedin_posts}
"""


def extract_json_from_response(text: str) -> str:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No JSON found in model response.")


def query_openai(prompt: str) -> dict:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only returns flat JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    content = res.choices[0].message.content.strip()
    print("Raw response:\n", content)
    return json.loads(extract_json_from_response(content))


slide_1_json = query_openai(slide_1_prompt)
slides_13_to_18_json = query_openai(slide_13_to_18_prompt)


final_json = {**slide_1_json, **slides_13_to_18_json}
os.makedirs("output", exist_ok=True)
with open("openai_output.json", "w", encoding="utf-8") as f:
    json.dump(final_json, f, indent=2)

print("Saved: openai_output.json")
