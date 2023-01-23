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
        self.data = self.collect_basic_data()
        pass

    def collect_basic_data(self):
        data = list()
        while True:
            page_deputies = self.webdriver.select_all_by_class('lista-resultados__txt')
            for deputy_info in page_deputies:
                deputy = dict()
                soup = BeautifulSoup(self.webdriver.get_attr('outerHTML', deputy_info), 'html.parser')
                self.collect_id(deputy, soup)
                self.collect_basic_info(deputy, soup)
                
                data.append(deputy)

            next_page = self.webdriver.find_by_class('pagination-list__nav--next')
            if 'disabled' not in self.webdriver.get_attr('class', next_page):
                self.webdriver.click(next_page)
            else:
                break
        return

    def collect_id(self, deputy, soup):
        link = soup.find('a')['href']
        id = link.split('/')[-1]
        deputy['id'] = id

    def collect_basic_info(self, deputy, soup):
        info = soup.find('a').get_text(strip=True)
        party_state = info[info.find("(")+1:info.find(")")]
        deputy['name'] = info[0:info.find(" (")]
        deputy['party'], deputy['state'] = party_state.split('-')
        deputy['status'] = soup.find('span').get_text(strip=True)