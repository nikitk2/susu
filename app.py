import streamlit as st
import pandas as pd
from datetime import datetime
import re

# --- UI SETUP ---
st.set_page_config(page_title="India Incident & Riot Analyzer", layout="wide")
st.title("🇮🇳 India Incident & Pattern Recognition Tool")
st.markdown("""
Summarize news, government releases, and media from **2019 to 2026**. 
Identify use cases for non-lethal riot control and police deployment patterns.
""")

# --- SIDEBAR OPTIONS ---
st.sidebar.header("Filter Settings")
source_type = st.sidebar.multiselect(
    "Select Sources", 
    ["Times of India", "The Hindu", "PIB (Govt)", "Social Media/Videos"],
    default=["Times of India", "PIB (Govt)"]
)

category = st.sidebar.radio(
    "Analysis Focus",
    ["Civil Unrest / Riots", "Terrorism / High-Stake Restraint", "General Policing"]
)

year_range = st.sidebar.slider("Select Year Range", 2019, 2026, (2019, 2026))

# --- MOCK DATA ENGINE (Simulating Scraper Results) ---
# In a real app, this function would call the news APIs/Scrapers
def fetch_and_analyze(query, years):
    # Simulated data reflecting your 2019-2026 landscape
    results = [
        {
            "date": "2026-02-15",
            "source": "PIB (Govt)",
            "title": "New 'PRAHAAR' Deployment Guidelines for Urban Unrest",
            "content": "Ministry of Home Affairs deployed 5,000 personnel. Used water cannons and new non-lethal barriers at a 200m perimeter.",
            "category": "Civil Unrest / Riots"
        },
        {
            "date": "2025-11-10",
            "source": "The Hindu",
            "title": "Restraint Tactics in Cordon and Search Operations",
            "content": "Security forces used flashbangs and tactical restraint to capture 2 suspects alive during a 12-hour standoff.",
            "category": "Terrorism / High-Stake Restraint"
        }
    ]
    return [r for r in results if r["category"] == category]

# --- PATTERN RECOGNITION ENGINE ---
def extract_patterns(text):
    patterns = {
        "Manpower": re.findall(r'(\d+,?\d*)\s(?:personnel|police|forces)', text),
        "Non-Lethal Used": [w for w in ["water cannon", "tear gas", "flashbang", "lathi"] if w in text.lower()],
        "Perimeter": re.findall(r'(\d+m|\d+\s?meter)', text)
    }
    return patterns

# --- MAIN INTERFACE ---
query = st.text_input("Enter Keywords (e.g., 'Delhi riots', 'Police deployment', 'Crowd control')", "Police deployment")

if st.button("Run Analysis"):
    st.subheader(f"Results for: {query} ({year_range[0]}-{year_range[1]})")
    
    data = fetch_and_analyze(query, year_range)
    
    if data:
        for item in data:
            with st.expander(f"{item['date']} | {item['title']} ({item['source']})"):
                st.write(item['content'])
                
                # Show Pattern Recognition
                patterns = extract_patterns(item['content'])
                col1, col2, col3 = st.columns(3)
                col1.metric("Forces Deployed", patterns["Manpower"][0] if patterns["Manpower"] else "N/A")
                col2.metric("Perimeter Size", patterns["Perimeter"][0] if patterns["Perimeter"] else "N/A")
                col3.write(f"**Tools Detected:** {', '.join(patterns['Non-Lethal Used'])}")
                
                # Use Case Generation
                st.info(f"**Potential Use Case for Your Product:** {item['category']} scenario requiring {patterns['Perimeter'][0] if patterns['Perimeter'] else 'rapid'} containment.")
    else:
        st.warning("No specific incidents found for these filters. Try adjusting the keywords.")

# --- DATA EXPORT ---
st.sidebar.markdown("---")
if st.sidebar.button("Export to Case Study (CSV)"):
    st.sidebar.success("Case study generated! (Simulated)")