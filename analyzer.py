import matplotlib.pyplot as plt
import yfinance as yf


def safe_divide(a, b):
    if b == 0:
        return None
    return a / b


def calculate_score(profit_margin, current_ratio, debt_to_equity, return_on_assets):
    score = 0

    if profit_margin is not None:
        score += profit_margin * 100

    if current_ratio is not None:
        score += min(current_ratio, 5) * 10  # cap it

    if debt_to_equity is not None and debt_to_equity > 0:
        score += max(0, (2 - debt_to_equity)) * 10

    if return_on_assets is not None:
        score += return_on_assets * 100

    return score


def get_recommendation(score):
    if score >= 130:
        return "BUY"
    elif score >= 100:
        return "HOLD"
    else:
        return "RISKY"


def analyze_financials(company, revenue, net_income, current_assets, current_liabilities, total_debt, total_equity, total_assets):
    profit_margin = safe_divide(net_income, revenue)
    current_ratio = safe_divide(current_assets, current_liabilities)
    debt_to_equity = safe_divide(total_debt, total_equity)
    return_on_assets = safe_divide(net_income, total_assets)

    print(f"\nAnalyzing {company}...")

    return profit_margin, current_ratio, debt_to_equity, return_on_assets


def plot_scores(results):
    companies = [c for c, s in results]
    scores = [s for c, s in results]
    labels = [get_recommendation(s) for c, s in results]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(companies, scores)

    for bar, label in zip(bars, labels):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, label,
                 ha='center', va='bottom')

    plt.title("Company Financial Scores")
    plt.xlabel("Company")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.show()


def main():
    tickers = ["AAPL", "TSLA", "NKE"]
    results = []

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        revenue = info.get("totalRevenue", 0)
        net_income = info.get("netIncomeToCommon", 0)
        total_assets = info.get("totalAssets", 0)
        total_debt = info.get("totalDebt", 0)
        total_equity = info.get("totalStockholderEquity") or 1

        current_assets = info.get("totalCurrentAssets", 0)
        current_liabilities = info.get("totalCurrentLiabilities", 1)

        pm, cr, de, roa = analyze_financials(
            ticker,
            revenue,
            net_income,
            current_assets,
            current_liabilities,
            total_debt,
            total_equity,
            total_assets
        )

        score = calculate_score(pm, cr, de, roa)
        results.append((ticker, score))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\nCompany Rankings")
    print("----------------------------")

    for i, (company, score) in enumerate(results, start=1):
        print(f"{i}. {company} | Score: {score:.2f} | {get_recommendation(score)}")

    plot_scores(results)


if __name__ == "__main__":
    main()