import google.generativeai as genai
import requests
import os

# ✅ Insert your actual keys here (better: use env vars in real use)

genai.configure(api_key="AIzaSyBPz7vic2EThir4iYE0_bmgeY1JYwa-Gso")
access_token = "AQW_6CFPKKcNCVPRqHNrKdS1twAsnpI3pUa4ZyuRiqY3qr9NVCoO-KzpRhNbzbaNkNXSVpzUUATHRqjCcOK2rTYFCAsKVmSJEfc8Y2C0OhGd8fI79jucziWQ3Jnl-tlLQ8fJbMrEDkQQ5CNs1LOsHaDH1WxFYajqT2cQQdByjCV1qf7T8xYCohi2heYai3_4U2fDDpSSpN_YpJ7UzBMHUKD-4_2d0mwnfm1H3gNr32IM-IAMWSfnl-0JPSFjjBVq_JsmsCQwwRA3O0S9o-7OMvaMV0o7V9WuH2uxwGeWQeErFanzXpHtXq64zMlEJRpTN-0362WApu-4zW2SELpWJXT3DlS8cg"     # Your real LinkedIn token
linkedin_urn = "urn:li:person:67eqmXVQy_"  # Replace this

prompt = (
    "Write a short LinkedIn post (under 180 words) about a trending tech topic. "
    "Use storytelling, psychology and human tone. Avoid technical jargon. Make it feel personal and thought-provoking. make easy english and something beautiful and new also sometime discuss ever green topics"
)
# 🔹 1. Generate content using Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content(prompt)
post_text = response.text.strip()

# 🔹 2. Prepare LinkedIn API headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

# 🔹 3. Prepare LinkedIn post payload
data = {
    "author": linkedin_urn,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {"text": post_text},
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

# 🔹 4. Post to LinkedIn
response = requests.post(
    "https://api.linkedin.com/v2/ugcPosts",
    headers=headers,
    json=data
)

print("Posted to LinkedIn:", response.status_code)
if response.status_code >= 400:
    print("Error:", response.json())
