import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


with open("scraped/prospect.json", "r", encoding="utf-8") as f:
    prospect_data = json.load(f)

company_text = prospect_data.get("raw_text", "")
linkedin_text = prospect_data.get("linkedin_profile_text", "")
linkedin_posts = "\n".join(prospect_data.get("linkedin_posts", []))

prompt = f"""
You are a digital presence analyst. Using the information provided, fill in the
following JSON template with concise values. Respond ONLY with JSON and do not
include any explanations.

{{
  "ProspectName": "",
  "CXOPositioning": "",
  "StrategicInsight": "",
  "ProfilePhotoStatus": "",
  "ProfilePhotoFixable": "",
  "HeadlineStatus": "",
  "HeadlineFixable": "",
  "CoverImageStatus": "",
  "CoverImageFixable": "",
  "AboutNarrativeStatus": "",
  "AboutFixable": "",
  "FirstImpressionSummary": "",
  "TotalFollowers": "",
  "PeerFollowers": "",
  "PostsPerMonth": "",
  "EngagementRate": "",
  "DaysSinceLastPost": "",
  "AuthorityScore": "",
  "AuthorityNotes": "",
  "ProofScore": "",
  "ProofNotes": "",
  "FounderVisibilityScore": "",
  "FounderNotes": "",
  "TrustHookScore": "",
  "TrustHookNotes": "",
  "FixableGap1": "",
  "FixableGap2": "",
  "FixableGap3": ""
}}

Company Website Text:
{company_text}

LinkedIn Profile Text:
{linkedin_text}

Recent LinkedIn Posts:
{linkedin_posts}
"""


def extract_json(text: str) -> str:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1)
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1)
    raise ValueError("No JSON found in model response.")


def main() -> None:
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You only return JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )
    content = res.choices[0].message.content.strip()
    json_content = json.loads(extract_json(content))

    os.makedirs("output", exist_ok=True)
    with open("openai_output.json", "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=2)

    print("Saved: openai_output.json")


if __name__ == "__main__":
    main()
