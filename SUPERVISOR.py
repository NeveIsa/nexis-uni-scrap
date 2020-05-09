import os
import datetime

with open("tickers.txt") as f:
    tickers = f.read().strip().split("\n")
    #tickers = map(lambda x: f'ticker({x})' ,tickers)
    #print (tickers)


with open("done.txt") as f:
    __done = f.read().split("\n")

for ticker in tickers:
    print("-------------------------- start |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
    
    if "ticker({})".format(ticker) in __done:
        print("Already done -> ", ticker)
    else:
        os.environ["SEARCHTERM"]="ticker({})".format(ticker)
        #os.system("sh test.sh")
        os.system("jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute scrap-clean-code.ipynb") 
    print("-------------------------- end |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
