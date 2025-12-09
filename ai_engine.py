import yfinance as yf

def fetch_basic_info(ticker: str):
    s = yf.Ticker(ticker)
    return s, s.info

def calculate_scores_from_info(i: dict):
    try:
        p = i.get("currentPrice")
        e = i.get("trailingEps")
        b = i.get("bookValue")
        x = (i.get("returnOnEquity") or 0) * 100
        y = (i.get("returnOnCapitalEmployed") or 0) * 100
        z = (i.get("revenueGrowth") or 0) * 100
        w = (i.get("profitMargins") or 0) * 100
        d = i.get("debtToEquity") or 0
        t = i.get("trailingPE")

        # intrinsic
        if p and e and b:
            q = ((b + e * 15) / (2 * p)) * 10
            q = 0 if q < 0 else (10 if q > 10 else q)
        else:
            q = 0

        # growth
        g = (x + y + z + w) / 20
        g = 0 if g < 0 else (10 if g > 10 else g)

        # risk
        r = 10 - (d * 5)
        r = 0 if r < 0 else (10 if r > 10 else r)

        # valuation
        if t:
            u = t * 1.15
            v = ((u - t) / u) * 10
            v = 0 if v < 0 else (10 if v > 10 else v)
        else:
            v = 0

        # momentum
        h = i.get("fiftyTwoWeekHigh")
        l = i.get("fiftyTwoWeekLow")
        if h and l and p and h != l:
            m = ((p - l) / (h - l)) * 10
            m = 0 if m < 0 else (10 if m > 10 else m)
        else:
            m = 0

        # final score
        f = (q + g + r + v + m) / 5

        if f >= 8:
            rec = "STRONG BUY"
        elif f >= 6:
            rec = "BUY"
        elif f >= 4:
            rec = "HOLD"
        else:
            rec = "SELL"

        return {
            "price": p,
            "eps": e,
            "book": b,
            "roe": x,
            "roce": y,
            "de": d,
            "intrinsic": q,
            "growth": g,
            "risk": r,
            "valuation": v,
            "momentum": m,
            "final_score": round(f, 2),
            "recommendation": rec,
        }
    except:
        return {
            "price": None,
            "eps": None,
            "book": None,
            "roe": 0,
            "roce": 0,
            "de": 0,
            "intrinsic": 0,
            "growth": 0,
            "risk": 0,
            "valuation": 0,
            "momentum": 0,
            "final_score": 0,
            "recommendation": "SELL",
        }

def get_news_balance_cashflow_financials(ticker: str):
    s = yf.Ticker(ticker)
    return s, s.news, s.balance_sheet, s.cashflow,s.financials