import os
import requests
import google.generativeai as genai

# Set up Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY_ERROR"))
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = (
    "Give me a random short, engaging LinkedIn post (under 300 words) on a trending software development topics . Make it educational, include a clear insight or takeaway, and ensure it's different from anything already trending on my timeline. Include 3 relevant hashtags."
    "Avoid technical jargon and make use of simple english"
)

response = model.generate_content(prompt)
post_text = response.text.strip()

# Set up LinkedIn API
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN_ERROR")
linkedin_urn = os.getenv("LINKEDIN_URN")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "X-Restli-Protocol-Version": "2.0.0"
}

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

response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=data)
print("Status:", response.status_code)
if response.status_code >= 400:
    print("Error:", response.json())
