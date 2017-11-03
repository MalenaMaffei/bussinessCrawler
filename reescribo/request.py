import requests
import requests.exceptions


class Request:
    def getSource(self, url):

        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 403:
                session = requests.Session()
                response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                return response.text
            else:
                raise


