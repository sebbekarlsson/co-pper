from copper_client.scrapers.Scraper import Scraper


class PythonDocsScraper(Scraper):
    base_url = 'https://docs.python.org/{}/library/{}.html'
    python_version = '3'
    
    def scrape(self, keyword):
        url = self.base_url.format(self.python_version, keyword)
        pass
