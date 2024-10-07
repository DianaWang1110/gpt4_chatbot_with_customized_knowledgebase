import os
import time
from collections import deque
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.remote.webdriver import By
from website_vectordb_query.constants import *




# Fetch the potential hyperlinks for get_hyperlinks
def elements_fetcher(driver):
    elems = driver.find_elements(By.TAG_NAME, 'a')
    if elems:
        return elems
    else:
        return False


# Function to get the hyperlinks from a URL
def get_hyperlinks(url, driver):
    hyperlinks = []
    driver.get(url)
    if "pdf" in url:
        return []
    try:
        elems = WebDriverWait(driver, 60).until(elements_fetcher)
    except:
        print("timeout exception on url " + url)
        return []

    for elem in elems:
        try:
            href = elem.get_attribute('href')
            if href is not None:
                # print(href)
                hyperlinks.append(href)
        except:
            continue
    return hyperlinks

"""
    pdfFileObj = open(new_path, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    pages = pdfReader.pages
    for page in pages:
        text = page.extract_text()
    pdfFileObj.close()
    print(text)
    return text"""


# Parse hyperlinks to ensure they are within the same domain and not blacklisted (image files, blog posts, etc)
def get_domain_hyperlinks(local_domain, url, driver):
    clean_links = []
    for link in set(get_hyperlinks(url, driver)):
        clean_link = None

        """
        # If the link is a URL, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # Parse the URL and check if the domain is the same
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link"""

        company_name = local_domain[4:-4]
        if company_name in url:
            clean_link = link
        # If the link is not a URL, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            # Check if the link contains any of the blacklist words
            # Currently hardcoded for sage to have only english links, need to broaden for other websites somehow
            flag = [word for word in BLACKLIST if (word in clean_link)]
            if not flag:
                if "sage" in clean_link and "en-us" not in clean_link:
                    continue
                clean_links.append(clean_link)

    # Return the list of hyperlinks that are within the same domain
    return list(set(clean_links))


# Get the top limit urls and store as text locally. Limit defaults to 100
def crawl(url, limit=LIMIT, driver=None):
    # Counter for capping to limit
    counter = 0
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    # Create a queue to store the URLs to crawl
    queue = deque([url])

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = set([url])

    if driver is None:
        # Set up driver to read links - headless option ensures links will not be opened locally
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('headless')
        driver = uc.Chrome(options=options)
    driver.implicitly_wait(30)

    # Create a directory to store the text files
    if not os.path.exists("./text/"):
        os.mkdir("./text/")

    if not os.path.exists("./text/" + local_domain + "/"):
        os.mkdir("./text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("./processed"):
        os.mkdir("./processed")

    # While the queue is not empty, continue crawling
    while queue and counter < limit:
        # Get the next URL from the queue - popleft to get the urls that were added first to ensure importance
        url = queue.popleft()
        print(url)  # for debugging and to see the progress

        write_path = './text/' + local_domain + '/' + url[8:].replace("/", "_") + ".txt"

        # Save text from the url to a <url>.txt file
        with open(write_path, "w") as f:
            # Get the full text from url
            driver.get(url)
            text = driver.find_element(By.TAG_NAME, "html").text

            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if ("You need to enable JavaScript to run this app." in text):
                print("Unable to parse page " + url + " due to JavaScript being required")

            # Otherwise, write the text to the file in the text directory
            f.write(text)

            # Get the hyperlinks from the URL and add them to the queue
            for link in get_domain_hyperlinks(local_domain, url, driver):
                if link not in seen:
                    queue.append(link)
                    seen.add(link)
        counter += 1


