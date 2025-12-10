import streamlit as st
import yfinance as yf
import pandas as pd
from ai_engine import(
    fetch_basic_info,
    calculate_scores_from_info,
    get_news_balance_cashflow_financials,
)

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
    st.write("Welcome! Use the menu to analyze Indian stocks.")
    
    st.markdown("### 🔍 Quick Stock Lookup")
    quick = st.text_input("Enter NSE stock (e.g., TCS.NS):")
    
    if quick:
        stock = yf.Ticker(quick)
        info = stock.info
        price = info.get("currentPrice")
        
        if price:
            st.metric("Current Price", price)
        else:
            st.error("Invalid stock or data not available.")
            
    st.markdown("---")
    st.write("➡ Go to *Stock Analysis* for full AI analysis.")
    
    
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
        results = []
        
        for t in tickers:
            stock = yf.Ticker(t)
            info = stock.info
            
            price = info.get("currentPrice")
            eps = info.get("trailingEps")
            book = info.get("bookValue")
             
            roe = info.get("returnOnEquity")
            roe = roe * 100 if roe else 0
            roce = info.get("returnOnCapitalEmployed")
            roce = roce * 100 if roce else 0
            de = info.get("debtToEquity")
            de = de if de else 0
            # Intrinsic Score
            if price and eps and book:
                intrinsic = ((book + eps * 15) / (2 * price)) * 10
                intrinsic = max(0, min(10, intrinsic))
            else:
                intrinsic = 0
            # Growth Score
            rg = (info.get("revenueGrowth") or 0) * 100
            pg = (info.get("profitMargins") or 0) * 100
            growth = (roe + roce + rg + pg) / 20
            growth = max(0, min(10, growth))
            # Risk Score
            risk = 10 - (de * 5)
            risk = max(0, min(10, risk))
            # Valuation Score
            pe = info.get("trailingPE")
            if pe:
                industry_pe = pe * 1.15
                valuation = ((industry_pe - pe) / industry_pe) * 10
                valuation = max(0, min(10, valuation))
            else:
                valuation = 0
            # Momentum Score
            high = info.get("fiftyTwoWeekHigh")
            low = info.get("fiftyTwoWeekLow")
            if high and low and price and high != low:
                momentum = ((price - low) / (high - low)) * 10
                momentum = max(0, min(10, momentum))
            else:
                momentum = 0
            # Final Score
            final = (intrinsic + growth + risk + valuation + momentum) / 5
            if final >= 8:
                reco = "STRONG BUY"
            elif final >= 6:
                reco = "BUY"
            elif final >= 4:
                reco = "Hold"
            else:
                reco = "SELL"
            results.append({
                "Ticker":t,
                "Price": price,
                "Intrinsic": round(intrinsic,2),
                "Growth": round(growth,2),
                "Risk" : round(risk,2),
                "valuation" : round(valuation,2),
                "momentum": round(momentum,2),
                "Final Score" : round(final,2),
                "Recommendation" : reco
            })
        st.write("### 📋 Comparison Table")
        st.dataframe(results)

# FINANCIALS PAGE

with tabs[3]:
    st.title("📑 Company Financials & Latest News")
    ticker_fin = st.text_input("Enter NSE ticker (e.g., RELIANCE.NS):")
    if ticker_fin:
        stock = yf.Ticker(ticker_fin)
        st.subheader("📊 Latest News")
        try:
            news = stock.news
            if news:
                for item in news[:5]:
                    st.write("### " + item["title"])
                    st.write(item["link"])
                    st.markdown("---")
            else:
                st.write("No news available.")
        except:
            st.write("News not available.")
        st.subheader("📘 Balance Sheet")
        try:
            bs = stock.balance_sheet
            if not bs.empty:
                st.dataframe(bs)
            else:
                st.write("No balance sheet available.")
        except:
            st.write("Balance sheet not available.")
            
        st.subheader("💰 Cash Flow Statement")
        try:
            cf = stock.cashflow
            if not cf.empty:
                st.dataframe(cf)
            else:
                st.write("No cashflow data available.")
        except:
            st.write("Cashflow data not available.")
        st.subheader("📈 Financial Performance (Income Statement)")
        try:
            fin = stock.financials
            if not fin.empty:
                st.dataframe(fin)
            else:
                st.write("No financial statement available.")
        except:
            st.write("Financials not available.")
            
        # TREND CHARTS

        st.markdown("### 📊 Trend Charts (Revenue & Profit Trend)")
        try:
            if not fin.empty:
                revenue = fin.loc["Total Revenue"]
                profit = fin.loc["Net Income"]
                st.write("*Revenue Trend*")
                st.line_chart(revenue)
                st.write("*Profit Trend*")
                st.line_chart(profit)
            else:
                st.write("Trend data not available.")
        except:
             st.write("Unable to generate trend charts.")

        # YOY GROWTH %

        st.markdown("### 📈 YoY Growth (%)")
        try:
            if not fin.empty:
                revenue = fin.loc["Total Revenue"]
                profit = fin.loc["Net Income"]
                rev_growth = revenue.pct_change(periods=-1) * -100
                prof_growth = profit.pct_change(periods=-1) * -100
                st.write("*Revenue YoY Growth (%)*")
                st.bar_chart(rev_growth)
                st.write("*Profit YoY Growth (%)*")
                st.bar_chart(prof_growth)
            else:
                st.write("Growth data not available.")
        except:
            st.write("Unable to calculate YoY growth.")
            
        # MANAGEMENT QUALITY RATING

        st.markdown("### 🏅 Management Quality Rating")
        try:
            roe = info.get("returnOnEquity") or 0
            roce = info.get("returnOnCapitalEmployed") or 0
            de = info.get("debtToEquity") or 0
            roe_score = min(10, max(0, (roe * 100) / 20))
            roce_score = min(10, max(0, (roce * 100) / 20))
            debt_score = max(0, 10 - (de / 20))
            management_quality = round((roe_score + roce_score + debt_score) / 3, 2)
            st.write("Management Quality Rating (0–10):", management_quality)
        except:
            st.write("Unable to calculate management rating.")
            
        # AI NEWS SENTIMENT ANALYSIS

        st.markdown("### 🤖 AI News Sentiment Analysis")
        try:
            sentiments = []
            if news:
                for item in news[:5]:
                    headline = item["title"].lower()
                    score = 0
                    if any(x in headline for x in ["profit", "growth", "surge", "up", "record"]):
                        score = 1
                    elif any(x in headline for x in ["loss", "fall", "fraud", "scam", "down"]):
                        score = -1
                    sentiments.append(score)
                final_sent = sum(sentiments)
                st.write("Sentiment Score:", final_sent)
                if final_sent >= 2:
                    st.success("Overall Sentiment: POSITIVE")
                elif final_sent <= -2:
                    st.error("Overall Sentiment: NEGATIVE")
                else:
                    st.warning("Overall Sentiment: NEUTRAL")
            else:
                st.write("No news available.")
        except:
            st.write("Unable to calculate sentiment.")
             
             

# AI Screener - Top 50 BUY/ STRONG BUY
with tabs[4]:
    
    st.title("📊 AI Screener")
    st.write(
    "This screener automatically scans a basket of major Indian stocks "
    "and shows only those that your AI engine marks as *BUY* or *STRONG BUY*."
    )
    run_scan = st.button("Run Full Market Scan")
    if run_scan:
        import os
        import pandas as pd
        
        # Always load CSV from the same folder as this app.py file
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "nse_list.csv")

        
        try:
            universe_df = pd.read_csv(csv_path)
            
        except Exception as e:
            st.error(f"⚠ Could not load nse_list.csv: {e}")
            st.stop()
        # Try to detect the Symbol column
        
        st.write("DEBUG — Columns:",universe_df.columns.tolist())
        
        # FORCE first column to be 'Symbol'
        first_col = universe_df.columns[0]
        universe_df.rename(columns={first_col: "Symbol"}, inplace=True)
        
        # Debug
        st.write("DEBUG — After rename:", universe_df.columns.tolist())            
        
        # Build ticker list
        tickers = (
            universe_df["Symbol"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
        
        st.write("Tickers Loaded:", len(tickers))
        st.write("First few:", tickers[:5])
        if not tickers:
            st.warning("No tickers found in nse_list.csv.")
            st.stop()
            
        st.info("Scanning {0} stocks. Please wait...".format(len(tickers)))
        
        
        results = []
        progress = st.progress(0)
        total = len(tickers)
        for idx, t in enumerate(tickers):
             
            try:
                stock, info = fetch_basic_info(t)
                scores = calculate_scores_from_info(info)
                # Filter only BUY and STRONG BUY
                if scores["recommendation"] in ("BUY", "STRONG BUY"):
                    results.append({
                    "Ticker": t,
                    "Recommendation": reco,
                    "Final Score": scores["final_score"],
                    "Price": scores["price"],
                    "Intrinsic": round(scores["intrinsic"], 2),
                    "Growth": round(scores["growth"], 2),
                    "Risk": round(scores["risk"], 2),
                    "Valuation": round(scores["valuation"], 2),
                    "Momentum": round(scores["momentum"], 2),
                    })
            except Exception:
                # Skip any stock that fails to load
                pass
            # Update progress bar
            progress.progress((idx + 1) / float(total))


        if not results:
            st.warning("No BUY or STRONG BUY candidates found in this universe right now.")
        else:
            df = pd.DataFrame(results)
            df = df.sort_values(by="Final Score", ascending=False).head(50)
            st.success(f"🎉 Found {len(df)} high-conviction BUY/STRONG BUY stocks.")
            st.dataframe(df, use_container_width=True)
            
            st.caption(
            
                "✔ These are the Top 50 highest scoring BUY/STRONG BUY stocks from the entire NSE list.\n"
                "✔ Data fetched using Dewan AI Engine.\n"
                "✔ For educational use only — not financial advice."
            )
            
# STOCK ANALYSIS PAGE
with tabs[5]:
    st.title("📈 Stock AI Analysis")
    st.warning("⚠ Disclaimer: This analysis is only for educational purposes. Please do your own research before investing.")
    ticker = st.text_input("Enter NSE ticker (e.g., RELIANCE.NS):")


    if ticker:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get("currentPrice")
        st.write("Current price:",price)
        eps = info.get("trailingEps")
        book = info.get("bookValue")
        roe = info.get("returnOnEquity")
        if roe:
            roe = roe * 100
        else:
            roe = 0
            
        roce = info.get("returnonCapitalemployed")
        if roce:
            roce = roce * 100
        else:
            roce = 0
            
        de = info.get("debttoequity")
        if de is None:
            de = 0
            
        st.write("EPS:",eps)
        st.write("Book Value:", book)
        st.write("ROE %:", roe)
        st.write("ROCE %:", roce)
        
        
        # Intrinsic Value Score
        if price and eps and book:
            
            intrinsic = ((book + eps * 15) / (2 * price)) * 10
            
            if intrinsic > 10:
                
                intrinsic = 10
            if intrinsic < 0:
                intrinsic = 0
        else:
            Intrinsic = 0
                
        st.write("Intrinsic Value Score:", intrinsic)
            
        # Growth Score
        
        rg = info.get("revenueGrowth")
        pg = info.get("profitMargins")
            
        if rg:
            rg = rg * 100
        else:
            rg = 0
                
        if pg:
            pg = pg * 100
        else:
            pg = 0
                
        growth = (roe + roce + rg + pg) / 20
        if growth > 10:
            growth = 10
        if growth < 0:
            growth = 0
                
        st.write("Growth Score:", growth)
            
        # Risk Score (based on debt/Equity)
        risk = 10 - de * 5
        if risk > 10:
            risk = 10
        if risk < 0:
            risk = 0 
                
        st.write("Risk Score:", risk)
        
        # valuation Score
        pe = info.get("trailingPE")
        if pe:
            industry_pe = pe * 1.15
            valuation = ((industry_pe - pe) / industry_pe) * 10
            if valuation > 10:
                valuation = 10
            if valuation < 0:
                valuation = 0
        else:
            valuation = 0
        
        st.write("Valuation Score:", valuation)
        
        # Momentum Score
        high = info.get("fiftyTwoWeekHigh")
        low = info.get("fiftyTwoWeekLow")
        
        if high and low and price and high != low:
            momentum = ((price - low) / (high - low)) * 10
            if momentum > 10:
                momentum = 10
            if momentum < 0:
                momentum = 0
        else:
            momentum = 0
            
        st.write("Momentum Score:", momentum)
        
        # Final AI Recommendation
        final = (intrinsic + growth + risk + valuation + momentum) / 5
        if final >= 8:
            reco = "Strong Buy"
        elif final >= 6:
            reco = "BUY"
        elif final >= 4:
            reco = "HOLD"
        else:
            reco = "SELL"
            
        st.write("Final Score:", round(final,2))
        st.write("Recommendation:", reco)
        
        # Price Chart (1-Year)
        st.write("### price Chart (1 Year)")
        
        hist = stock.history(period="1y")
        if not hist.empty:
            st.line_chart(hist["Close"])
        else:
            st.write("No price data available for chart.")
            
                
                   
            

        
        