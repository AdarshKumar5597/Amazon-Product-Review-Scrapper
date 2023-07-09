from selenium import webdriver
import codecs
import os
from selenium.webdriver.chrome.service import Service
import subprocess
import requests
import hashlib
import datetime

def downloadWebpage(url, download_folder):
    """
    Function to download a webpage and save it to a file.

    Parameters:
    - url: The URL of the webpage to download.
    - download_folder: The folder where the downloaded file will be saved.

    Returns:
    - output_file: The path of the downloaded file.
    """
    if not download_folder:
        download_folder = os.path.join(os.path.abspath(os.getcwd()), "webScrapping", "savedResultPages")

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)

    output_file = os.path.join(download_folder, generate_unique_hash(url))

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
    n=os.path.join(download_folder,output_file)
    #open file in write mode with encoding
    f = codecs.open(n, "w", "utf-8")
    #obtain page source
    h = driver.page_source
    #write page source content to file
    f.write(h)
    #close browser
    driver.quit()

    return output_file

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


def generate_unique_hash(text):
    """
    Function to generate a unique hash based on the given text and current time.

    Parameters:
    - text: The input text to generate the hash from.

    Returns:
    - unique_hash: The generated unique hash.
    """

    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")  # Format current time as a string
    input_data = f"{text}{current_time}"  # Concatenate the string and current time
    unique_hash = hashlib.md5(input_data.encode()).hexdigest()  # Generate MD5 hash

    return unique_hash

def download_webpage(url, download_folder=""):
    """
    Function to download a webpage from the given URL and save it in the specified download folder.

    Parameters:
    - url: The URL of the webpage to download.
    - download_folder (optional): The folder to save the downloaded webpage. If not provided, a default folder will be used.

    Returns:
    - output_file: The path of the downloaded webpage file.
    """
    if not download_folder:
        download_folder = os.path.join(os.path.abspath(os.getcwd()), "webScrapping", "savedResultPages")

    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)

    output_file = os.path.join(download_folder, generate_unique_hash(url))

    try:
        current_os = os.name
        if current_os == 'nt':
            print("Operating system: Windows")
            result = subprocess.run(["Start-BitsTransfer", "-Source", download_webpage, "-Destination", os.path.join(download_folder, output_file)], capture_output=True, text=True, check=True)
        elif current_os == 'posix':
            print("Operating system: Unix/Linux")
            result = subprocess.run(["wget", "-P", download_folder, url, "-O", output_file], capture_output=True, text=True, check=True)
        # elif current_os == 'java':
        #     print("Operating system: Java")
        else:
            print("Unknown operating system\nUsing selenium")


        
        print("Webpage downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print("Failed to download webpage.")
        print("Error:", e.stderr)

    return output_file