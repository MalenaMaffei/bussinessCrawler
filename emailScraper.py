from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import csv
import sys
# from googlemaps import GoogleMaps

# a queue of urls to be crawled
# new_urls = deque(['http://www.midtowndentalmiami.com'])
# new_urls = deque([sys.argv[1]])


# extract base url to resolve relative links
# url = sys.argv[1]
# # processed_urls.add(url)
# parts = urlsplit(url)
# base_url = "{0.scheme}://{0.netloc}".format(parts)
# path = url[:url.rfind('/')+1] if '/' in parts.path else url
#
# # a set of urls that we have already crawled
# processed_urls = set()
#
# # a set of crawled emails
# emails = set()
# fbs = set()
# tws = set()
# instas = set()
# pins = set()
# process urls one by one until we exhaust the queue
# csvFile = open('prueba.csv', 'w')
# fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter', 'instagram', 'pinterest']
# writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
# writer.writeheader()
# for row in reader
# print row

def isImage(link):
    png = "png" in link
    jpeg = "jpeg" in link
    jpg = "jpg" in link
    gif = "gif" in link
    return(png or jpeg or jpg or gif)

def scrapeWebsite(writer, url, name):
    new_urls = deque([url])

    parts = urlsplit(url)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()
    fbs = set()
    tws = set()
    # instas = set()
    # pins = set()

    while len(new_urls):
        # move next url from the queue to the set of processed urls

        if foundEverything(emails, fbs, tws):
            print("found everything! Moving on...")
            break

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

            # elif "png" in link or "jpg" in link:
            #     # print("PDF found")
            #     print("ignored: %s" % link)
            #     continue
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

            else:
                continue

            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in new_urls and not link in processed_urls:
                new_urls.append(link)
                # print("New Link added: %s" % link)

    data = {'name': name, 'URL': url, 'emails': ' '.join(emails), 'facebook': ' '.join(fbs), 'twitter': ' '.join(tws)}
    writer.writerow(data)



# data = {'name': 'holi','URL': sys.argv[1], 'emails': ' '.join(emails), 'facebook': ' '.join(fbs), 'twitter': ' '.join(tws), 'instagram': ' '.join(instas), 'pinterest': ' '.join(pins)}
# writer.writerow(data)
# csvFile.close()

def foundEverything(emails, fbs, tws):
    if(len(emails) > 0 and len(fbs) > 0 and len(tws) > 0):
        return True

def main():
    csvFileOut = open('prueba.csv', 'w')
    csvFileIn = open('../restaurants in  miami.csv', 'r')
    reader = csv.DictReader(csvFileIn)
    fieldnames = ['name', 'URL', 'emails', 'facebook', 'twitter']
    writer = csv.DictWriter(csvFileOut, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
    #     # print(row['first_name'], row['last_name'])
        scrapeWebsite(writer, row['URL'], row['name'])

    # scrapeWebsite(writer, 'http://www.acpediatricdentistry.com/', "ACP")
    csvFileOut.close()
    csvFileIn.close()

if __name__ == "__main__":
    main()
