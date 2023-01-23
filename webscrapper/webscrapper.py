from bs4 import BeautifulSoup
from .driver.webdriver import WebDriver

class WebScrapper():

    def __init__(self) -> None:
        self.webdriver = WebDriver()
        self.data = None

    def start(self):
        self.get_data()

    def get_data(self):
        self.webdriver.connect("https://www.camara.leg.br/deputados/quem-sao/resultado?legislatura=56")
        ids = self.collect_ids()
        pass

    def collect_ids(self):
        ids = list()
        while True:
            page_deputies = self.webdriver.select_all_by_class('lista-resultados__txt')
            for deputy in page_deputies:
                soup = BeautifulSoup(self.webdriver.get_attr('outerHTML', deputy), 'html.parser')
                link = soup.find('a')['href']
                id = link.split('/')[-1]
                ids.append(id)
            next_page = self.webdriver.find_by_class('pagination-list__nav--next')
            if 'disabled' not in self.webdriver.get_attr('class', next_page):
                self.webdriver.click(next_page)
            else:
                break
        return ids