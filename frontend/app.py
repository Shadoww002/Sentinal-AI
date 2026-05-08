import streamlit as st
import requests

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Sentinel AI | Fact Checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS for better typography and spacing
st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0;}
    .sub-header { font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;}
    .claim-box { padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<p class="main-header">🛡️ Sentinel AI Fact-Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by Retrieval-Augmented Generation & NLI Verification</p>', unsafe_allow_html=True)

# 4. Input Section using a Form (Allows users to press 'Enter' or click the button)
with st.form("fact_check_form"):
    input_text = st.text_area(
        "Paste an article, headline, or claim below:",
        height=150,
        placeholder="e.g., The CEO of the company announced yesterday that their new product sold 50 million units..."
    )
    
    # We put the button in a column to make it look cleaner
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button("Analyze Content 🔍", use_container_width=True)

# 5. Processing and Results Section
if submitted:
    if not input_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Initiating RAG Pipeline & DeBERTa Verification..."):
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
                        st.metric(label="Live Sources Cross-Referenced", value=len(claims_list) * 3) # Assuming top_k=3
                    with m3:
                        st.metric(label="Verification Model", value="DeBERTa-v3")

                    st.divider()
                    st.subheader("🔎 Detailed Claim Breakdown")
                    
                    # --- INDIVIDUAL CLAIMS ---
                    for i, item in enumerate(claims_list):
                        # Use an expander for each claim, keep the first one open by default
                        with st.expander(f"Claim {i+1}: {item['claim']}", expanded=(i==0)):
                            
                            # Split the inside of the expander into two columns
                            c1, c2 = st.columns([3, 1])
                            
                            with c1:
                                st.markdown("**🤖 AI Reasoning:**")
                                st.info(item.get('explanation', 'No explanation provided.'))
                                
                                # --- NEW: SHOW SOURCES ---
                                sources = item.get('sources', [])
                                if sources:
                                    st.markdown("**🌐 Live Sources Evaluated:**")
                                    for src in sources:
                                        if src['href'] != "#":
                                            # Renders a clickable markdown link: [Title](URL)
                                            st.markdown(f"- [{src['title']}]({src['href']})")
                                        else:
                                            st.markdown(f"- {src['title']}")
                                
                            with c2:
                                v = item.get('verdict', 'Unverified')
                                st.markdown("**Status:**")
                                if v == 'True':
                                    st.success("✅ " + v)
                                elif v == 'False':
                                    st.error("❌ " + v)
                                else:
                                    st.warning("⚠️ " + v)

                else:
                    st.error(f"Backend API Error: {response.status_code}")
                    st.code(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Failed to connect to the backend. Please ensure your FastAPI server is running on port 8000.")