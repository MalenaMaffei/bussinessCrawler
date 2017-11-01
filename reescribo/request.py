import requests
import requests.exceptions

class Request:
    def getSource(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

