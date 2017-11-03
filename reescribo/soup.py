from bs4 import BeautifulSoup, SoupStrainer

class Soup:
    def __init__(self, html):
        self.parser = "html.parser"
        # self.links = BeautifulSoup(html, self.parser)
        self.aTags = BeautifulSoup(html, parseOnlyThese=SoupStrainer('a'))

    def getSoup(self):
        return self.html

    def getLinks(self):
        links = []

        # for anchor in self.html.find_all("a"):
        #     link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        #     if "contact" in link or "contact" in anchor.text:
        #         links.insert(0, link)
        #     else:
        #         links.append(link)
        # return links

        for aTag in self.aTags:
            if aTag.has_attr('href'):
                link = aTag['href']
                if "contact" in link or "contact" in aTag.text:
                    links.insert(0, link)
                else:
                    links.append(link)

        return links