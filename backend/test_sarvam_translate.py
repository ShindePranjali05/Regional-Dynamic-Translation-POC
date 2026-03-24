import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

client = SarvamAI(api_subscription_key=api_key)

response = client.text.translate(
    input="Apply ice to the injured area for 20 minutes every 2 hours.",
    source_language_code="en-IN",
    target_language_code="hi-IN",
    model="sarvam-translate:v1",
    #mode="formality"
)

print(type(response))
print(response)
