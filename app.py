import streamlit as st
import pandas as pd
import os
from ai_engine import fetch_basic_info, calculate_scores_from_info,get_news_balance_cashflow_financials

# Mobile Friendly Styling
st.set_page_config(
page_title="Indian Stock Dashboard",
layout="wide",
initial_sidebar_state="expanded"
)
st.markdown(
"""
<style>
/* Reduce width and center content on mobile */
@media (max-width: 600px) {
.block-container {
padding: 1rem !important;
max-width: 100% !important;
}
}

/* Increase readability on mobile */
body {
font-size: 18px !important;
}
/* Better input box look */
.stTextInput>div>div>input {
font-size: 18px !important;
border-radius: 8px;
padding: 10px;

}
/* Buttons more touch-friendly */
.stButton>button {
width: 100%;
padding: 12px;
border-radius: 10px;
font-size: 18px;

}

/* Sidebar text scaling */
@media (max-width: 600px) {
.css-1lcbmhc {
font-size: 20px !important;
}
}

</style>
""",
unsafe_allow_html= True
)

# FOOTER (Visible on every page)

st.markdown(
"""
<hr>
<p style='text-align: center; font-size: 14px; color: gray;'>
Developed by <strong>Akash Dewan</strong>
</p>
""",
unsafe_allow_html= True
)
# PAGE + MOBILE LAYOUT

st.set_page_config(page_title="Indian Stock Dashboard", layout="centered")
st.markdown(
"""
<style>
.block-container {
padding-top: 1rem;
max_width: 480px;
margin: auto;
}
<style>
""",
unsafe_allow_html=True
)

# Horizontal Navigation (Tabs)

tabs = st.tabs([
"Home",
"How AI Works",
"Compare Stocks",
"Financials",
"AI Screener",
"Stock Analysis"
])


# HOME PAGE

with tabs[0]:
    st.title("📊 Indian Stock Dashboard")
    st.write(
       "This app analyzes Indian stocks using a custom AI logic based on "
       "financial performance, growth trends, and risk factors."
    )
    
    st.markdown("### 🔍 Quick Stock Lookup")
    quick = st.text_input("Enter NSE ticker (e.g., TCS.NS):")
    
    if quick:
        data = fetch_basic_info(quick)
        if not data:
            st.error("Data temporarily unavailable.")
        else:
            st.metric("Current Price", data["price"])

# HOW AI Works

with tabs[1]:
    st.title("🧠 How the AI Gives Recommendations")
    st.write("""
    This page explains the logic behind the AI engine created by *Mr. Dewan*.
    The AI uses five key financial pillars to analyze any stock and generate a
    final recommendation such as *STRONG BUY, **BUY, **HOLD, or **SELL*.
""")

st.markdown("---")
st.subheader("📌 1. Intrinsic Value Score")
st.write("""
This measures whether a stock is *underpriced or overpriced* compared to its
intrinsic value.

*Formula used:*
(Book Value + (EPS × 15)) ÷ (2 × Current Price) → scaled from 0–10.
- High score → Stock is undervalued
- Low score → Stock may be overvalued
""")
st.subheader("📌 2. Growth Score")
st.write("""
Growth score measures how strong the company's performance is.
*Values considered:*
- ROE (Return on Equity)
- ROCE (Return on Capital Employed)
- Revenue Growth
- Profit Margin %

All combined and converted to a 0–10 score.
""")
st.subheader("📌 3. Risk Score")
st.write("""
Risk score uses *Debt-to-Equity (D/E ratio)*.
- High D/E means high risk → lower score
- Low D/E means safe company → higher score

Score = 10 – (D/E × 5)
""")

st.subheader("📌 4. Valuation Score")
st.write("""
Compares *stock PE* with *industry PE*.
- If stock PE < industry PE → undervalued → higher score
- If stock PE > industry PE → overvalued → lower score
""")

st.subheader("📌 5. Momentum Score")
st.write("""
Measures where current price stands between 52-week high and low.
- If price is closer to high → momentum strong
- If price closer to low → weak momentum
""")

st.markdown("---")
st.subheader("🎯 Final Recommendation")
st.write("""
The AI averages all 5 scores:
*Final Score = (Intrinsic + Growth + Risk + Valuation + Momentum) / 5*

Recommendation logic:
- *8–10 → STRONG BUY*
- *6–7.9 → BUY*
- *4–5.9 → HOLD*
- *0–3.9 → SELL*

This makes the system honest, transparent, and easy to understand.
""")

st.markdown("---")

st.write("Made by *Akash Dewan*")



# COMPARE MULTIPLE STOCKS PAGE
with tabs[2]:
    st.title("📊 Compare Multiple Stocks")
    tickers_input = st.text_input(
    "Enter multiple NSE tickers (comma separated):",
    placeholder="Example: TCS.NS, RELIANCE.NS, HDFCBANK.NS"
)

if tickers_input:
    tickers = [t.strip() for t in tickers_input.split(",")]
    rows = []

for t in tickers:
    data = fetch_basic_info(t)
    if not data:
        continue

scores = calculate_scores_from_info(data)
rows.append({
"Ticker": t,
"Price": data["price"],
"Growth": scores["growth"],
"Risk": scores["risk"],
"Momentum": scores["momentum"],
"Final Score": scores["final_score"],
"Recommendation": scores["recommendation"],
})
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No valid data found.")



# FINANCIALS PAGE

with tabs[3]:
    st.title("📑 Company Financials & Latest News")
    ticker_fin = st.text_input("Enter NSE ticker (e.g., RELIANCE.NS):")
    if ticker_fin:
        fin_data = get_news_balance_cashflow_financials(ticker_fin)

if not fin_data:
    st.error("Financial data unavailable.")
    st.stop()
st.subheader("📘 Balance Sheet")

if fin_data["balance_sheet"] is not None:
    st.dataframe(fin_data["balance_sheet"])

st.subheader("💰 Cash Flow")
if fin_data["cashflow"] is not None:
    st.dataframe(fin_data["cashflow"])

st.subheader("📈 Income Statement")
if fin_data["financials"] is not None:
    st.dataframe(fin_data["financials"])

st.subheader("📰 Latest News")
if fin_data["news"]:
    for n in fin_data["news"][:5]:
        st.write("•", n.get("title"))
else:
    st.write("No news available.")


# AI Screener - Top 50 BUY/ STRONG BUY
with tabs[4]:
    st.title("📊 AI Screener")
    st.write("This screener automatically scans a basket of major Indian stocks "
    "and shows only those that your AI engine marks as *BUY* or *STRONG BUY*."
)
run_scan = st.button("Run Full Market Scan")
if run_scan:
    base_dir = os.path.dirname(os.path.abspath(_file_))
    csv_path = os.path.join(base_dir, "nse_list.csv")
    try:
        universe_df = pd.read_csv(csv_path)
    except Exception as e:
        st.error(f"Could not load nse_list.csv: {e}")
        st.stop()
    universe_df.rename(
      columns={universe_df.columns[0]: "Symbol"},
      inplace=True
)

    tickers = (
    universe_df["Symbol"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
    )

    if not tickers:
        st.warning("No tickers found in CSV.")
        st.stop()
        results = []
        progress = st.progress(0)
        total = len(tickers)

        for idx, t in enumerate(tickers):
            data = fetch_basic_info(t)
            if not data:
                progress.progress((idx + 1) / total)
                continue

            scores = calculate_scores_from_info(data)
            if scores["recommendation"] in ("BUY", "STRONG BUY"):
                results.append({
                "Ticker": t,
                "Price": data["price"],
                "Final Score": scores["final_score"],
                "Recommendation": scores["recommendation"],
                })

            progress.progress((idx + 1) / total)


        if results:
            df = pd.DataFrame(results)
            df = df.sort_values("Final Score", ascending=False).head(50)
            st.success(f"Found {len(df)} BUY / STRONG BUY stocks")
            st.dataframe(df, use_container_width=True)
            st.caption("Educational use only. Not financial advice.")
        else:
            st.warning("No BUY or STRONG BUY stocks found.")





# STOCK ANALYSIS PAGE
with tabs[5]:
    st.title("📈 Stock AI Analysis")
    st.warning("⚠ Disclaimer: This analysis is only for educational purposes. Please do your own research before investing.")
    ticker = st.text_input("Enter NSE ticker (e.g., RELIANCE.NS):")


if ticker:
    data = fetch_basic_info(ticker)
if not data:
    st.error("Data unavailable right now.")
    st.stop()

scores = calculate_scores_from_info(data)

st.metric("Current Price", data["price"])
st.metric("Final Score", scores["final_score"])
st.metric("Recommendation", scores["recommendation"])
st.write("### Score Breakdown")
st.write("Growth:", scores["growth"])
st.write("Risk:", scores["risk"])
st.write("Momentum:", scores["momentum"])






