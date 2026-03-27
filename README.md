 Financial Statement Analyzer

A Python tool that analyzes real company financial data, calculates key financial ratios, ranks companies, and generates investment recommendations.

 Features
- Pulls real financial data using yfinance
- Calculates key ratios (profit margin, liquidity, leverage, ROA)
- Ranks companies based on financial performance
- Generates BUY / HOLD / RISKY recommendations
- Visualizes results with color-coded charts
- Saves chart output as an image

 How it Works
1. User enters stock tickers (e.g. AAPL, MSFT, TSLA)
2. Program pulls financial statement data
3. Calculates ratios and scores each company
4. Ranks companies and provides recommendations
5. Displays and saves a chart

 How to Run

Install dependencies:
-install yfinance matplotlib

Run the Program:
-python analyzer.py

Enter tickers:
-Example: TSLA,WMT,AAPL,NVDA

 Example Output
- Company rankings
- BUY / HOLD / RISKY recommendations
- Visual chart saved as `financial_scores_chart.png`

 Notes
- Some companies may be skipped due to missing financial data from Yahoo Finance
- This tool is for educational purposes and not financial advice
