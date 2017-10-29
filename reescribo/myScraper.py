#! /usr/bin/python3
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

MAX_URLS = 20 #absolute maximum of urls to scrape
MID_URLS = 15 # if theres 1 contact found, stop after this amount of links

# Setting Logger Up
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#file handler
handler = logging.FileHandler('test.log')
handler.setLevel(logging.DEBUG)
#logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)







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
                # print("Theres nothing left prbly. Moving on...")
                logger.warn("Searched %d links. Theres nothing left prbly. Moving on...", MID_URLS)
                break;

            if len(processed_urls) > MAX_URLS:
                logger.warn("Searched %d links and nothing was found! Moving on...", MAX_URLS)
                break;


        new_url = new_urls.popleft()
        processed_urls.add(new_url)



        # get url's content
        print("Processing %s" % new_url)
        logger.info("Processing %s", new_url)

        response = requests.get(new_url)
        try:
            response.raise_for_status()
        except Exception as axc:
            logger.error('There was a problem processing %s', new_url)
            logger.error('Failed to open website', exc_info=True)
            continue

        # extract all email addresses and add them into the resulting set


        # TODO: falta parsear los mailto CREO

        emailRegex = re.compile(r'''
            [a-zA-Z0-9._%+-]+ #userName
            @
            [a-zA-Z0-9._%+-]+ #domainName
            \.[a-zA-z]{2,4} #dot-something
            ''', re.VERBOSE|re.I)

        new_emails = set(re.findall(emailRegex, response.text))
        emails.update(new_emails)

        # print("MAIL found: %s" % new_emails)
        logger.info("!!!!!!!!!!!!!!!!!!MAIL found: %s", new_emails)

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, "html.parser")

        # # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            if foundEverything(emails, fbs, tws):
                logger.info("found everything! Moving on...")
                break
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            logger.debug("New link found: %s", link)
            # resolve relative links

            if "facebook" in link:
                logger.info("FB found: %s", link)
                fbs.update([link])
                continue

            elif "twitter" in link:
                logger.info("TW found: %s", link)
                tws.update([link])
                continue

            elif "pdf" in link:
                logger.debug("ignored as pdf")
                continue

            # elif "mailto" in link:

            elif isImage(link):
                logger.debug("ignored as media or blog")
                continue

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




    # fileIn = 'clinic in Miami-2017-Oct-20 12:54:47.csv'
    # # csvFileIn = open('../restaurants in  miami.csv', 'r')
    # csvFileIn = open(fileIn, 'r')
    url = 'https://www.miamiculinarytours.com'
    name = 'MCT'
    fileOut = 'emails for ' + name + '.csv'
    csvFileOut = open(fileOut, 'w')
    #
    # reader = csv.DictReader(csvFileIn)
    fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    writer.writeheader()
    #
    # for row in reader:
    #     scrapeWebsite(writer, row['URL'], row['name'])
    #
    # csvFileOut.close()
    # csvFileIn.close()
    # subirAlDrive.main(fileOut, fileOut, fileOut, 'email')
    # print("ALL DONE")

    scrapeWebsite(writer, url, name)
    csvFileOut.close()


if __name__ == "__main__":
    main()
