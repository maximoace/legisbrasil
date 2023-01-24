from .driver.webdriver import WebDriver
from database.database import Database

from bs4 import BeautifulSoup

class WebScrapper():

    def __init__(self) -> None:
        self.webdriver = WebDriver()
        self.data = None

    def start(self):
        if not Database().exists():
            self.get_data()
            self.save_data()

    def get_data(self):
        self.webdriver.start()
        attempt = 0
        while attempt < 3:
            try:
                self.webdriver.connect("https://www.camara.leg.br/deputados/quem-sao/resultado?legislatura=56")
                self.collect_basic_data()
                break
            except:
                attempt +=1
                print(f"Failed {attempt} attempt at gathering general basic data")
        self.collect_detailed_data()
        print("Dados dos deputados obtidos com sucesso.")
        self.webdriver.finish()

    def save_data(self):
        Database().save(self.data)

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
        self.data = data

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

    def collect_detailed_data(self):
        base_url = "https://www.camara.leg.br/deputados"

        for deputy in self.data:
            self.collect_summary_page(deputy, base_url)
            self.collect_biography(deputy, base_url)

    def collect_summary_page(self, deputy:dict, base_url):
        attempt = 0
        while attempt < 3:
            try:
                indexed_url = f"{base_url}/{deputy['id']}"
                self.webdriver.connect(indexed_url)

                info_section = self.webdriver.find_by_class("informacoes-deputado")
                soup = BeautifulSoup(self.webdriver.get_attr("outerHTML", info_section), 'html.parser')
                self.collect_summary_info(deputy, soup)
                break
            except:
                attempt += 1
                print(f"Failed {attempt} attempt(s) at obtaining ID:{deputy['id']} summary")

    def collect_summary_info(self, deputy:dict, soup):
        info_list = soup.find_all('li')

        for info in info_list:
            text = info.get_text()
            if 'Nome' in text:
                deputy["fullname"] = text[text.find(': ')+2:]
            elif 'E-mail' in text:
                deputy["email"] = text[text.find(': ')+2:]
            elif 'Telefone' in text:
                deputy["phone"] = text[text.find(': ')+2:]
            elif 'Endereço' in text:
                deputy["address"] = text[text.find(': ')+2:].replace('\n', '').replace('   ', '')
            elif 'Nascimento' in text:
                deputy["birthday"] = text[text.find(': ')+2:]
            elif 'Naturalidade' in text:
                deputy["pob"] = text[text.find(':')+1:].replace('\n','').replace('  ','')
        
    def collect_biography(self, deputy:dict, base_url):
        attempt = 0
        while attempt < 3:
            try:
                biography_url = f"{base_url}/{deputy['id']}/biografia"
                self.webdriver.connect(biography_url)

                info_section = self.webdriver.find_by_class("informacoes-deputado")
                soup = BeautifulSoup(self.webdriver.get_attr("outerHTML", info_section), 'html.parser')
                self.collect_biography_info(deputy, soup)

                info_section = self.webdriver.find_by_class("biografia-detalhes-deputado")
                soup = BeautifulSoup(self.webdriver.get_attr("outerHTML", info_section), 'html.parser')
                self.collect_biography_extra(deputy, soup)
                break
            except:
                attempt += 1
                print(f"Failed {attempt} attempt(s) at obtaining ID:{deputy['id']} biography")


    def collect_biography_info(self, deputy:dict, soup):
        info_list = soup.find_all('li')
        for info in info_list:
            text = info.get_text()
            if 'Profissões' in text:
                deputy['jobs'] = text[text.find(':')+2:]
            if 'Escolaridade' in text:
                deputy['scholarity'] = text[text.find(':')+2:]

    def collect_biography_extra(self, deputy:dict, soup):
        info_name_list = soup.find_all('strong')
        for name in info_name_list:
            text = name.get_text()
            if 'Mandatos' in text:
                deputy['mandate'] = name.next_sibling.next_sibling.get_text()[1:]