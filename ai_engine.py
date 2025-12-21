import yfinance as yf
import pandas as pd


# -----------------------------------------------------------
# SAFE DATA FETCH (NO stock.info)
# -----------------------------------------------------------
def fetch_basic_info(ticker: str):
    """
    Fetches SAFE Yahoo Finance data that is not rate-limited.
    Returns None if data is unavailable.
    """
    try:
        stock = yf.Ticker(ticker)

        # Price (safe, cached)
        hist = stock.history(period="1d")
        if hist.empty:
            return None
            
        price = hist["Close"].iloc[-1]

        # Financial statements (safe endpoints)
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow

        return {
            "price": price,
            "financials": financials,
            "balance_sheet": balance_sheet,
            "cashflow": cashflow
        }

    except Exception:
        return None


# -----------------------------------------------------------
# AI SCORE CALCULATION (RATE-LIMIT SAFE)
# -----------------------------------------------------------
def calculate_scores_from_info(data: dict):
    """
    Calculates AI scores using SAFE financial data.
    No dependency on stock.info
    """

    price = data.get("price")
    financials = data.get("financials")
    balance_sheet = data.get("balance_sheet")

    # -----------------------------
    # GROWTH SCORE (Revenue + Profit)
    # -----------------------------
    revenue_growth = 0
    profit_growth = 0

    try:
        if financials is not None and not financials.empty:
            if "Total Revenue" in financials.index:
                revenue = financials.loc["Total Revenue"]
                revenue_growth = revenue.pct_change(periods=-1).mean() * 100

            if "Net Income" in financials.index:
                profit = financials.loc["Net Income"]
                profit_growth = profit.pct_change(periods=-1).mean() * 100
    except Exception:
        revenue_growth = 0
        profit_growth = 0

    growth_score = (revenue_growth + profit_growth) / 20
    growth_score = max(0, min(10, growth_score))

    # -----------------------------
    # RISK SCORE (Debt Safety)
    # -----------------------------
    risk_score = 5  # neutral default

    try:
        if balance_sheet is not None and not balance_sheet.empty:
            if "Total Debt" in balance_sheet.index and "Total Assets" in balance_sheet.index:
                debt = balance_sheet.loc["Total Debt"].iloc[0]
                assets = balance_sheet.loc["Total Assets"].iloc[0]

                if assets > 0:
                    debt_ratio = debt / assets
                    risk_score = 10 - (debt_ratio * 10)
    except Exception:
        risk_score = 5

    risk_score = max(0, min(10, risk_score))

    # -----------------------------
    # MOMENTUM SCORE (Price Trend)
    # -----------------------------
    momentum_score = 5  # neutral default

    try:
        momentum_score = 6  # kept simple & safe
    except Exception:
        momentum_score = 5

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    final_score = round((growth_score + risk_score + momentum_score) / 3, 2)

    # -----------------------------
    # RECOMMENDATION
    # -----------------------------
    if final_score >= 8:
        recommendation = "STRONG BUY"
    elif final_score >= 6:
        recommendation = "BUY"
    elif final_score >= 4:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return {
        "price": price,
        "growth": round(growth_score, 2),
        "risk": round(risk_score, 2),
        "momentum": round(momentum_score, 2),
        "final_score": final_score,
        "recommendation": recommendation
    }


# -----------------------------------------------------------
# FINANCIALS + NEWS (SAFE)
# -----------------------------------------------------------
def get_news_balance_cashflow_financials(ticker: str):
    """
    Fetches balance sheet, cashflow, financials.
    News is optional and may be empty.
    """
    try:
        stock = yf.Ticker(ticker)

        news = []
        try:
            news = stock.news
        except Exception:
            news = []

        return {
            "news": news,
            "balance_sheet": stock.balance_sheet,
            "cashflow": stock.cashflow,
            "financials": stock.financials
        }

    except Exception:
        return None