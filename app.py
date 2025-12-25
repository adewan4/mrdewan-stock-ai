import streamlit as st

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Indian Stock AI Dashboard",
    layout="wide"
)

# ---------------------------
# GLOBAL STYLES (Mobile Friendly)
# ---------------------------
st.markdown(
    """
    <style>
        body {
            font-size: 16px;
        }
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# HEADER
# ---------------------------
st.title("📊 Indian Stock AI Dashboard")
st.caption("Developed by Akash Dewan")

# ---------------------------
# NAVIGATION TABS
# ---------------------------
tabs = st.tabs([
    "Home",
    "How AI Works",
    "Stock Analysis",
    "Financials",
    "AI Screener"
])

# ---------------------------
# HOME TAB
# ---------------------------
with tabs[0]:
    st.subheader("Welcome 👋")
    st.write(
        """
        This app analyzes Indian stocks using a rule-based AI engine.
        
        ✔ Fundamental analysis  
        ✔ Risk & growth scoring  
        ✔ Valuation & momentum checks  
        
        Use the tabs above to explore.
        """
    )

# ---------------------------
# HOW AI WORKS TAB
# ---------------------------
with tabs[1]:
    st.subheader("🧠 How the AI Works")

    st.write(
        """
        The AI evaluates stocks using *5 key pillars*:
        
        ⿡ Intrinsic Value  
        ⿢ Growth  
        ⿣ Risk  
        ⿤ Valuation  
        ⿥ Momentum  

        Each pillar is scored from *0 to 10*.
        The final recommendation is an average of these scores.
        """
    )

    st.markdown(
        """
        *Final Recommendation Logic*
        - 8 – 10 → *STRONG BUY*
        - 6 – 7.9 → *BUY*
        - 4 – 5.9 → *HOLD*
        - Below 4 → *SELL*
        """
    )

# ---------------------------
# STOCK ANALYSIS TAB
# ---------------------------
with tabs[2]:
    st.subheader("📈 Stock Analysis")
    st.warning(
        "⚠ This analysis is for educational purposes only. "
        "Always do your own research before investing."
    )

    st.write("Stock analysis engine will be added next.")

# ---------------------------
# FINANCIALS TAB
# ---------------------------
with tabs[3]:
    st.subheader("📑 Financials")
    st.write("Company financial statements and trends will appear here.")

# ---------------------------
# AI SCREENER TAB
# ---------------------------
with tabs[4]:
    st.subheader("🤖 AI Screener")
    st.write(
        """
        This screener will scan *the entire NSE stock universe*
        and return the *top 50 BUY / STRONG BUY stocks* daily.
        """
    )

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© Developed by Akash Dewan")

