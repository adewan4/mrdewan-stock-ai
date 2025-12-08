import yfinance as yf

# -----------------------------------------------------------
# FETCH BASIC STOCK INFO
# -----------------------------------------------------------
def fetch_basic_info(ticker: str):
    """Fetch stock object and info dictionary from yfinance."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return stock, info


# -----------------------------------------------------------
# AI SCORE CALCULATIONS
# -----------------------------------------------------------
def calculate_scores_from_info(info: dict):
    """
    Uses yfinance info dict to compute:
    intrinsic, growth, risk, valuation, momentum,
    final_score, recommendation
    """

    # Basic data
    price = info.get("currentPrice")
    eps = info.get("trailingEps")
    book = info.get("bookValue")

    # ROE / ROCE
    roe = info.get("returnOnEquity") or 0
    roce = info.get("returnOnCapitalEmployed") or 0
    roe *= 100
    roce *= 100

    # Debt-to-equity
    de = info.get("debtToEquity") or 0

    # -----------------------------
    # INTRINSIC SCORE
    # -----------------------------
    if price and eps and book:
        intrinsic = ((book + eps * 15) / (2 * price)) * 10
        intrinsic = max(0, min(10, intrinsic))
    else:
        intrinsic = 0

    # -----------------------------
    # GROWTH SCORE
    # -----------------------------
    rg = (info.get("revenueGrowth") or 0) * 100
    pg = (info.get("profitMargins") or 0) * 100

    growth = (roe + roce + rg + pg) / 20
    growth = max(0, min(10, growth))

    # -----------------------------
    # RISK SCORE
    # -----------------------------
    risk = 10 - (de * 5)
    risk = max(0, min(10, risk))

    # -----------------------------
    # VALUATION SCORE
    # -----------------------------
    pe = info.get("trailingPE")
    if pe:
        industry_pe = pe * 1.15
        valuation = ((industry_pe - pe) / industry_pe) * 10
        valuation = max(0, min(10, valuation))
    else:
        valuation = 0

    # -----------------------------
    # MOMENTUM SCORE
    # -----------------------------
    high = info.get("fiftyTwoWeekHigh")
    low = info.get("fiftyTwoWeekLow")

    if high and low and price and high != low:
        momentum = ((price - low) / (high - low)) * 10
        momentum = max(0, min(10, momentum))
    else:
        momentum = 0

    # -----------------------------
    # FINAL SCORE + RECOMMENDATION
    # -----------------------------
    final = (intrinsic + growth + risk + valuation + momentum) / 5

    if final >= 8:
        reco = "STRONG BUY"
    elif final >= 6:
        reco = "BUY"
    elif final >= 4:
        reco = "HOLD"
    else:
        reco = "SELL"

    return {
        "price": price,
        "eps": eps,
        "book": book,
        "roe": roe,
        "roce": roce,
        "de": de,
        "intrinsic": intrinsic,
        "growth": growth,
        "risk": risk,
        "valuation": valuation,
        "momentum": momentum,
        "final_score": round(final, 2),
        "recommendation": reco,
    }


# -----------------------------------------------------------
# FINANCIALS PAGE HELPERS: NEWS + BALANCE SHEET + CASHFLOW
# -----------------------------------------------------------
def get_news_balance_cashflow_financials(ticker: str):
    """Returns news, balance sheet, cashflow, income statement."""
    stock = yf.Ticker(ticker)
    news = stock.news
    bs = stock.balance_sheet
    cf = stock.cashflow
    fin = stock.financials
    return stock, news, bs, cf, fin