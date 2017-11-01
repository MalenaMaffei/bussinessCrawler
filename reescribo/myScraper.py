#! /usr/bin/python36
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import csv
import sys
import logging
# import subirAlDrive
from soup import Soup
from request import Request
from logger import Logger

MAX_URLS = 15 #absolute maximum of urls to scrape
MID_URLS = 10 # if theres 1 contact found, stop after this amount of links
#
# Setting Logger Up
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#file handler
handler = logging.FileHandler('test.log')
handler.setLevel(logging.DEBUG)
#logging format
formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

#stream handler
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

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


def findEmail(text, emails):
    emailRegex = re.compile(r'''
        [a-zA-Z0-9._%+-]+ #userName
        @
        [a-zA-Z0-9._%+-]+ #domainName
        \.[a-zA-z]{2,4} #dot-something
        ''', re.VERBOSE|re.I)

    new_emails = set(re.findall(emailRegex, text))

    if len(new_emails) != 0:
        logger.info("BG!!!!!!!!!!!!!!!!!!MAIL found: %s", new_emails)
        emails.update(new_emails)


def isImage(link):
    png = "png" in link
    jpeg = "jpeg" in link
    jpg = "jpg" in link
    gif = "gif" in link
    mp4 = "mp4" in link
    blog = "blog" in link
    return(png or jpeg or jpg or gif or mp4 or blog)

def scrapeWebsite(writer, url, name):
    new_urls = deque([url])

    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    logger.info('Handling baseurl: %s, path: %s', base_url, path)
    # print("baseurl: " + base_url + "path: " + path)

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()
    fbs = set()
    tws = set()


    while len(new_urls):
        # move next url from the queue to the set of processed urls

        if foundEverything(emails, fbs, tws):
            logger.info("found everything! Moving on...")
            break

        if len(processed_urls) > MID_URLS:
            if(amountFound(emails, fbs, tws) > 1):
                logger.warning("Searched %d links. Theres nothing left prbly. Moving on...", MID_URLS)
                reCheck(processed_urls, emails)
                break;

            if len(processed_urls) > MAX_URLS:
                logger.warning("Searched %d links and nothing was found! Moving on...", MAX_URLS)
                reCheck(processed_urls, emails)
                break;


        new_url = new_urls.popleft()
        processed_urls.add(new_url)



        # get url's content
        logger.info("Processing %s", new_url)


        try:
            html = Request().getSource(new_url)
        except Exception as axc:
            logger.error('There was a problem processing %s', new_url)
            logger.error('Failed to open website', exc_info=True)
            continue



        emailRegex = re.compile(r'''
            [a-zA-Z0-9._%+-]+ #userName
            @
            [a-zA-Z0-9._%+-]+ #domainName
            \.[a-zA-z]{2,4} #dot-something
            ''', re.VERBOSE|re.I)

        new_emails = set(re.findall(emailRegex, html))

        if len(new_emails) != 0:
            logger.info("!!!!!!!!!!!!!!!!!!MAIL found: %s", new_emails)
            emails.update(new_emails)



        soup = Soup(html)
        links = soup.getLinks()



        for link in links:
            if foundEverything(emails, fbs, tws):
                logger.info("found everything! Moving on...")
                break
            logger.debug("New link found: %s", link)



            if "facebook" in link:
                logger.info("FB found: %s", link)
                fbs.update([link])
                continue
            #
            elif "twitter" in link:
                logger.info("TW found: %s", link)
                tws.update([link])
                continue

            elif "pdf" in link:
                logger.debug("ignored as pdf")
                continue



            elif isImage(link) or "javascript" in link:
                logger.debug("ignored as media or blog")
                continue
            #
            elif link.startswith('/'):
                link = base_url + link
                logger.debug("link startswith / now is: %s", link)

            elif link.startswith('#'):
                logger.debug("link startswith # was ignored")
                continue


            elif not link.startswith('http'):
                link = path + link
                logger.debug("As link did not start with http was changed to: %s", link)


            elif link.startswith('http') and base_url in link:
                logger.debug("Link did start with http")
                link = link

            else:
                logger.debug("None of the conditions were met, link was from outside")
                continue

            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in new_urls and not link in processed_urls:
                new_urls.append(link)
                logger.debug("New Link added as was not in processed or new")




    data = {'name': name, 'URL': url, 'emails': ' '.join(emails), 'facebook': ' '.join(fbs), 'twitter': ' '.join(tws)}
    writer.writerow(data)



def foundEverything(emails, fbs, tws):
    if(len(emails) > 0 and len(fbs) > 0 and len(tws) > 0):
        return True

def amountFound(emails, fbs, tws):
    i = 0
    if(len(emails) > 0):
        i+=1
    if(len(fbs)>0):
        i+=1
    if(len(tws)>0):
        i+=1

    return i

def main():

    #MODO UNA SOLA PAGINA
    url = 'http://www.creatohairdressing.com/'
    name = 'creatohairdressing'
    fileOut = 'emails for ' + name + '.csv'
    csvFileOut = open(fileOut, 'w')
    fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    writer.writeheader()
    logger.info("Scraping: %s", url)
    scrapeWebsite(writer, url, name)
    csvFileOut.close()
    logger.info("ALL DONE")
    csvFileOut.close()



    # fileIn = 'hairdresser in Miami-2017-Oct-09.csv'
    # csvFileIn = open(fileIn, 'r')
    # fileOut = 'emails for ' + fileIn
    # csvFileOut = open(fileOut, 'w')
    # #
    # reader = csv.DictReader(csvFileIn)
    # fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    # writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    # writer.writeheader()
    #
    # for row in reader:
    #     logger.info("Scraping: %s", row['URL'])
    #     scrapeWebsite(writer, row['URL'], row['name'])
    #
    # csvFileOut.close()
    # csvFileIn.close()
    # subirAlDrive.main(fileOut, fileOut, fileOut, 'email')
    # logger.info("ALL DONE")
    #
    #
    # csvFileOut.close()


if __name__ == "__main__":
    main()
