import os
import datetime

with open("tickers.txt") as f:
    tickers = f.read().strip().split("\n")
    #tickers = map(lambda x: f'ticker({x})' ,tickers)
    #print (tickers)


def isdone():
    with open("done.txt") as f:
        __done = f.read().split("\n")

for ticker in tickers:
    print("-------------------------- start |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
    
    __done = isdone()

    if "ticker({})".format(ticker) in __done:
        print("Already done -> ", ticker)
    else:
        os.environ["SEARCHTERM"]="ticker({})".format(ticker)
        #os.system("sh test.sh")

        while not ticker in isdone():
            print("---> RUNNING -> {}".format(ticker))
            os.system("jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute scrap-clean-code.ipynb") 
    print("-------------------------- end |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
