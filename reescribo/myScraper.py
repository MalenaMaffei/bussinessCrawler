#! /usr/bin/python36
from selenium import webdriver

from collections import deque
import re
import csv

import subirAlDrive
from soup import Soup
from request import Request
from logger import Logger
from linkFinder import LinkFinder

MAX_URLS = 14 #absolute maximum of urls to scrape
MID_URLS = 7 # if theres 1 contact found, stop after this amount of links


logger = Logger.Instance()

browser = webdriver.Firefox()


def theBigGuns(url, emails):
    browser.get(url)
    source = browser.page_source
    findEmail(source, emails)


def reCheck(urls, emails):
    for url in urls:
        theBigGuns(url, emails)
        if len(emails) > 0:
            return
    logger.info("big guns couldn't find anything :(")


def findEmail(text, emails):
    emailRegex = re.compile(r'''
        [a-zA-Z0-9._%+-]+ #userName
        @
        [a-zA-Z0-9._%+-]+ #domainName
        \.[a-zA-z]{2,4} #dot-something
        ''', re.VERBOSE | re.I)

    new_emails = set(re.findall(emailRegex, text))
    new_emails = set(filter(lambda x: ".png" not in x and ".jpg" not in x, new_emails))

    if len(new_emails) != 0:
        logger.info(f"BG!!!!!!!!!!!!!!!!!!MAIL found: {new_emails}")
        emails.update(new_emails)



def scrapeWebsite(writer, url, name):
    new_urls = deque([url])

    linkFinder = LinkFinder(url)

    # parts = urlsplit(url)
    # base_url = "{0.scheme}://{0.netloc}".format(parts)
    # path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # logger.info(f'Handling baseurl: {base_url}, path: {path}')

    # a set of urls that we have already crawled
    # processed_urls = set()

    # a set of crawled emails
    emails = set()



    while linkFinder.still_urls():
        # move next url from the queue to the set of processed urls

        if found_everything(emails, linkFinder):
            logger.info("found everything! Moving on...")
            break

        if linkFinder.processed() >= MID_URLS and len(emails) > 0:
            logger.warn(f"Searched {MID_URLS}, not all social media was found but we have mail. Moving on...")
            break

        if linkFinder.processed() >= MAX_URLS and len(emails) == 0:
            # logger.warn(f"Searched {MAX_URLS} links and no email was found! Bringing in the big guns...")
            logger.warn(f"Searched {MAX_URLS} links and no email was found! Moving on...")
            # reCheck(linkFinder.processed_urls, emails)
            break;


        new_url = linkFinder.next_url()

        # get url's content
        logger.info(f"Processing {new_url}")

        # try:
        #     html = Request().getSource(new_url)
        # except Exception:
        #     logger.error(f'There was a problem processing {new_url}')
        #     continue

        try:
            browser.get(new_url)
            html = browser.page_source
        except Exception:
            logger.error(f'There was a problem processing {new_url}')
            continue

        findEmail(html, emails)

        soup = Soup(html)
        links = soup.getLinks()

        # print(links)
        #
        # print(html)
        #
        # if(len(links) == 0):
        #     browser.get(new_url)
        #     source = browser.page_source
        #     soup = Soup(source)
        #     links = soup.getLinks()

        linkFinder.parse(links)


    # if len(emails) == 0 and linkFinder.processed() < MAX_URLS:
    #     reCheck(linkFinder.processed_urls, emails)



    data = {'name': name, 'URL': url, 'emails': ' '.join(emails), 'facebook': ' '.join(linkFinder.get_fbs()), 'twitter': ' '.join(linkFinder.get_tws())}
    writer.writerow(data)


def found_everything(emails, linkFinder):
    if len(emails) > 0 and linkFinder.found_everything():
        return True


def amount_found(emails, fbs, tws):
    i = 0
    if len(emails) > 0:
        i += 1
    if len(fbs) > 0:
        i += 1
    if len(tws) > 0:
        i += 1

    return i


def main():

    #MODO UNA SOLA PAGINA
    # url = 'http://www.midtowndentalmiami.com/'
    # name = 'midtowndentalmiami'
    # fileOut = 'emails for ' + name + '.csv'
    # csvFileOut = open(fileOut, 'w')
    # fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    # writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    # writer.writeheader()
    # logger.info(f"Scraping: {url}")
    # scrapeWebsite(writer, url, name)
    # csvFileOut.close()
    # logger.info("ALL DONE")
    # csvFileOut.close()

    fileIn = 'Marketing agency in Miami-2017-Oct-31 14_56_15.csv'
    csvFileIn = open(fileIn, 'r')
    fileOut = 'emails for ' + fileIn
    csvFileOut = open(fileOut, 'w')
    #
    reader = csv.DictReader(csvFileIn)
    fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    writer.writeheader()

    # cant_rows = len(list(reader))
    # csvFileIn.seek(1)
    # logger.info(f"There are {cant_rows} websites.")

    logger.info(f"#######################{fileIn}########################")

    i = 1
    for row in reader:
        logger.info(f"#######################[ {i} ]Scraping : {row['URL']}#######################")
        scrapeWebsite(writer, row['URL'], row['name'])
        i += 1

    csvFileOut.close()
    csvFileIn.close()
    subirAlDrive.main(fileOut, fileOut, fileOut, 'email')
    logger.info("ALL DONE")


    csvFileOut.close()


if __name__ == "__main__":
    main()
