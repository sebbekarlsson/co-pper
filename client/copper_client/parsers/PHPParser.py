from copper_client.parsers.Parser import Parser
from copper_client.scrapers.php_docs_scraper import PHPDocsScraper
import re
import os


class PHPParser(Parser):
    language = 'php'


    def clean(self, text):
        text = text.replace('_', '-')
        text = text.split('(')[0]

        return text


    def info(self, docs, line):
        inf = '''
        <article>
            <h3>{line}</h3>
            <p>{name}({args}) - {type}</p>
            <p>{desc}</p>
        </article>
        '''.format(
                line=line,
                name=docs.name,
                type=docs.return_type,
                args=['{}|{},'.format(par['type'], par['parameter']) for par in docs.parameters],
                desc=docs.description
                )

        return inf


    def parse(self, file):
        if self.language == 'php':
            self.scraper = PHPDocsScraper()

        if not os.path.isfile(file):
            print('Could not find file')
            quit()

        with open(file, 'r+') as ifile:
            ifile_input = ifile.read()
            lines = ifile_input.split('\n')
            docs_ = []

            with open('{}.html'.format(file), 'w+') as ofile:
                ofile.write('<!DOCTYPE HTML>\n<html>\n<body>')
                for i, line in enumerate(lines):
                    if '(' and ')' in line:
                        funcs = re.finditer("[a-zA-Z-0-9_]+\([^\)]*\)(\.[^\)]*\))?", line)
                        for func in funcs:
                            funcx = func.group(0)
                            func_name = self.clean(funcx)
                            docs = self.scraper.scrape(func_name)
                            if docs is None:
                                continue
                            
                            if not docs in docs_:
                                docs_.append(docs)
                                print(self.info(docs, i))
                                ofile.write(self.info(docs, i))


                ofile.write('\n</body>\n</html>')
                ofile.close()


            with open('{}.latest'.format(file), 'w+') as lfile:
                lfile.write(ifile_input)
                lfile.close()

            ifile.close()
