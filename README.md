### STEP 1
Only to install dependencies, run only once, else skip to STEP 2
`pip install -r req.txt`


### STEP 2

put all tickers in tickers.txt, one in each line

### STEP 3

put the tickers to ignore in done.txt, one in each line
if required to restart all download from begining, delete the ticker from done.txt
### STEP 4 

run `python SUPERVISOR.py`

if you kill SUPERVISOR.py, run `sh kill.sh`

**CAUTION: SUPERVISOR.py kills firefox programs after it finished one ticker, do not use firefox browser for personal browsing while running SUPERVISOR.py**
**CAUTION: kill.sh will kill all firefox and python programs running on your machine**


