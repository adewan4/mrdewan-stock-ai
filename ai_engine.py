import time
import yfinance as yf
import pandas as pd

# -------------------------------------------------
# SAFE FETCH WITH RETRY (RATE-LIMIT PROTECTION)
# -------------------------------------------------
def fetch_basic_info(ticker: str, retries: int = 2, delay: float = 1.5):
    for attempt in range(retries + 1):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            if isinstance(info, dict) and info:
                return stock, info
        except Exception:
            if attempt < retries:
                time.sleep(delay)
            else:
                return None, {}
    return None, {}
    
    
    
# -------------------------------------------------
# LONG-TERM AI SCORE ENGINE
# ------------------------------------
def calculate_scores_from_info(info: dict):
    price = info.get("currentPrice") or 0
    eps = info.get("trailingEps") or 0
    book = info.get("bookValue") or 0
    
    
    roe = (info.get("returnOnEquity") or 0) * 100
    roce = (info.get("returnOnCapitalEmployed") or 0) * 100
    de = info.get("debtToEquity") or 0
    
    
    revenue_growth = (info.get("revenueGrowth") or 0) * 100
    profit_margin = (info.get("profitMargins") or 0) * 100
    
    

    # ---------- Intrinsic ----------

    if price > 0 and eps > 0 and book > 0:
        intrinsic = ((book + eps * 15) / (2 * price)) * 10
    else:
        intrinsic = 0
        intrinsic = max(0, min(10, intrinsic))
    
    # ---------- Growth ----------
    growth = (roe + roce + revenue_growth + profit_margin) / 20
    growth = max(0, min(10, growth))
    
    # ---------- Risk ----------
    risk = 10 - (de * 5)
    risk = max(0, min(10, risk))
    
    # ---------- Valuation ----------
    
    pe = info.get("trailingPE")
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
        
    # ---------- Momentum ----------
    
    high_52 = info.get("fiftyTwoWeekHigh")
    low_52 = info.get("fiftyTwoWeekLow")
    
    if high_52 and low_52 and price > 0 and high_52 != low_52:
        momentum = ((price - low_52) / (high_52 - low_52)) * 10
        momentum = max(0, min(10, momentum))
        
    else:
        momentum = 0
        
    final_score = round(
        (intrinsic + growth + risk + valuation + momentum) / 5, 2
    )
    
    if final_score >= 8:
        reco = "STRONG BUY"
    elif final_score >= 6:
        reco = "BUY"
    elif final_score >= 4:
        reco = "HOLD"
    else:
        reco = "SELL"
        
    return {
        "price": price,
        "intrinsic": intrinsic,
        "growth": growth,
        "risk": risk,
        "valuation": valuation,
        "momentum": momentum,
        "final_score": final_score,
        "recommendation": reco,
   }
    

# -------------------------------------------------
# INTRADAY SIGNAL ENGINE (5-MIN)
# -------------------------------------------------

def intraday_signal(ticker: str):
    try:
        df = yf.download(
           ticker,
           period="1d",
           interval="5m",
           progress=False,
           threads=False,
        )
        
        time.sleep(0.4)
        
        if df.empty or len(df) < 20:
            return None
            
        df = df.dropna()
        
        df["VWAP"] = (
          (df["Volume"] * (df["High"] + df["Low"] + df["Close"]) / 3).cumsum()
          / df["Volume"].cumsum()
        )
        
        df["EMA20"] = df["Close"].ewm(span=20).mean()
        df["VOL_AVG"] = df["Volume"].rolling(20).mean()
        
        last = df.iloc[-1]
        
        score = 0
        reasons = []
        
        if last["Close"] > last["VWAP"] and last["Close"] > last["EMA20"]:
            score += 3
            reasons.append("Bullish trend above VWAP & EMA")
        elif last["Close"] < last["VWAP"] and last["Close"] < last["EMA20"]:
            score += 3
            reasons.append("Bearish trend below VWAP & EMA")
            
        if last["VOL_AVG"] > 0 and last["Volume"] > last["VOL_AVG"] * 1.8:
            score += 3
            reasons.append("High volume spike")
            
        if abs(last["Close"] - last["Open"]) / last["Open"] > 0.004:
            score += 2
            reasons.append("Strong momentum candle")
            
        if score >= 6:
            direction = "LONG" if last["Close"] > last["VWAP"] else "SHORT"
        else:
            direction = "NO TRADE"
            
        return {
           "direction": direction,
           "confidence": round(score, 1),
           "price": round(last["Close"], 2),
           "reason": " | ".join(reasons),
        }
        
    except Exception:
        return None
            

