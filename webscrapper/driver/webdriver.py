from selenium import webdriver as driver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By

from selenium.webdriver.remote.webelement import WebElement

#This is an all purpose Selenium webdriver manager with most popular functions

class WebDriver():

    def __init__(self) -> None:
        self.driver = driver.Edge(service = EdgeService(EdgeChromiumDriverManager().install()))

    def connect(self, url):
        self.driver.get(url)

    def find_by_id(self, id):
        return self.driver.find_element(By.ID, id)

    def find_by_class(self, classname):
        return self.driver.find_element(By.CLASS_NAME, classname)

    def select_all_by_class(self, classname):
        return self.driver.find_elements(By.CLASS_NAME, classname)

    def click(self, element:WebElement):
        element.click()

    def get_attr(self, attr_name, element:WebElement):
        return element.get_attribute(attr_name)