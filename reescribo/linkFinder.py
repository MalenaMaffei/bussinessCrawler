from urllib.parse import urlsplit
from logger import Logger
from collections import deque
import re


class LinkFinder:
    def __init__(self, url):
        parts = urlsplit(url)
        self.base_url = "{0.scheme}://{0.netloc}".format(parts)
        self.path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        self.fbs = set()
        self.tws = set()
        self.new_urls = deque([url])
        self.processed_urls = set()

        regex = re.compile(r"https?://(www\.)?([^.]+\.[^/]+)", re.I)
        self.name = re.findall(regex, url)[-1][-1]





        Logger.Instance().info(f'Handling name: {self.name}, baseurl: {self.base_url}, path: {self.path}')

    def parse(self, links):
        logger = Logger.Instance()

        for link in links:
            if self.found_everything():
                # logger.info("found everything! Moving on...")
                break
            logger.debug(f"New link found: {link}")

            if "facebook" in link:
                logger.info(f"FB found: {link}")
                self.fbs.update([link])
                continue
            #
            elif "twitter" in link:
                logger.info(f"TW found: {link}")
                self.tws.update([link])
                continue

            elif "pdf" in link:
                logger.debug("ignored as pdf")
                continue

            elif self.isImage(link) or "javascript" in link:
                logger.debug("ignored as media or blog")
                continue
            #
            elif link.startswith('/'):
                link = self.base_url + link
                logger.debug(f"link startswith / now is: {link}")

            elif link.startswith('#'):
                logger.debug("link startswith # was ignored")
                continue

            elif not link.startswith('http'):
                link = self.path + link
                logger.debug(f"As link did not start with http was changed to: {link}")

            elif link.startswith('http') and self.name in link:
                logger.debug("Link did start with http")
                link = link

            else:
                logger.debug("None of the conditions were met, link was from outside")
                continue

            # add the new url to the queue if it was not enqueued nor processed yet
            if not link in self.new_urls and not link in self.processed_urls:
                if "contact" in link:
                    self.new_urls.insert(0, link)
                    logger.info(f"Link with 'contact' added to start of link queue: {link}")
                else:
                    self.new_urls.append(link)
                logger.debug("New Link added as was not in processed or new")



    def still_urls(self):
        return len(self.new_urls) != 0

    def next_url(self):
        new_url = self.new_urls.popleft()
        self.processed_urls.add(new_url)
        return new_url

    def isImage(self, link):
        png = "png" in link
        jpeg = "jpeg" in link
        jpg = "jpg" in link
        gif = "gif" in link
        mp4 = "mp4" in link
        blog = "blog" in link
        tel = "tel:" in link
        mail = "mailto:" in link
        return png or jpeg or jpg or gif or mp4 or blog or tel or mail

    def found_everything(self):
        if len(self.fbs) > 0 and len(self.tws) > 0:
            return True

    def processed(self):
        return len(self.processed_urls)

    def get_fbs(self):
        return self.fbs

    def get_tws(self):
        return self.tws