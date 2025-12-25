import time
import yfinance as yf

def fetch_basic_info(ticker, retries=2, delay=1.5):
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
    
def calculate_scores_from_info(info):
    price = info.get("currentPrice") or 0
    eps = info.get("trailingEps") or 0
    book = info.get("bookValue") or 0

    roe = (info.get("returnOnEquity") or 0) * 100
    roce = (info.get("returnOnCapitalEmployed") or 0) * 100
    de = info.get("debtToEquity") or 0

    rg = (info.get("revenueGrowth") or 0) * 100
    pm = (info.get("profitMargins") or 0) * 100

    pe = info.get("trailingPE")
    high = info.get("fiftyTwoWeekHigh")
    low = info.get("fiftyTwoWeekLow")

    intrinsic = ((book + eps * 15) / (2 * price)) * 10 if price and eps and book else 0
    intrinsic = max(0, min(10, intrinsic))

    growth = (roe + roce + rg + pm) / 20
    growth = max(0, min(10, growth))

    risk = max(0, min(10, 10 - (de * 5)))

    try:
        pe = float(pe)
    except (TypeError, ValueError):
        pe = 0
    if pe > 0:
        industry_pe = pe * 1.15
        valuation = ((industry_pe - pe) / industry_pe) * 10
        valuation = max(0, min(10, valuation))
    else:
        valuation = 0

    if high and low and price and high != low:
        momentum = ((price - low) / (high - low)) * 10
        momentum = max(0, min(10, momentum))
    else:
        momentum = 0

    final = round((intrinsic + growth + risk + valuation + momentum) / 5, 2)

    if final >= 8:
        reco = "STRONG BUY"
    elif final >= 6:
        reco = "BUY"
    elif final >= 4:
        reco = "HOLD"
    else:
        reco = "SELL"

    return{
        "price":price,
        "intrinsic":intrinsic,
        "growth":growth,
        "risk":risk,
        "valuation":valuation,
        "momentum":momentum,
        "final_score":final,
        "recommendation":reco,
}
