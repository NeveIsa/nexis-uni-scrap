import os

with open("tickers.txt") as f:
    tickers = f.read().strip().split("\n")
    #tickers = map(lambda x: f'ticker({x})' ,tickers)
    #print (tickers)


with open("done.txt") as f:
    __done = f.read().split("\n")

for ticker in tickers:
    print(f"-------------------------- start |  {ticker} | start ------------------------------")
    
    if f"ticker({ticker})" in __done:
        print("Already done -> ", ticker)
    else:
        os.environ["SEARCHTERM"]=f"ticker({ticker})"
        #os.system("sh test.sh")
        os.system("runipy scrap-clean-code.ipynb") 
    print(f"-------------------------- end |  {ticker} | end ------------------------------")
