import sys
sys.path.append("/Users/yixuanwang/Desktop/PipeIQ/website_vectordb_query")
from website_vectordb_query.upload_s3 import *
from website_vectordb_query.main_functions import *
from urllib.parse import urlparse
from constants import *
import undetected_chromedriver as uc
import os

downloadpath = "/Users/yixuanwang/Downloads"

def main():
    pdf_upload_test()


def add_sage_to_pinecone():
    website_to_vectordb_storage(full_url=sage_url, index_name=index_name, namespace="sage")


def add_egnyte_to_pinecone_namespace():
    website_to_vectordb_storage(full_url=egnyte_url, index_name=index_name, namespace="egnyte")

def snowflake_to_pinecone():
    website_to_vectordb_storage(full_url=snowflake_url, index_name=index_name, namespace="snowflake",
                                openai_key=openai_key, limit=10)


def email_sage_solutions_msg3_pinecone():
    url = sage_url
    system_msg = email_system_msg_sage
    query = sage_solutions_query
    augmented_query = create_augmented_query_vectordb(index_name=index_name, namespace="sage", query=query, openai_key=openai_key)
    print(augmented_query)
    test_augmented_query(augmented_query, system_msg, openai_key)


def email_sage_solutions_msg3_local():
    url = sage_url
    system_msg = email_system_msg_sage
    query = sage_solutions_query
    domain = urlparse(url).netloc
    augmented_query = create_augmented_query_local(domain, query)
    test_augmented_query(augmented_query, system_msg)


def email_egnyte_pricing_msg2_local():
    url = egnyte_url
    system_msg = email_system_msg_egnyte
    query = egnyte_pricing_query
    domain = urlparse(url).netloc
    augmented_query = create_augmented_query_local(domain, query)
    test_augmented_query(augmented_query, system_msg)


def email_egnyte_pricing_msg1_pinecone():
    query = egnyte_pricing_query

    system_msg = email_ai_assistant_system_msg

    augmented_query = create_augmented_query_vectordb(index_name, "egnyte", query, openai_key)
    print(augmented_query)
    response = test_augmented_query(augmented_query, system_msg, openai_key)
    print(response)


def email_egnyte_pricing_msg2_pinecone():
    query = egnyte_pricing_query

    system_msg = email_system_msg_egnyte

    namespace = "egnyte"

    augmented_query = create_augmented_query_vectordb(index_name, namespace, query, openai_key)
    print(test_augmented_query(augmented_query, system_msg, openai_key))

def sage_pdf_test():
    #url = "https://www.sage.com/en-us/"
    url = "https://www.sage.com/en-us/-/media/files/sagedotcom/master/documents/pdf/legal/global-hr-privacy-notice-en.pdf"
    crawl(url, downloadpath)
    #website_to_vectordb_storage(url, "websites", downloadpath, "sage", limit=300)

def egnyte_pdf_test():
    url = "https://www.egnyte.com/resource-center? category=ebook"
    url = "https://pages.egnyte.com/rs/038-PTQ-391/images/%5Bebook%5DEgnyte%20for%20AEC.pdf"
    crawl(url, downloadpath)
    domain = "www.egnyte.com"
    #read_pdf_from_download("/Users/saigopinath/Downloads/2022-SANS-Protects-FileStorage.pdf")
    #hyperlinks = get_domain_hyperlinks(domain, url, driver)
    #hyperlinks = get_domain_hyperlinks(domain, url, driver)
    #for h in hyperlinks:
        #print(h)

def pdf_upload_test():
    file_name = 'Report-Cybersecurity-Trends-for-Mid-Sized-Organizations.pdf'
    bucket_name = 'pipeiq-pdfs'
    s3_file_path = 'Report-Cybersecurity-Trends-for-Mid-Sized-Organizations.pdf'
    upload_to_s3(file_name, bucket_name, s3_file_path)

if __name__ == '__main__':
    main()

