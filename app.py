import streamlit as st
import requests
import re

# --- UI SETUP ---
st.set_page_config(page_title="India Security & Riot Analyzer", layout="wide")
st.title("🛡️ Indian Internal Security & Non-Lethal Use Case Tool")

# --- USER INPUTS ---
api_key = st.sidebar.text_input("Serper API Key", type="password", help="Get one for free at serper.dev")
st.sidebar.markdown("---")

# Source Selection
source_groups = {
    "News Agencies": "site:ptinews.com OR site:aninews.in OR site:uniindia.com",
    "Top News Outlets": "site:indianexpress.com OR site:ndtv.com OR site:news18.com OR site:theprint.in",
    "Government/Law": "site:nia.gov.in OR site:mha.gov.in OR site:bprd.nic.in OR site:pib.gov.in",
    "Gazettes/Official": "site:egazette.gov.in OR site:ips.gov.in"
}

selected_groups = st.sidebar.multiselect("Select Information Nodes", list(source_groups.keys()), default=["News Agencies", "Top News Outlets"])
date_range = st.sidebar.slider("Timeline", 2019, 2026, (2019, 2026))

# --- CORE ENGINE ---
def run_strategic_search(query, key, sources):
    if not sources: return []
    
    # Building the site filter
    site_query = " OR ".join([source_groups[s] for s in sources])
    full_query = f"{query} ({site_query}) after:{date_range[0]}-01-01 before:{date_range[1]}-12-31"
    
    url = "https://google.serper.dev/search"
    payload = {"q": full_query, "gl": "in"} 
    headers = {'X-API-KEY': key, 'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json().get('organic', [])
    except:
        return []

def pattern_match(text):
    # Regex to find police count and restraint terms
    deployment = re.findall(r'(\d+,?\d*)\s(?:cops|personnel|police|jawans)', text, re.I)
    restraint = [w for w in ["restrained", "cordon", "tear gas", "water cannon", "pellets", "lathi", "drone", "non-lethal"] if w in text.lower()]
    return deployment[0] if deployment else "Unknown", restraint

# --- MAIN APP ---
search_term = st.text_input("Search Case Studies (e.g. 'Protest dispersal Delhi' or 'CASO Jammu Kashmir')", "Police riot control India")

if st.button("Generate Case Studies"):
    if not api_key:
        st.warning("Please enter an API key in the sidebar.")
    else:
        results = run_strategic_search(search_term, api_key, selected_groups)
        
        if results:
            for item in results:
                dep_count, tech_used = pattern_match(item.get('snippet', ''))
                
                with st.expander(f"📌 {item['title']}"):
                    st.write(f"**Source:** {item.get('link')}")
                    st.write(f"**Context:** {item.get('snippet')}")
                    
                    # Pattern dashboard
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Forces on Ground", dep_count)
                    c2.write("**Methods Detected:**")
                    c2.write(", ".join(tech_used) if tech_used else "No specific tool mentioned")
                    
                    # Automated Analysis for your product
                    if "tear gas" in tech_used or "lathi" in tech_used:
                        st.info("💡 **Product Opportunity:** High-injury method detected. Use this as a case study for your safer non-lethal alternative.")
        else:
            st.error("No data found for this specific query. Try reducing the number of filters.")
