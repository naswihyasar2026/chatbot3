# GEMINI KNOWLEDGE-BASED CHATBOT (Streamlit version)
import os

import streamlit as st
from google import genai
from google.genai import types

MODEL_NAME = "gemini-3.5-flash-lite"

# Knowledge / Manual
MANUAL = """
Digital Marketing – Knowledge Base
1. What is Digital Marketing?
Digital Marketing is the process of promoting products, services, or brands through the internet and digital technologies. It helps businesses reach potential customers, increase brand awareness, generate leads, and boost sales.

Example: Promoting a clothing brand through Instagram advertisements, Google Ads, websites, and email campaigns.
2. Main Types of Digital Marketing
1. Search Engine Optimization (SEO): Improving a website's visibility on search engines like Google to get free organic traffic.
2. Search Engine Marketing (SEM): Promoting websites through paid search advertisements.
3. Social Media Marketing (SMM): Promoting brands through platforms like Instagram, Facebook, LinkedIn, and YouTube.
4. Content Marketing: Creating valuable content, such as blogs, videos, articles, and infographics, to attract customers.
5. Email Marketing: Sending promotional emails, newsletters, offers, and updates to customers.
6. Affiliate Marketing: Promoting another company's products and earning a commission for successful sales.
7. Influencer Marketing: Collaborating with social media influencers to promote products or services.
8. Pay-Per-Click Advertising (PPC): Paying for advertisements whenever someone clicks on them.
9. Mobile Marketing: Reaching customers through mobile applications, SMS, and mobile advertisements.
10. Video Marketing: Using videos to promote products, explain services, and engage audiences.
3. Importance of Digital Marketing
- Reaches a global audience.
- Costs less than many traditional marketing methods.
- Helps target specific customer groups.
- Increases brand awareness.
- Generates leads and sales.
- Provides measurable marketing results.
- Improves customer engagement.
- Helps businesses understand customer behaviour.
4. Major Digital Marketing Platforms
- Google: SEO, Google Ads, and search marketing.
- Instagram: Reels, stories, influencer marketing, and advertisements.
- Facebook: Business pages, targeted advertisements, and community building.
- YouTube: Video advertisements and educational content.
- LinkedIn: Professional networking and B2B marketing.
- WhatsApp: Customer communication and promotional messages.
- Pinterest: Visual content discovery and product promotion.
5. Important Digital Marketing Terms
Term	Meaning
SEO	Improving organic search visibility
SEM	Marketing through search engines
CTR	Percentage of people who click an advertisement
CPC	Cost per click
CPM	Cost per 1,000 ad impressions
ROI	Return on investment
Conversion	Desired customer action
Lead	Potential customer
Engagement	Likes, comments, shares, and interactions
Reach	Number of unique people who see content
Impressions	Total number of times content is displayed
Bounce Rate	Percentage of visitors who leave without further interaction
Keyword	Search term used by people
Landing Page	Webpage designed for a specific marketing goal

6. Digital Marketing Strategies
1. Identify the target audience.
2. Understand customer needs and behaviour.
3. Set clear marketing objectives.
4. Choose suitable digital platforms.
5. Create attractive and valuable content.
6. Use SEO and paid advertising.
7. Monitor campaign performance.
8. Analyse results and improve strategies.
7. Digital Marketing Tools
- Google Analytics: Tracks website traffic and user behaviour.
- Google Ads: Creates and manages paid advertisements.
- Google Search Console: Monitors website search performance.
- Canva: Designs marketing graphics and social media posts.
- Mailchimp: Manages email marketing campaigns.
- SEMrush: Supports SEO and keyword research.
- HubSpot: Provides CRM, marketing automation, and lead management.
- Meta Ads Manager: Manages Facebook and Instagram advertisements.
8. Traditional Marketing vs Digital Marketing
Traditional Marketing	Digital Marketing
Newspapers and television	Websites and social media
Limited audience targeting	Specific audience targeting
Difficult to measure results	Easy performance tracking
Often expensive	Flexible budgets
Mostly one-way communication	Interactive communication

9. Advantages and Disadvantages
Advantages:
- Global reach.
- Cost-effective promotion.
- Real-time performance tracking.
- Better audience targeting.
- Direct customer interaction.
Disadvantages:
- High online competition.
- Privacy and security concerns.
- Requires technical knowledge.
- Negative reviews can affect brand reputation.
- Digital platforms frequently change their algorithms.
10. Future of Digital Marketing
The future of digital marketing includes Artificial Intelligence (AI), machine learning, voice search, chatbots, personalized advertisements, influencer marketing, marketing automation, and data-driven decision-making.

AI helps businesses analyse customer behaviour, generate marketing content, personalize recommendations, and automate customer support.
11. Example of a Digital Marketing Campaign
Example: A new clothing brand launching on Instagram.
- Objective: Increase brand awareness and sales.
- Target audience: Young adults aged 18–30.
- Platform: Instagram and Facebook.
- Strategy: Reels, influencer collaborations, and paid advertisements.
- Budget: Set a fixed advertising budget.
- Measurement: Track reach, engagement, website visits, and sales.
- Expected result: More brand visibility, potential customers, and purchases.
12. Main Objective of Digital Marketing
The main objective of digital marketing is to attract potential customers, convert them into buyers, build customer relationships, increase brand awareness, and achieve business growth.
"""

SYSTEM_INSTRUCTION = """
Answer only from the given manual.
If the answer is not available in the manual, say: Information not available.
Give simple and clear answers.
"""


def get_api_key():
    """Read the API key from Streamlit secrets or an environment variable."""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")


@st.cache_resource
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


# ---------- Page setup ----------
st.set_page_config(page_title="Digital Marketing Chatbot", page_icon="📣")
st.title("📣 Digital Marketing Chatbot")
st.caption("Ask questions answered from the Digital Marketing knowledge base.")

api_key = get_api_key()
if not api_key:
    st.error(
        "Gemini API key not found. Add `GEMINI_API_KEY` to "
        "`.streamlit/secrets.toml` or set it as an environment variable."
    )
    st.stop()

client = get_client(api_key)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()
    with st.expander("View knowledge base"):
        st.text(MANUAL)

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Chat input ----------
question = st.chat_input("Ask your question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=MANUAL + "\n\nQuestion: " + question,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION
                    ),
                )
                answer = response.text or "Information not available."
            except Exception as e:
                answer = f"⚠️ Error: {e}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
