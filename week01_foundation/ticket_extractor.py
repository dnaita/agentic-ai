import os
import json
from pydantic import ValidationError
from google import genai
from google.genai import types
from dotenv import load_dotenv

from models import CustomerTicket

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

raw_ticket_text = """
Hi, this is John Doe. I am absolutely furious. I was charged twice for my 
subscription this month. I need this fixed immediately or I'm cancelling my 
account. It's the second time this has happened.
"""

def extract_ticket(text: str) -> CustomerTicket:
    prompt = f"Extract the customer ticket information from the following text and return only valid JSON:\n\n{text}"
    error_feedback = ""

    for attempt in range(1,4):
        print(f"Attempt {attempt} to extract ticket information...")

        #1. Call Gemini
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt + error_feedback,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )

        raw_response = response.text
        print(f"Raw LLM Output: {raw_response}")

        try:
            #2. Parse the JSON response into a CustomerTicket object
            data = json.loads(raw_response)
            #3. Validate and create a CustomerTicket instance
            ticket = CustomerTicket(**data)
            return ticket

        except (json.JSONDecodeError, ValidationError) as e:
            print(f" Validation Failed: {e}")
            #4. "reflect": Add the error to the prompt for the next attempt
            error_feedback = f"\n\nYour previous response failed validation with this error:\n{e}\nPlease fix the JSON and try again."

    raise Exception("Failed to extract a valid CustomerTicket after 3 attempts.")

if __name__ == "__main__":
    try:
        ticket = extract_ticket(raw_ticket_text)
        print("\n✅ Successfully Extracted:")
        print(ticket.model_dump_json(indent=2))
    except Exception as e:
        print(f"\n🛑 Fatal Error: {e}")