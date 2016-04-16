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
        code_description = soup.find(class_='dc-title').text

        if code is None:
            return None
        
        if php_type == 'function':
            code_type = code.find(class_='type').text
            code_name = code.find(class_='methodname').text
            params = code.find_all(class_='methodparam')
            params_parameters = []

            for param in params:
                try:
                    parameter_type = param.find(class_='type').text
                    parameter = param.find(class_='parameter').text
                except AttributeError:
                    continue

                params_parameters.append({'type': parameter_type, 'parameter': parameter})

            func = CodeFunction(
                        return_type=code_type,
                        name=code_name,
                        parameters=params_parameters,
                        description=code_description
                    )

        return func
