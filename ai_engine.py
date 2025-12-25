import time
import yfinance as yf

# -------------------------------------------------
# SAFE FETCH WITH RETRY (RATE-LIMIT PROTECTION)
# -------------------------------------------------
def fetch_basic_info(ticker: str, retries: int = 2, delay: float = 1.5):
    """
    Safely fetch yfinance Ticker object and info dict.
    Retries automatically if Yahoo rate-limits.
    """
    for attempt in range(retries + 1):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if info:
                return stock, info
        except Exception:
            if attempt < retries:
                time.sleep(delay)
            else:
                return None, {}

    return None, {}


# -------------------------------------------------
# AI SCORE CALCULATION (RULE-BASED, SAFE)
# -------------------------------------------------
def calculate_scores_from_info(info: dict):
    """
    Computes AI scores using defensive defaults.
    Never raises exceptions.
    """

    # -------- BASIC METRICS --------
    price = info.get("currentPrice") or 0
    eps = info.get("trailingEps") or 0
    book = info.get("bookValue") or 0

    roe = (info.get("returnOnEquity") or 0) * 100
    roce = (info.get("returnOnCapitalEmployed") or 0) * 100
    de = info.get("debtToEquity") or 0

    revenue_growth = (info.get("revenueGrowth") or 0) * 100
    profit_margin = (info.get("profitMargins") or 0) * 100

    pe = info.get("trailingPE")
    high_52 = info.get("fiftyTwoWeekHigh")
    low_52 = info.get("fiftyTwoWeekLow")

    # -------- INTRINSIC VALUE SCORE --------
    if price > 0 and eps > 0 and book > 0:
        intrinsic = ((book + eps * 15) / (2 * price)) * 10
    else:
        intrinsic = 0

    intrinsic = max(0, min(10, intrinsic))

    # -------- GROWTH SCORE --------
    growth = (roe + roce + revenue_growth + profit_margin) / 20
    growth = max(0, min(10, growth))

    # -------- RISK SCORE --------
    risk = 10 - (de * 5)
    risk = max(0, min(10, risk))

    # -------- VALUATION SCORE --------
    if pe and pe > 0:
        industry_pe = pe * 1.15
        valuation = ((industry_pe - pe) / industry_pe) * 10
        valuation = max(0, min(10, valuation))
    else:
        valuation = 0

    # -------- MOMENTUM SCORE --------
    if high_52 and low_52 and price > 0 and high_52 != low_52:
        momentum = ((price - low_52) / (high_52 - low_52)) * 10
        momentum = max(0, min(10, momentum))
    else:
        momentum = 0

    # -------- FINAL SCORE --------
    final_score = round(
        (intrinsic + growth + risk + valuation + momentum) / 5, 2
    )

    # -------- RECOMMENDATION --------
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
        "intrinsic": intrinsic,
        "growth": growth,
        "risk": risk,
        "valuation": valuation,
        "momentum": momentum,
        "final_score": final_score,
        "recommendation": recommendation,
    }


# -------------------------------------------------
# FINANCIALS + NEWS (OPTIONAL, SAFE)
# -------------------------------------------------
def get_news_balance_cashflow_financials(ticker: str):
    """
    Fetches news, balance sheet, cashflow, financials.
    Returns empty objects on failure (never crashes).
    """
    try:
        stock = yf.Ticker(ticker)
        return (
            stock.news or [],
            stock.balance_sheet,
            stock.cashflow,
            stock.financials,
        )
    except Exception:
        return [], None, None, None
