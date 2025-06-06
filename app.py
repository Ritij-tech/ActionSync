import subprocess
import json
import os
from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image

print("Running scraper.py...")
subprocess.run([r"C:\Users\sriva\PycharmProjects\Sales_Deck\.venv/Scripts\python.exe", "scraper.py"], check=True)

print("Running LLM_output.py...")
subprocess.run([r"C:\Users\sriva\PycharmProjects\Sales_Deck\.venv/Scripts\python.exe", "LLM_output.py"], check=True)

pptx_template = r"E:\ActionSync.pptx"
json_path = "openai_output.json"
prs = Presentation(pptx_template)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

slide_1_data = data.get("Slide 1", {})
client_name = slide_1_data.get("Client Company Name", "Client")

slide_1 = prs.slides[0]
for shape in slide_1.shapes:
    if shape.has_text_frame and "{Client Company Name}" in shape.text:
        shape.text = shape.text.replace("{Client Company Name}", client_name)

def fill_slide(slide, replacements: dict):
    for shape in slide.shapes:
        if shape.has_text_frame:
            new_text = shape.text
            for key, value in replacements.items():
                placeholder = f"{{{key}}}"
                if placeholder in new_text:
                    new_text = new_text.replace(placeholder, str(value))
            shape.text_frame.clear()
            shape.text_frame.text = new_text

def insert_logo_image(slide):
    logo_path = "scraped/logo.png"
    if os.path.exists(logo_path):
        try:
            with Image.open(logo_path) as img:
                img.verify()
            left = Inches(6.5)
            top = Inches(2.0)
            height = Inches(1.2)
            for shape in list(slide.shapes):
                if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    slide.shapes._spTree.remove(shape._element)
            slide.shapes.add_picture(logo_path, left, top, height=height)
            print("Logo successfully inserted on Slide 13.")
        except Exception as e:
            print(f"Failed to insert logo: {e}")

slide_map = {
    13: ("Slide 13", "Slide13_Heading"),
    14: ("Slide 14", "Slide14_Heading"),
    15: ("Slide 15", "Slide15_Heading"),
    16: ("Slide 16", "Slide16_Heading"),
    17: ("Slide 17", "Slide17_Heading"),
    18: ("Slide 18", "Slide18_Heading")
}

if "slides" in data:
    for entry in data["slides"]:
        slide_num = entry.get("slide")
        content = entry.get("content", {})
        flat = {}
        for section in content.values():
            if isinstance(section, dict):
                flat.update(section)
            else:
                flat = content
                break
        slide = prs.slides[slide_num - 1]
        flat["ClientName"] = client_name
        fill_slide(slide, flat)
        if slide_num == 13:
            insert_logo_image(slide)
else:
    for slide_num, (slide_key, heading_key) in slide_map.items():
        slide = prs.slides[slide_num - 1]
        slide_data = data.get(slide_key, {})
        heading_text = slide_data.get(heading_key)
        if heading_text:
            for shape in slide.shapes:
                if shape.has_text_frame and f"{{{heading_key}}}" in shape.text:
                    shape.text = shape.text.replace(f"{{{heading_key}}}", heading_text)
        slide_data["ClientName"] = client_name
        fill_slide(slide, slide_data)
    insert_logo_image(prs.slides[12])

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"Final_ActionSync_Deck_{client_name.replace(' ', '_')}.pptx")
prs.save(output_file)

print(f"Presentation saved as {output_file}")
