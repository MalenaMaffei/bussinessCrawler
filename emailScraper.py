from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import csv
import sys

import subirAlDrive


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

    print("baseurl: " + base_url + "path: " + path)

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()
    fbs = set()
    tws = set()


    while len(new_urls):
        # move next url from the queue to the set of processed urls

        if foundEverything(emails, fbs, tws):
            print("found everything! Moving on...")
            break

        if len(processed_urls) > 10:
            if(amountFound(emails, fbs, tws) > 1):
                print("Theres nothing left prbly. Moving on...")
                break;

            if len(processed_urls) > 20:
                print("it's been too long! Moving on...")
                break;


        new_url = new_urls.popleft()
        processed_urls.add(new_url)



        # get url's content
        print("Processing %s" % new_url)
        try:
            response = requests.get(new_url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors
            continue

        # extract all email addresses and add them into the resulting set
        # print("response.text: %s\n" % response.text)

        # TODO: falta parsear los mailto
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)
        print("MAIL found: %s" % new_emails)

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, "html.parser")
        # print("soup: \n %s" % soup)
        # # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # print("LINK: %s" % link)
            # resolve relative links

            if "facebook" in link:
                print("FB found")
                fbs.update([link])
                continue

            elif "twitter" in link:
                print("TW found")
                tws.update([link])
                continue

            elif "pdf" in link:
                # print("PDF found")
                print("ignored: %s" % link)
                continue

            # elif "mailto" in link:

            elif isImage(link):
                print("ignored: %s" % link)
                continue

            elif link.startswith('/'):
                # print("link found: %s" % link)
                link = base_url + link
                # print("link startswith / now is: %s" % link)

            elif link.startswith('#'):
                # print("ignored: %s" % link)
                continue



            elif not link.startswith('http'):
                # print("link found: %s" % link)
                # print("path is: %s" % path)
                link = path + link

                # if not link.startswith('/'):
                #     link = path + '/' + link
                # else:
                #     link = path + link
                # print("link not startswith http is now: %s" % link)

            elif link.startswith('http') and base_url in link:
                link = link

            else:
                continue

            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in new_urls and not link in processed_urls:
                new_urls.append(link)
                # print("New Link added: %s" % link)



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

    fileIn = 'bar in Miami-2017-Oct-09 21:53:37.csv'
    # csvFileIn = open('../restaurants in  miami.csv', 'r')
    csvFileIn = open(fileIn, 'r')
    fileOut = 'emails for ' + fileIn
    csvFileOut = open(fileOut, 'w')

    reader = csv.DictReader(csvFileIn)
    fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        scrapeWebsite(writer, row['URL'], row['name'])

    csvFileOut.close()
    csvFileIn.close()
    subirAlDrive.main(fileOut, fileOut, fileOut, 'email')
    print("ALL DONE")


if __name__ == "__main__":
    main()
