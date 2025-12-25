import streamlit as st
from ai_engine import fetch_basic_info, calculate_scores_from_info


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

    ticker = st.text_input(
      "Enter NSE stock ticker (example: TCS.NS, RELIANCE.NS):"
    )
    
    if ticker:
        with st.spinner("Analyzing stock with AI engine..."):
            stock, info = fetch_basic_info(ticker)
        if not info:
            st.error("Unable to fetch data for this stock. Please try later.")
        else:
            scores = calculate_scores_from_info(info)
            
            st.metric(
                label="Current Price",
                value=f"₹ {scores['price']}"
            )

            st.markdown("### 🧠 AI Score Breakdown")

            col1, col2, col3 = st.columns(3)

            col1.metric("Intrinsic", round(scores["intrinsic"], 2))
            col1.metric("Growth", round(scores["growth"], 2))

            col2.metric("Risk", round(scores["risk"], 2))
            col2.metric("Valuation", round(scores["valuation"], 2))

            col3.metric("Momentum", round(scores["momentum"], 2))
            col3.metric("Final Score", scores["final_score"])

            st.markdown("---")

            reco = scores["recommendation"]

            if reco == "STRONG BUY":
                st.success(f"📈 Final Recommendation: *{reco}*")
            elif reco == "BUY":
                st.info(f"✅ Final Recommendation: *{reco}*")
            elif reco == "HOLD":
                st.warning(f"⏸ Final Recommendation: *{reco}*")
            else:
                st.error(f"⚠ Final Recommendation: *{reco}*")


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

