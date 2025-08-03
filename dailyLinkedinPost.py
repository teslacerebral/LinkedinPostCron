import os
import requests
import google.generativeai as genai

# Set up Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = (
    "Write a short LinkedIn post (under 180 words) about a trending tech topic. "
    "Use storytelling, psychology and human tone. Avoid technical jargon and make use of easy english and something beautiful and new also sometime discuss ever green topics on Java and SQL and NOSQL but sometime"
)

response = model.generate_content(prompt)
post_text = response.text.strip()

# Set up LinkedIn API
access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
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
