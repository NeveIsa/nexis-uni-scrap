#!/usr/bin/env python
# coding: utf-8

# In[1]:


with open("tickers.txt") as f:
    data=f.read()
    tickers = data.strip().split("\n")
    
#print(tickers)


# In[2]:


### IMPORTS

import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
#from selenium.webdriver.common.keys import Keys
import re
import numpy as np
import os
import shutil
import time
import zipfile
from docx import Document
import pandas as pd
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from xml.etree.cElementTree import XML
import sys


# In[3]:


### CONFIGS



month_d = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
#searchTerms = r'JP Morgan'
searchTermsList = [r'oracle', r'morgan stanley']
searchTermsList = map(lambda x: "ticker({})".format(x) ,tickers[:10])
url = r'https://libproxy.usc.edu/login?url=http://www.nexisuni.com'
# url = r'http://libguides.usc.edu/go.php?c=9232127'
username = 'junhuihe'
password = 'ivy930322jasper951128'
# username = 'MyUSCPassUsername'
# password = 'MyUSCPassWord'
#root = r'/Users/jasper/Documents/scrape_help/LexisNexis-Scraping'
root = os.getcwd() + r'/browser'
path_to_chromedriver = root + r'/operadriver'
path_to_ffdriver = root + r'/geckodriver'

#download_folder = root + r'\{}\download'.format(searchTerms)
# path_to_chromedriver = root + r'\chromedriver'
# download_folder = root + r'\download'
# dead_time = 300
dead_time = 300


## NEW PARAMS
__default_enddate = "December.2014"

__default_startdate = "January.2005"


# In[4]:


### DOWNLOAD METHOD


def download_file(searchTerms, download_folder, url = url, username = username,                   dead_time = dead_time, path_to_chromedriver=path_to_chromedriver, enddate=__default_enddate):
    while True:
        endmonth,endyear = enddate.split(".")
        
        startmonth,startyear = __default_startdate.split(".")
        
        try:
            
            __DRIVER = "OP" #  OP -opera

            if __DRIVER=="FF":
                #### FIREFOX OPTIONS
                

                profile = webdriver.FirefoxProfile()
                profile.set_preference("browser.download.folderList", 2)
                profile.set_preference("browser.download.manager.showWhenStarting", False)
                profile.set_preference("browser.download.dir", download_folder + r'/temp')
                profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-zip-compressed")
                
                #make headless
                from selenium.webdriver.firefox.options import Options
                __options = Options()
                __options.headless = False
                browser = webdriver.Firefox(executable_path = path_to_ffdriver,firefox_options=__options,firefox_profile=profile)


            elif __DRIVER=="OP":
                ### CHROME/OPERA
                

                # chromeOptions = webdriver.ChromeOptions()
                prefs = {"download.default_directory" : download_folder + r'/temp'}
                # chromeOptions.add_argument('headless')
                chromeOptions = webdriver.ChromeOptions()
                # chromeOptions.add_argument("--window-size=1800,1000")
                # chromeOptions.add_argument("--disable-extensions")
                # chromeOptions.add_argument("--proxy-server='direct://'")
                # chromeOptions.add_argument("--proxy-bypass-list=*")
                # chromeOptions.add_argument("--start-maximized")
                # chromeOptions.add_argument('--headless')
                # chromeOptions.add_argument('--disable-gpu')
                # chromeOptions.add_argument('--disable-dev-shm-usage')
                # chromeOptions.add_argument('--no-sandbox')
                # chromeOptions.add_argument('--ignore-certificate-errors')
                # chromeOptions.add_argument('no-sandbox')
                chromeOptions.add_experimental_option("prefs",prefs)
                browser = webdriver.Chrome(executable_path = path_to_chromedriver, options=chromeOptions)

                        
            print("scraping starts")
            browser.set_window_size(1800, 1000)
            #browser.set_window_size(900, 500)
            #Login
            browser.get(url)
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("login in time out")
                    raise Exception()
                try:
                    browser.find_element_by_id('username').send_keys(username)
                    break
                except:
                    time.sleep(2)
            browser.find_element_by_id('password').send_keys(password)
            browser.find_element_by_xpath('//*[@id="loginform"]/div[4]/button').click()
            print("{} login in successfully".format(username))
            # Get Page Info
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("redirect to search page time out")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="searchTerms"]').send_keys(searchTerms)
                    break
                except:
                    time.sleep(2)
            browser.find_element_by_xpath('//*[@id="mainSearch"]').click()
            # Sort by Date and narrow by some conditions
            #publication type
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("setting publication type conditions timeout")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="podfiltersbuttonpublicationtype"]').click()
                    break
                except:
                    time.sleep(2)
            try:
                browser.find_element_by_class_name('more').click()
            except:
                pass
            while True:
                try:
                    for ele in browser.find_elements_by_xpath("//*[contains(text(), 'Newswires & Press Releases')]"):
                        try:
                            ele.click()
                            break
                        except:
                            pass
                    break
                except:
                    time.sleep(2)
            print("publication type is set")
            #source
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("setting source conditions timeout")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="podfiltersbuttonsource"]').click()
                    break
                except:
                    time.sleep(2)
            try:
                # browser.find_element_by_xpath('//*[@id="refine"]/ul[1]/li[7]/button').click()
                browser.find_element_by_class_name('more').click()
            except:
                pass
            try:
                for ele in browser.find_elements_by_xpath("//*[contains(text(), 'Business Wire')]"):
                    try:
                        ele.click()
                        break
                    except:
                        pass
                #browser.find_element_by_text_link('The Associated Press').click()
                #browser.find_elements_by_xpath("//*[contains(text(), 'My Button')]").click()
                print("source is set")
            except:
                pass
            # timeline start
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("setting timeline time out")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="refine"]/button[2]').click()
                    break
                except:
                    time.sleep(2)
            if int(browser.find_element_by_xpath('//*[@id="refine"]/div[2]/div[4]/div[1]/input').get_attribute('value').split('/')[-1]) <= 2001:
                browser.find_element_by_xpath('//*[@id="refine"]/div[2]/div[4]/div[1]/button').click()
                browser.find_element_by_xpath('//*[@id="selectyeartimeline"]').click()
                #browser.find_element_by_xpath('//*[@id="datepicker"]/h3/div[2]/ol/li[33]/button').click()
                for ele in browser.find_elements_by_xpath("//*[contains(text(), '"+startyear+"')]"):
                    try:
                        ele.click()
                        break
                    except:
                        pass
                browser.find_element_by_xpath('//*[@id="selectmonthtimeline"]').click()
                for ele in browser.find_elements_by_xpath("//*[contains(text(), '"+startmonth+"')]"):
                    try:
                        ele.click()
                        break
                    except:
                        pass
                browser.find_element_by_xpath('//*[@id="datepicker"]/table/tbody/tr[2]/td[3]/button').click()
            # timeline end
            if int(browser.find_element_by_xpath('//*[@id="refine"]/div[2]/div[4]/div[2]/input').get_attribute('value').split('/')[-1]) >= 2019:
                browser.find_element_by_xpath('//*[@id="refine"]/div[2]/div[4]/div[2]/button').click()
                browser.find_element_by_xpath('//*[@id="selectyeartimeline"]').click()
                #for ele in browser.find_elements_by_xpath("//*[contains(text(), '2014')]"):
                for ele in browser.find_elements_by_xpath("//*[contains(text(), '"+endyear+"')]"):
                    try:
                        ele.click()
                        break
                    except:
                        pass
                browser.find_element_by_xpath('//*[@id="selectmonthtimeline"]').click()
                #for ele in browser.find_elements_by_xpath("//*[contains(text(), 'December')]"):
                for ele in browser.find_elements_by_xpath("//*[contains(text(), '"+endmonth+"')]"):
                    try:
                        ele.click()
                        break
                    except:
                        pass
                #browser.find_element_by_xpath('//*[@id="selectmonthtimeline"]').click()
                #browser.find_element_by_xpath('//*[@id="datepicker"]/h3/div[1]/ol/li[12]/button').click()
                browser.find_element_by_xpath('//*[@id="datepicker"]/table/tbody/tr[6]/td[2]/button').click()
            # click ok
            browser.find_element_by_xpath('//*[@id="refine"]/div[2]/div[4]/button').click()
            start_time = time.time()
            print("time range is set")
            # subject
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("setting subject conditions timeout")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="podfiltersbuttonsubject"]').click()
                    break
                except:
                    time.sleep(2)
            while True:
                try:
                    for ele in browser.find_elements_by_xpath("//*[contains(text(), 'Business News')]"):
                        try:
                            ele.click()
                            break
                        except:
                            pass
                    break
                except:
                    time.sleep(2)
            print("subject is set")

            #sort by time
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("sorting by time time out")
                    raise Exception()
                try:
                    browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[2]/li/div/button').click()
                    break
                except WebDriverException:
                    time.sleep(1)
            browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[2]/li/div/div/button[4]').click()
            #N_temp = how many articles eg: News (10,000+)
            start = time.time()
            while True:
                if time.time() - start > dead_time:
                    print("get number of articles time out")
                    raise Exception()
                try:
                    #N_temp = browser.find_element_by_xpath('//*[@id="content"]/header/h2/span').text
                    N_temp = browser.find_element_by_xpath('/html/body/main/div/main/div[2]/div/div[2]/div[2]/form/div[2]/nav/ol/li[6]/a').text
                    break
                except:
                    time.sleep(2)
            total_number = int(''.join(re.findall(r'[0-9]', N_temp)))
            print("we'll scrape down {} files related to '{}'".format(total_number, searchTerms))
            total_page = int(np.ceil(total_number/10))
            file_digit = len(str(total_page)) * 2 + 1
            for page in range(1, total_page + 1):
                time.sleep(2)
                date = browser.find_element_by_xpath('//*[@id="content"]/div[2]/form/div[2]/ol/li[1]/div/div[1]/dl/dd[4]/a').text
                month, year = date.split(',')
                month = month_d[month[:3]]
                new_folder = download_folder + r'/{}/{}{}'.format(searchTerms, month.strip(), year.strip())
                #new_folder = download_folder + r'\{}-{}\{}'.format( month.strip(), year.strip(),searchTerms)
                # =============================================================================
                #     If the file already exists. Go to next page.
                # =============================================================================
                if os.path.isfile(new_folder + '/'  + (str(page) + '_' + str(total_page)).zfill(file_digit) +  '.ZIP'):
                #if os.path.isfile(download_folder + '/'  + (str(page) + '_' + str(total_page)).zfill(file_digit) +  '.ZIP'):

                    print('exist: ' + str(page) + '_' + str(total_page) +  '.ZIP')
                    if page < total_page:
                        try:
                            start_time = time.time()
                            while True:
                                if time.time() - start_time > dead_time:
                                    raise Exception()
                                WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.LINK_TEXT , str(page + 1))))
                                browser.find_element_by_link_text(str(page + 1)).click()
                        except WebDriverException:
                            time.sleep(3)
                            continue
                # =============================================================================
                # Wait the all checkbox to be clickable
                # =============================================================================
                while True:
                    print("here")
                    try:
                        ele = browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[1]/input')
                        print(ele)
                        # if browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[1]/input').get_attribute('checked') != 'true':
                        #     browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[1]/input').click()
                        # print(ele.get_attribute('checked'))
                        # if not ele.get_attribute('checked'):
                        ele.click()
                        break
                    except WebDriverException:
                        time.sleep(1)
                # =============================================================================
                #   Wait the IncludeAttachments button to be clickable.  otherwise re-click download buttom
                # =============================================================================
                # try:
                #     start_time = time.time()
                #     while True:
                #         if time.time() - start_time > dead_time:
                #             raise Exception()
                #         elm = browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[4]/ul/li[3]/button')
                #         elm.click()
                # except WebDriverException:
                #     pass
                while True:
                    try:
                        browser.find_element_by_xpath('//*[@id="results-list-delivery-toolbar"]/div/ul[1]/li[4]/ul/li[3]/button').click()
                        break
                    except:
                        time.sleep(1)
                start_time = time.time()
                while True:
                    if time.time() - start_time > dead_time:
                        raise Exception()
                    try:
                        browser.find_element_by_xpath('//*[@id="DocumentsOnly"]').click()
                        break
                    except:
                        time.sleep(1)
                browser.find_element_by_xpath('//*[@id="IncludeAttachments"]').click()
                browser.find_element_by_xpath('//*[@id="Docx"]').click()
                browser.find_element_by_xpath('//*[@id="SeparateFiles"]').click()
                browser.find_element_by_xpath('//*[@id="FileName"]').clear()
                browser.find_element_by_xpath('//*[@id="FileName"]').send_keys((str(page) + '_' + str(total_page)).zfill(file_digit))
                # =============================================================================
                #     After downloading Close the pop up window. LexisNexis only allows 5 cocurrent windows
                # =============================================================================
                
                before = browser.window_handles[0]
                # browser.find_element_by_xpath('/html/body/aside/footer/ul/li[1]/input').click()
                browser.find_element_by_xpath('/html/body/aside/footer/div/button[1]').click()
                # print('here')
                start_time = time.time()
                while True:
                    try:
                        after = browser.window_handles[1]
                        break
                    except:
                        time.sleep(1)
                browser.switch_to.window(after)
                start_time = time.time()
                while True:
                    if time.time() - start_time > dead_time:
                        raise Exception()
                    if  browser.find_elements_by_link_text((str(page) + '_' + str(total_page)).zfill(file_digit)):
                        break
                
                ### CHECK DOWNLOAD COMPLETED BEFORE WE CLOSE DOWNLOAD WINDOW
                start_time = time.time()
                ### wait maximum 30s for download
                while time.time() - start_time < 30:
                    try:
                        if "Delivery Complete" in browser.find_element_by_xpath('/html/body/main/div/div[2]/section/h1').text:
                            print("-> Closing the Download Window...")
                            time.sleep(1)
                            break
                        else:
                            print("-> Waiting for Download to be complete...")
                        time.sleep(1)
                        
                    except Exception as e:
                        print("Exception @ waiting download to complete -->",e)
                        time.sleep(1)
                    finally:
                        time.sleep(1)
        
                        
                #time.sleep(100)
                
                browser.close()
                browser.switch_to.window(before)
                print(browser.title)
                time.sleep(2)
                old_folder = download_folder + r'/temp'
                os.chdir(old_folder)
                if not os.path.isdir(new_folder):
                    os.makedirs(new_folder)
                for f in os.listdir():
                    shutil.move(old_folder + r'/{}'.format(f), new_folder + r'/{}'.format(f))
                print('finishing page' + str(page) + '_' + str(total_page)  )
                # =============================================================================
                #     Go to the next page. Have to check the next page link is clickable
                # =============================================================================
                if page < total_page:
                    try:
                        browser.find_element_by_link_text(str(page + 1)).click()
                        start_time = time.time()
                        while True:
                            if time.time() - start_time > dead_time:
                                raise Exception()
                            browser.find_element_by_link_text(str(page + 1)).click()
                    except WebDriverException:
                        time.sleep(3)
                        pass
                else:
                    print('FINISHED!')
                    #sys.exit()
                    return 7
                # except Exception:
                #     print('restarting')
                #     continue
            print('Finished')
            return 7
            break
        except Exception as e:
            print("Main exception->",e)
            print(traceback.format_exc())
            print("restarting")


# In[5]:


### UTILITIES AND HELPERS



def unzip(download_folder):
    if not os.path.exists(download_folder + '/' + 'unzipped'):
        os.makedirs(download_folder + '/' + 'unzipped')
    for filename in os.listdir(download_folder):
        if not filename.endswith('.ZIP'):
            continue
        zip_ref = zipfile.ZipFile(download_folder +  '/' + filename, 'r')
        zip_ref.extractall(download_folder + '/' + 'unzipped')
        if len(zip_ref.namelist()) != 11:
            print('missing document at ' + filename)
        zip_ref.close()
        print('unzipping ' + filename)


def create_index(download_folder, searchTerms):
    def get_docx_text(path):
        WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
        PARA = WORD_NAMESPACE + 'p'
        TEXT = WORD_NAMESPACE + 't'
        """
        Take the path of a docx file as argument, return the text in unicode.
        """
        document = zipfile.ZipFile(path)
        xml_content = document.read('word/document.xml')
        document.close()
        tree = XML(xml_content)

        paragraphs = []
        for paragraph in tree.getiterator(PARA):
            texts = [node.text
                     for node in paragraph.getiterator(TEXT)
                     if node.text]
            if texts:
                paragraphs.append(''.join(texts))

        return '\n\n'.join(paragraphs)
    def get_docx_hyperlink(path):
        document = Document(path)
        rels = document.part.rels
        link = []
        for rel in rels:
            if rels[rel].reltype == RT.HYPERLINK:
                link.append(rels[rel]._target)
        return pd.Series(link)
    def find_between(s, first, last):
        list = []
        try:
            while True:
                try:
                    start = s.index( first ) + len( first )
                    end = s.index( last, start )
                    list.append( s[start:end])
                    s = s.replace(first + s[start:end] + last,'')
                except:
                    break
            return list
        except ValueError:
            return ""

    index = pd.DataFrame(({'Title':{},'Link':{}}))
    for filename in os.listdir(download_folder + '/' + 'unzipped'):
        if filename.find("doclist") == -1:
            continue
        text = get_docx_text(download_folder + '/' + 'unzipped/' + filename)
        link = get_docx_hyperlink(download_folder + '/' + 'unzipped/' + filename).loc[0]
        content = '<start>' + re.sub(r'.*Documents \(\d*\)', '',text.replace('\n',' ')).replace(              'Client/Matter: -None-  Search Terms: '+ searchTerms + '  Search Type: Terms and Connectors   Narrowed by:   Content Type  Narrowed by  News  -None-',              '<end><start>')
        content_list = pd.Series(find_between(content, '<start>', '<end>'))
        content_list = content_list.str[5:]
        index = index.append(pd.DataFrame({'Title':content_list,'Link':link}),ignore_index = True)
    index = index.reset_index()
    index['index'] = index.index + 1
    index.to_csv(download_folder + '/index.csv', index=False)
    return index


# In[6]:


### FIX AND SCRIPT SUPERVISOR HELPERS

import dateutil.parser


# SET CONFIG VARIABLES
__download_folder = os.path.join(root,"download")




def get_last_download_date(__searchterm):
    # check if folder exists
    if __searchterm in os.listdir(__download_folder):
        __folder_searchterm = os.path.join(__download_folder,__searchterm)

        already_downloaded = os.listdir(__folder_searchterm)

        if len(already_downloaded)==0:
            __enddate = __default_enddate

        else:

            # sort on datetime
            already_downloaded = sorted(already_downloaded, key=dateutil.parser.parse)


            latest = already_downloaded[0]


            # empty the latest folder
            __folder_latest = os.path.join(__folder_searchterm,latest)

            #crawl subdirs in side latest folder and delete
            for subfolder in os.listdir(__folder_latest):
                this_path = os.path.join(__folder_latest,subfolder)
                print("DELETING --->",this_path)
                if os.path.isdir(this_path):
                    shutil.rmtree(__folder_latest)
                else:
                    os.remove(this_path)




            __enddate = dateutil.parser.parse(latest).strftime("%B.%Y")

    else:
        __enddate = __default_enddate
        
    return __enddate



 


# In[ ]:


### MAIN


try:
    if "SEARCHTERM" in os.environ:
        searchTermsList = [os.environ["SEARCHTERM"]]
except Exception as e:
    print(e)
    print("Have you suppied ENVIRONMENT VAR -> SEARCHTERM")
    #exit(0)
    
    

if __name__ == "__main__":
    for searchTerms in searchTermsList:
        
        __enddate = get_last_download_date(searchTerms)
        
        if(__enddate==__default_enddate):
            print("\nSTARTING FULL DOWNLOAD TILL ---> %s\n\n" % __enddate )
        else:
            print("\nRESUMING TILL END DATE --> %s\n\n" % __enddate)
            
        

        val = download_file(searchTerms = searchTerms, download_folder = __download_folder, enddate=__enddate )
        
        ## SAVE PROGRESS IF FINISHED
        if val==7:
            with open("done.txt",'a+') as g:
                g.write(searchTerms+"\n")
        
    # unzip()
    # create_index()


# In[ ]:





# In[ ]:




