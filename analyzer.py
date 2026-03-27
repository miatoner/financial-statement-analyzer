import matplotlib.pyplot as plt
import yfinance as yf


def safe_divide(a, b):
    if b is None or b == 0:
        return None
    return a / b


def calculate_score(profit_margin, current_ratio, debt_to_equity, return_on_assets):
    score = 0

    if profit_margin is not None:
        score += profit_margin * 100

    if current_ratio is not None:
        score += min(current_ratio, 5) * 10

    if debt_to_equity is not None and debt_to_equity > 0:
        score += max(0, (2 - debt_to_equity)) * 10

    if return_on_assets is not None:
        score += return_on_assets * 100

    return score


def get_recommendation(score):
    if score >= 70:
        return "BUY"
    elif score >= 40:
        return "HOLD"
    else:
        return "RISKY"


def get_first_value(df, possible_rows):
    if df is None or df.empty:
        return None

    for row_name in possible_rows:
        if row_name in df.index:
            value = df.loc[row_name].iloc[0]
            if value is not None:
                return value

    return None


def analyze_financials(company, revenue, net_income, current_assets, current_liabilities, total_debt, total_equity, total_assets):
    profit_margin = safe_divide(net_income, revenue)
    current_ratio = safe_divide(current_assets, current_liabilities)
    debt_to_equity = safe_divide(total_debt, total_equity)
    return_on_assets = safe_divide(net_income, total_assets)

    print(f"\nAnalyzing {company}...")
    print("----------------------------")
    print(f"Revenue: {revenue}")
    print(f"Net Income: {net_income}")
    print(f"Current Assets: {current_assets}")
    print(f"Current Liabilities: {current_liabilities}")
    print(f"Total Debt: {total_debt}")
    print(f"Total Equity: {total_equity}")
    print(f"Total Assets: {total_assets}")

    if profit_margin is not None:
        print(f"Profit Margin: {profit_margin:.2%}")
    else:
        print("Profit Margin: Cannot calculate")

    if current_ratio is not None:
        print(f"Current Ratio: {current_ratio:.2f}")
    else:
        print("Current Ratio: Cannot calculate")

    if debt_to_equity is not None:
        print(f"Debt-to-Equity Ratio: {debt_to_equity:.2f}")
    else:
        print("Debt-to-Equity Ratio: Cannot calculate")

    if return_on_assets is not None:
        print(f"Return on Assets (ROA): {return_on_assets:.2%}")
    else:
        print("Return on Assets (ROA): Cannot calculate")

    return profit_margin, current_ratio, debt_to_equity, return_on_assets


def plot_scores(results):
    companies = [company for company, score in results]
    scores = [score for company, score in results]
    labels = [get_recommendation(score) for company, score in results]

    colors = []
    for label in labels:
        if label == "BUY":
            colors.append("green")
        elif label == "HOLD":
            colors.append("gold")
        else:
            colors.append("red")

    plt.figure(figsize=(9, 5))
    bars = plt.bar(companies, scores, color=colors)

    plt.title("Company Financial Scores")
    plt.xlabel("Company")
    plt.ylabel("Score")

    for bar, label in zip(bars, labels):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            label,
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig("financial_scores_chart.png")
    plt.show()


def get_company_data(ticker):
    stock = yf.Ticker(ticker)

    financials = stock.financials
    balance_sheet = stock.balance_sheet

    revenue = get_first_value(financials, ["Total Revenue", "Operating Revenue"])
    net_income = get_first_value(financials, ["Net Income", "Net Income Common Stockholders"])
    current_assets = get_first_value(balance_sheet, ["Current Assets", "Total Current Assets"])
    current_liabilities = get_first_value(balance_sheet, ["Current Liabilities", "Total Current Liabilities"])
    total_debt = get_first_value(balance_sheet, ["Total Debt", "Long Term Debt And Capital Lease Obligation", "Long Term Debt"])
    total_equity = get_first_value(balance_sheet, ["Stockholders Equity", "Total Equity Gross Minority Interest"])
    total_assets = get_first_value(balance_sheet, ["Total Assets"])

    if revenue is None or net_income is None or total_assets is None:
        return None

    if total_equity is None or total_equity <= 0:
        total_equity = 1

    if current_liabilities is None or current_liabilities <= 0:
        current_liabilities = 1

    if current_assets is None:
        current_assets = 0

    if total_debt is None:
        total_debt = 0

    return {
        "ticker": ticker,
        "revenue": revenue,
        "net_income": net_income,
        "current_assets": current_assets,
        "current_liabilities": current_liabilities,
        "total_debt": total_debt,
        "total_equity": total_equity,
        "total_assets": total_assets,
    }


def main():
    tickers = [t.strip().upper() for t in input("Enter stock tickers (comma separated): ").split(",")]
    results = []

    for ticker in tickers:
        try:
            data = get_company_data(ticker)

            if data is None:
                print(f"\nSkipping {ticker}: missing financial statement data")
                continue

            pm, cr, de, roa = analyze_financials(
                data["ticker"],
                data["revenue"],
                data["net_income"],
                data["current_assets"],
                data["current_liabilities"],
                data["total_debt"],
                data["total_equity"],
                data["total_assets"]
            )

            score = calculate_score(pm, cr, de, roa)
            results.append((ticker, score))

        except Exception as e:
            print(f"\nError with {ticker}: {e}")

    if not results:
        print("\nNo valid companies were analyzed.")
        return

    results.sort(key=lambda x: x[1], reverse=True)

    print("\nCompany Rankings")
    print("----------------------------")
    for i, (company, score) in enumerate(results, start=1):
        print(f"{i}. {company} | Score: {score:.2f} | {get_recommendation(score)}")

    best = results[0]
    worst = results[-1]

    print(f"\nTop Pick: {best[0]} ({get_recommendation(best[1])})")
    print(f"Weakest: {worst[0]} ({get_recommendation(worst[1])})")

    plot_scores(results)


if __name__ == "__main__":
    main()