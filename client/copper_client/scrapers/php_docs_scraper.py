from copper_client.scrapers.Scraper import Scraper
from copper_client.parts.code_function import CodeFunction
import requests
from bs4 import BeautifulSoup


class PHPDocsScraper(Scraper):
    base_url = 'http://php.net/manual/en/{}.{}.php'

    
    def scrape(self, keyword, php_type='function'):
        url = self.base_url.format(php_type, keyword)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        code = soup.find(class_='methodsynopsis dc-description')

        if code is None:
            return None
        
        if php_type == 'function':
            code_type = code.find(class_='type').text
            code_name = code.find(class_='methodname').text
            params = code.find_all(class_='methodparam')
            params_parameters = []

            for param in params:
                parameter_type = param.find(class_='type').text
                parameter = param.find(class_='parameter').text

                params_parameters.append({'type': parameter_type, 'parameter': parameter})

            func = CodeFunction(
                        type=code_type,
                        name=code_name,
                        parameters=params_parameters
                    )

        return func.__dict__
