import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.

For the given user input, analyse the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.

Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".

Rules:
1. Follow the strict JSON output as per Output schema.
2. Always perform one step at a time and wait for next input
3. Carefully analyse the user query

Output Format:
{{ step: "string", content: "string" }}

Example:
Input: What is 2 + 2.
Output: {{ step: "analyse", content: "Alright! The user is intersted in maths query and he is asking a basic arthermatic operation" }}
Output: {{ step: "think", content: "To perform the addition i must go from left to right and add all the operands" }}
Output: {{ step: "output", content: "4" }}
Output: {{ step: "validate", content: "seems like 4 is correct ans for 2 + 2" }}
Output: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all numbers" }}
"""

messages = []

query = input("> ")
messages.append({"role": "user", "parts": [{"text": query}]})

while True:
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json"
        ),
    )

    response_text = response.text.strip()

    
    try:
        parsed_response = json.loads(response_text)
    except Exception as e:
        print("❌ Failed to parse JSON. Model said:\n", response.text)
        print("Error:", e)
        break

    messages.append({"role": "model", "parts": [{"text": json.dumps(parsed_response)}]})

    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get('content')}")
        continue

    print(f"🤖: {parsed_response.get('content')}")
    break
