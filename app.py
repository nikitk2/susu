import streamlit as st
import requests
import re

# --- STYLING & UI ---
st.set_page_config(page_title="India Riot Intelligence 2026", layout="wide")
st.title("🛰️ India Internal Security Intelligence Engine (2019-2026)")
st.sidebar.info("Focus: Pattern Recognition for Non-Lethal Deployment")

# --- USER CONFIG ---
api_key = st.sidebar.text_input("Enter Serper API Key", type="password")
year_range = st.sidebar.slider("Timeline", 2019, 2026, (2019, 2026))

# --- INTELLIGENCE LOGIC ---
def deep_intelligence_search(query, key):
    # We use 'site:' filters to create a "Truth vs. Report" view
    sites = {
        "Official": "site:pib.gov.in OR site:mha.gov.in OR site:bprd.nic.in",
        "Field Reporting": "site:indianexpress.com OR site:thehindu.com OR site:theprint.in OR site:ndtv.com",
        "Global/UN": "site:ohchr.org OR site:hrw.org"
    }
    
    intel_results = {}
    for label, site_query in sites.items():
        full_q = f"{query} ({site_query}) after:{year_range[0]}-01-01 before:{year_range[1]}-12-31"
        url = "https://google.serper.dev/search"
        payload = {"q": full_q, "gl": "in"}
        headers = {'X-API-KEY': key, 'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload).json()
        intel_results[label] = response.get('organic', [])
    return intel_results

def extract_intel_patterns(text):
    # Tech/Forces detection
    tech = [t for t in ["water cannon", "tear gas", "drone", "AI glasses", "facial recognition", "pellet", "lathi", "Section 144", "CASO", "smart glasses"] if t in text.lower()]
    # Violence triggers
    triggers = [tr for tr in ["stone pelting", "clash", "breached", "provocation", "vandalism", "mob"] if tr in text.lower()]
    
    return {"tech": tech, "triggers": triggers}

# --- MAIN DASHBOARD ---
user_query = st.text_input("Enter Incident or Location (e.g., 'Jammu Kashmir CASO' or 'Delhi Protests')", "Riot control India")

if st.button("Generate Case Study"):
    if not api_key: st.error("Key required.")
    else:
        with st.spinner("Analyzing cross-referenced sources..."):
            data = deep_intelligence_search(user_query, api_key)
            
            # --- Visualizing the 2nd Layer: Pattern Recognition ---
            st.subheader("📊 Tactical Analysis")
            all_snippets = " ".join([r.get('snippet', '') for r in data["Official"] + data["Field Reporting"]])
            patterns = extract_intel_patterns(all_snippets)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**⚠️ Common Violence Triggers Found:**")
                for t in set(patterns["triggers"]): st.warning(f"Trigger: {t}")
            with col2:
                st.write("**🛡️ Forces/Tech Currently Deployed:**")
                for tech in set(patterns["tech"]): st.success(f"Deployed: {tech}")

            st.divider()

            # --- Bilateral View (Both Sides) ---
            st.subheader("⚖️ Narrative Gap: Official vs. Public Perception")
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("#### [Government View]")
                for item in data["Official"][:3]:
                    st.caption(f"**{item['title']}**")
                    st.write(item.get('snippet', ''))
            
            with c2:
                st.markdown("#### [Field/Civil View]")
                for item in data["Field Reporting"][:3]:
                    st.caption(f"**{item['title']}**")
                    st.write(item.get('snippet', ''))
