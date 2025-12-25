import streamlit as st
import pandas as pd
import time
from ai_engine import fetch_basic_info, calculate_scores_from_info

# -------------------------------------------------
# PAGE CONFIG + MOBILE FRIENDLY
# -------------------------------------------------
st.set_page_config(
    page_title="Indian Stock AI Dashboard",
    layout="wide"
)

st.markdown("""
<style>
@media (max-width: 600px) {
    .block-container {
        padding: 1rem !important;
    }
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<hr>
<p style="text-align:center;font-size:13px;color:gray;">
Developed by <b>Akash Dewan</b> | Educational purpose only
</p>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TABS
# -------------------------------------------------
tabs = st.tabs([
    "Home",
    "How AI Works",
    "Compare Stocks",
    "Financials",
    "AI Screener",
    "Stock Analysis"
])

# -------------------------------------------------
# HOME
# -------------------------------------------------
with tabs[0]:
    st.title("📊 Indian Stock AI Dashboard")
    st.write(
        "Analyze Indian stocks using a transparent, rule-based AI engine. "
        "This app helps you understand *valuation, growth, risk, and momentum*."
    )

    ticker = st.text_input("Quick stock lookup (e.g. TCS.NS)")
    if ticker:
        stock, info = fetch_basic_info(ticker)
        if info:
            scores = calculate_scores_from_info(info)
            st.metric("Current Price", scores["price"])
            st.success(f"Recommendation: {scores['recommendation']}")
        else:
            st.error("Data temporarily unavailable.")

# -------------------------------------------------
# HOW AI WORKS
# -------------------------------------------------
with tabs[1]:
    st.title("🧠 How the AI Works")

    st.markdown("""
This AI *does NOT predict prices*.  
It *scores stocks objectively* using 5 pillars:

### ⿡ Intrinsic Value
Is the stock undervalued compared to earnings & book value?

### ⿢ Growth
ROE, ROCE, revenue growth, profit margins.

### ⿣ Risk
Debt-to-equity — lower debt = higher score.

### ⿤ Valuation
Compares stock PE with industry-adjusted PE.

### ⿥ Momentum
Position of price between 52-week high & low.

### 🎯 Final Score
Average of all 5 → recommendation:
- *8+* → STRONG BUY
- *6–7.9* → BUY
- *4–5.9* → HOLD
- *<4* → SELL

⚠ Educational use only. Always do your own research.
""")

# -------------------------------------------------
# COMPARE STOCKS
# -------------------------------------------------
with tabs[2]:
    st.title("📊 Compare Stocks")

    tickers_input = st.text_input(
        "Enter NSE tickers (comma separated)",
        placeholder="TCS.NS, RELIANCE.NS, INFY.NS"
    )

    if tickers_input:
        tickers = [t.strip() for t in tickers_input.split(",")]
        rows = []

        for t in tickers:
            stock, info = fetch_basic_info(t)
            if info:
                scores = calculate_scores_from_info(info)
                rows.append({
                    "Ticker": t,
                    "Price": scores["price"],
                    "Final Score": scores["final_score"],
                    "Recommendation": scores["recommendation"]
                })

        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)

# -------------------------------------------------
# FINANCIALS (LIGHT VERSION)
# -------------------------------------------------
with tabs[3]:
    st.title("📑 Financials")

    ticker = st.text_input("Enter ticker for financials")
    if ticker:
        stock, info = fetch_basic_info(ticker)
        if info:
            st.write("Market Cap:", info.get("marketCap"))
            st.write("PE Ratio:", info.get("trailingPE"))
            st.write("Dividend Yield:", info.get("dividendYield"))
        else:
            st.error("Unable to fetch financial data.")

# -------------------------------------------------
# AI SCREENER
# -------------------------------------------------
with tabs[4]:
    st.title("🤖 AI Screener (Top 50)")

    if st.button("Run Full NSE Scan"):
        df = pd.read_csv("nse_list.csv")
        df.rename(columns={df.columns[0]: "Symbol"}, inplace=True)
        tickers = df["Symbol"].dropna().unique().tolist()

        results = []
        progress = st.progress(0)

        for i, t in enumerate(tickers):
            stock, info = fetch_basic_info(t)
            if info:
                scores = calculate_scores_from_info(info)
                if scores["recommendation"] in ("BUY", "STRONG BUY"):
                    results.append({
                        "Ticker": t,
                        "Score": scores["final_score"],
                        "Recommendation": scores["recommendation"]
                    })
            progress.progress((i + 1) / len(tickers))
            time.sleep(0.2)

        if results:
            out = pd.DataFrame(results).sort_values("Score", ascending=False).head(50)
            st.dataframe(out, use_container_width=True)
        else:
            st.warning("No strong opportunities today.")

# -------------------------------------------------
# STOCK ANALYSIS
# -------------------------------------------------
with tabs[5]:
    st.title("📈 Stock Analysis")
    st.warning("Educational purpose only.")

    ticker = st.text_input("Enter NSE ticker")
    if ticker:
        stock, info = fetch_basic_info(ticker)
        if info:
            scores = calculate_scores_from_info(info)
            st.metric("Price", scores["price"])
            st.write(scores)


