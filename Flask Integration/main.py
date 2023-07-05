from bs4 import BeautifulSoup as bs
import os
import pagedeleter as pd
import filedownloader as fd
import logging
logging.basicConfig(filename="scrapper.log", level=logging.INFO)

def wholeReviewProcess(searchString):
    amazon_url = "https://www.amazon.in/s?k=" + searchString
    download_folder = 'C:\\Users\\KIIT\\Documents\\PYTHON\\WEB SCRAPPING\\savedWEBpages\\'
    download_temp_folder = 'C:\\Users\\KIIT\\Documents\\PYTHON\\WEB SCRAPPING\\savedResultpages\\'

    pd.deletepage(download_folder)

    if (len(os.listdir(download_folder)) == 0):
        fd.downloadWebpage(amazon_url, download_folder)

    amazon_page = os.listdir(download_folder)
    amazon_html = download_folder + amazon_page[0]

    with open (amazon_html, 'r', encoding="utf8") as f:
        html_content = f.read()
    f.close()

    soup = bs(html_content, 'html.parser')

    bigbox = soup.find("div", {"data-component-type":"s-search-result"})

    product_link_list = []
    prod_name = ""
    m = 1
    for i in bigbox:
        try:
            for j in i.find("span", class_ = "a-size-medium a-color-base a-text-normal"):
                # print("Prod Name: "+ j.text)
                prod_name = j.text
        except Exception as e:
            logging.info(e)
        j = i.find('a')
        try:
            if 'href' in j.attrs:
                url = j.get('href')
                # print(m ,"------> : ", "https://www.amazon.in"+url)
                # m = m + 1
                product_link_list.append("https://www.amazon.in"+url)
        except Exception as e:
            logging.info(e)
            return "Something is wrong"
            

    name = ""
    rating = ""
    title = ""
    review = ""
    reviews = []
        
    for index, product_link in enumerate(product_link_list):
        pd.deletepage(download_temp_folder)

        print(index ,"------> : ", product_link)
        if (len(os.listdir(download_temp_folder)) == 0):
            fd.downloadWebpage(product_link, download_temp_folder)
            

        product_page = os.listdir(download_temp_folder)
        product_html = download_temp_folder + product_page[0]

        with open (product_html, 'r', encoding="utf8") as f:
            html_content = f.read()
        f.close()

        product_soup = bs(html_content, 'html.parser')

        commentbox = product_soup.findAll("div", {"class":"a-section review aok-relative"})

        for i in commentbox:
            try:
                for j in i.find_all("span", class_ = "a-profile-name"):
                    # print("Name: "+ j.text)
                    name = j.text

                for j in i.find_all("a", class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"):
                    for k in j.find("span", class_ = "a-icon-alt"):
                        # print("Ratings: "+ k.text)
                        rating = k.text

                    for k in j.find("span", class_ = None):
                        # print("Title: "+ k.text)
                        title = k.text

                for j in i.find_all("div", class_ = "a-expander-content reviewText review-text-content a-expander-partial-collapse-content"):
                    # print("Review: "+ j.text)
                    review = j.text

                # print("\n")
                mydict = {"product":prod_name, "prod_link":product_link, "reviewer_name":name, "rating":rating, "title":title, "review":review}
                reviews.append(mydict)
                logging.info("log my final result {}".format(reviews))
            except Exception as e:
                logging.info(e)
    try:
        a = pd.deletepage(download_folder)
        b = pd.deletepage(download_temp_folder)
        logging.info(a + "\n" + b)
    except Exception as e:
        logging.info(e)
    return(reviews)
    