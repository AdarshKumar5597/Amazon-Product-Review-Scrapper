from selenium import webdriver
import codecs
import os
from selenium.webdriver.chrome.service import Service



def downloadWebpage(url, download_folder):
    options = webdriver.ChromeOptions()
    # set chromedriver.exe path
    service = Service(executable_path='C:\Program Files\Chrome Driver\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)
    # driver.implicitly_wait(0.5)
    #maximize browser
    # driver.maximize_window()
    #launch URL
    driver.get(url)
    #get file path to save page
    n=os.path.join(download_folder,"Page.html")
    #open file in write mode with encoding
    f = codecs.open(n, "w", "utf-8")
    #obtain page source
    h = driver.page_source
    #write page source content to file
    f.write(h)
    #close browser
    driver.quit()
