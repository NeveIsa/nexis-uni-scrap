import os,time
import datetime


#convert to py
os.system("sh convert.sh")

#make required dirs
os.system("mkdir -p browser/download/temp")


with open("tickers.txt") as f:
    tickers = f.read().strip().split("\n")
    #tickers = map(lambda x: f'ticker({x})' ,tickers)
    #print (tickers)


def isdone():
    with open("done.txt") as f:
        __done = f.read().strip().split("\n")
        return __done

for ticker in tickers:
    print("-------------------------- start |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
    
    __done = isdone()

    if "ticker({})".format(ticker) in __done:
        print("Already done -> ", ticker)
    else:
        print("Not done yet -> ",ticker)
        print(ticker)
        os.environ["SEARCHTERM"]="ticker({})".format(ticker)
        #os.system("sh test.sh")

        while not (ticker in isdone()):
            print("---> RUNNING -> {}".format(ticker))
            #os.system("jupyter nbconvert --ExecutePreprocessor.timeout=600 --to notebook --execute scrap-clean-code.ipynb") 
            os.system("python scrap-clean-code.py")
            time.sleep(3)
            os.system("pkill firefox")
    print("-------------------------- end |  {} | {} ------------------------------".format(ticker,datetime.datetime.now().isoformat()))
