import pandas as pd

# S&P 500 목록을 Wikipedia에서 가져오기
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
tables = pd.read_html(url)

# 첫 번째 테이블이 S&P 500 목록
sp500 = tables[0][["Symbol", "Security"]]
sp500.columns = ["Ticker", "Name"]

# CSV로 저장
sp500.to_csv("sp500.csv", index=False)

print("✅ S&P 500 티커와 이름을 'sp500_companies.csv'에 저장했습니다.")