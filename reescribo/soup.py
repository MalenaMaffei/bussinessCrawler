from bs4 import BeautifulSoup

class Soup:
    def __init__(self, html):
        self.parser = "html.parser"
        self.html = BeautifulSoup(html, self.parser)

    def getSoup(self):
        return self.html

    def getLinks(self):
        links = []
        for anchor in self.html.find_all("a"):
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            if "contact" in link:
                links.insert(0, link)
            else:
                links.append(link)
        return links