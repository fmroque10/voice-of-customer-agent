from mcp_tools import (
    mcp_severity_tool,
    mcp_trend_tool,
    mcp_count_tool,
    mcp_complaint_tool
)


import streamlit as st
import pandas as pd
from collections import Counter
from google import genai

# ------------------------
# Gemini Client
# ------------------------

client = genai.Client(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# ------------------------
# Tools
# ------------------------

def get_complaints(df):
    return "\n".join(df["complaint"].tolist())


def count_complaints(df):
    return len(df)


def top_words(df):

    words = []

    for complaint in df["complaint"]:
        words.extend(complaint.lower().split())

    return Counter(words).most_common(10)


def severity_tool(df):

    severe_keywords = [
        "failure",
        "overheating",
        "stalls",
        "slipping"
    ]

    severe_count = 0

    for complaint in df["complaint"]:

        text = complaint.lower()

        for word in severe_keywords:

            if word in text:
                severe_count += 1
                break

    return {
        "high_severity_complaints": severe_count,
        "total_complaints": len(df)
    }


def trend_tool(df):

    categories = {
        "Transmission": 0,
        "Brake": 0,
        "Engine": 0
    }

    for complaint in df["complaint"]:

        text = complaint.lower()

        if "transmission" in text:
            categories["Transmission"] += 1

        if "brake" in text:
            categories["Brake"] += 1

        if "engine" in text:
            categories["Engine"] += 1

    return categories


# ------------------------
# Agent
# ------------------------

def customer_agent(goal, df):

    complaints = mcp_complaint_tool(
    df,
    get_complaints
)

    total = mcp_count_tool(
    df,
    count_complaints
)

    common_words = top_words(df)

    severity = mcp_severity_tool(
    df,
    severity_tool
)

    trends = mcp_trend_tool(
    df,
    trend_tool
)

st.write("🔌 MCP Tool: Complaint Retrieval")
st.write("🔌 MCP Tool: Complaint Statistics")
st.write("🔌 MCP Tool: Severity Analysis")
st.write("🔌 MCP Tool: Trend Analysis")
    

    prompt = f"""
You are an autonomous Customer Intelligence Agent.

Your job is to gather context from tools
and execute a business analysis.

TOOL OUTPUTS

TOTAL_COMPLAINTS:
{total}

COMMON_WORDS:
{common_words}

SEVERITY_TOOL:
{severity}

TREND_TOOL:
{trends}

COMPLAINTS:
{complaints}

BUSINESS GOAL:
{goal}

Generate:

1. Executive Summary
2. Major Trends
3. Severity Assessment
4. Business Risks
5. Recommended Actions
6. Priority Actions for Leadership
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ------------------------
# Streamlit UI
# ------------------------

st.title("Voice of Customer Agent")

st.write(
    "Upload a CSV containing a column named 'complaint'."
)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")

    st.dataframe(df)

    if st.button("Analyze Complaints"):

        with st.spinner("Agent is analyzing complaints..."):

            result = customer_agent(
                """
Analyze customer complaints and provide
executive recommendations.
""",
                df
            )

        st.subheader("Agent Report")

        st.write(result)
