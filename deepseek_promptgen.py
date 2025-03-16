import sys
from openai import OpenAI

key = sys.argv[1]
modality = sys.argv[2]
position = sys.argv[3]
company = sys.argv[4]
file = sys.argv[5]

with open(file,"r") as f:
    proposal = f.read()

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=key,
)

completion = client.chat.completions.create(
    extra_headers={
    "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
    "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="deepseek/deepseek-chat:free",
    messages=[{"role": "user", "content": f"Could you generate a prompt for {modality} generation with numbered steps (like step 1, step 2, ...) that would produce an image easily understood by a {position} at a {company} for the following project proposal : {proposal}"}]
)

f = open(f"prompts_{modality}.txt", "w")
f.write(completion.choices[0].message.content)
f.close()
