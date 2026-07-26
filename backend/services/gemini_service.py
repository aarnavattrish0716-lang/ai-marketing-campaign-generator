from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_campaign(product, audience, platform):
    prompt = f"""
    Create a marketing campaign.

    Product: {product}
    Audience: {audience}
    Platform: {platform}

    Return:
    - Campaign Title
    - Tagline
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text  