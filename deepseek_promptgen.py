

from openai import OpenAI

key = input("Please input your key from OpenRouter: ")
modality = input("Please input your desired modality for information communication (text, image, or audio): ")
company = input("What kind of company do you work at (business, logistics, transport, etc)? ")
position = input("What is your position (floor manager, cargo driver, project manager, ect): ")

with open("summary.txt","r") as f:
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
    messages=[{"role": "user", "content": f"Could you generate a prompt for {modality} generation that would produce an image easily understood by a {position} at a {company} for the following project proposal : {proposal}"}]
)

f = open("prompt.txt", "w")
f.write(completion.choices[0].message.content)
f.close()
