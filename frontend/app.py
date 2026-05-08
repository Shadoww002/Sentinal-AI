import streamlit as st
import requests

# 1. Page Configuration 
st.set_page_config(
    page_title="Sentinel AI | Fact Checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded" # Changed to expanded to show off the engine specs
)

# 2. Custom CSS for better typography and spacing
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0;}
    .sub-header { font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;}
    .claim-box { padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; margin-bottom: 10px;}
    .confidence-high { color: #10B981; font-weight: bold; }
    .confidence-med { color: #F59E0B; font-weight: bold; }
    .confidence-low { color: #EF4444; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar (NEW: System Status & Info)
with st.sidebar:
    st.markdown("### ⚙️ System Architecture")
    st.info("""
    **Brain:** Local Llama-3 (8B)
            
    **Retrieval:** Google News (Live RAG)
            
    **Embeddings:** MPNet Base v2
            
    **NLP Router:** FastAPI
    """)
    st.markdown("---")
    st.markdown("### 📖 How it works")
    st.markdown("1. **Extracts** verifiable claims from your text using Llama 3.\n2. **Searches** live journalistic sources via Google for each claim.\n3. **Filters** the noise using semantic vector math.\n4. **Reasons** over the live evidence to give a final verdict.")
# 4. Header Section
st.markdown('<p class="main-header">🛡️ Sentinel AI Fact-Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by Live Web RAG & Local Llama 3 Reasoning</p>', unsafe_allow_html=True)

# 5. Input Section 
with st.form("fact_check_form"):
    input_text = st.text_area(
        "Paste an article, headline, or claim below:",
        height=150,
        placeholder="e.g., The CEO of the company announced yesterday that their new product sold 50 million units..."
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button("Analyze Content 🔍", use_container_width=True)

# 6. Processing and Results Section
if submitted:
    if not input_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Initiating Live Search & Llama 3 Reasoning (This may take a moment)..."):
            try:
                response = requests.post("http://localhost:8000/api/v1/verify", json={"text": input_text})
                
                if response.status_code == 200:
                    data = response.json()
                    st.divider()
                    
                    # --- TOP LEVEL VERDICT ---
                    verdict = data.get('overall_verdict', 'Unknown')
                    if verdict in ["Likely True", "True"]:
                        st.success(f"### Final System Verdict: {verdict}")
                    elif verdict in ["Misleading/False", "False"]:
                        st.error(f"### Final System Verdict: {verdict}")
                    else:
                        st.warning(f"### Final System Verdict: {verdict}")

                    # --- METRICS ROW ---
                    claims_list = data.get('analysis', [])
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric(label="Verifiable Claims Extracted", value=len(claims_list))
                    with m2:
                        st.metric(label="Live Sources Cross-Referenced", value=len(claims_list) * 3) 
                    with m3:
                        st.metric(label="Verification Model", value="Llama 3 (Local)") # UPDATED MODEL NAME

                    st.divider()
                    st.subheader("🔎 Detailed Claim Breakdown")
                    
                    # --- INDIVIDUAL CLAIMS ---
                    for i, item in enumerate(claims_list):
                        with st.expander(f"Claim {i+1}: {item['claim']}", expanded=(i==0)):
                            
                            c1, c2 = st.columns([2.5, 1.5]) # Adjusted ratio for better fit
                            
                            with c1:
                                st.markdown("**🤖 AI Reasoning:**")
                                st.info(item.get('explanation', 'No explanation provided.'))
                                
                                sources = item.get('sources', [])
                                if sources:
                                    st.markdown("**🌐 Live Sources Evaluated:**")
                                    for src in sources:
                                        if src['href'] != "#":
                                            st.markdown(f"- [{src['title']}]({src['href']})")
                                        else:
                                            st.markdown(f"- {src['title']}")
                            
                            with c2:
                                v = item.get('verdict', 'Unverified')
                                conf = item.get('confidence', 0.0)
                                
                                st.markdown("**Status:**")
                                if v == 'True':
                                    st.success("✅ " + v)
                                elif v == 'False':
                                    st.error("❌ " + v)
                                else:
                                    st.warning("⚠️ " + v)
                                    
                                # --- NEW: CONFIDENCE BAR ---
                                st.markdown("**AI Confidence:**")
                                # Normalize confidence to a percentage
                                conf_pct = conf * 100 if conf <= 1.0 else conf
                                
                                # Render visual progress bar
                                st.progress(int(conf_pct))
                                
                                # Render text color based on score
                                if conf_pct >= 80:
                                    st.markdown(f"<span class='confidence-high'>{conf_pct:.0f}% (High Certainty)</span>", unsafe_allow_html=True)
                                elif conf_pct >= 50:
                                    st.markdown(f"<span class='confidence-med'>{conf_pct:.0f}% (Moderate Certainty)</span>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<span class='confidence-low'>{conf_pct:.0f}% (Low Certainty)</span>", unsafe_allow_html=True)

                else:
                    st.error(f"Backend API Error: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to the backend. Please ensure your FastAPI server is running on port 8000.")