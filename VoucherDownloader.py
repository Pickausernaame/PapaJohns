from selenium import webdriver
from selenium.webdriver.firefox.options import Options as Firefox_Options
from selenium.webdriver.common.keys import Keys

from random import randrange
from time import sleep


# Данный класс
# 1) Создает почтовый ящик
# 2) Забивает данные в форму на сайте папы джонса
# 3) Забирает промокод из входящего сообщения
class VoucherDownloader:
    def __init__(self):
        self._clients = []
        self._numbers = []
        self._proxy = []
        self._emails = []
        self.user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        self.papa_url = "https://www.papajohns.ru/30off"
        self.mail_url = "https://temp-mail.org/ru/"


        self._profile = webdriver.FirefoxProfile()
        self._options = Firefox_Options()
        self._options.add_argument('-headless')
        self._profile.set_preference('intl.accept_languages', 'ru')
       # self._profile.set_preference("general.useragent.override", self.user_agent)
        self._profile.set_preference('permissions.default.image', 2)

        self._driver = webdriver.Firefox(firefox_profile=self._profile, firefox_options=self._options)
        self._driver.set_window_size(720, 1280)



    def _get_data(self):
        self._clients.append("Михайлов Стас Михайлович")
        self._numbers.append("9253831" + str(randrange(10)) + str(randrange(10)) + str(randrange(10)))
        self._get_email()

    def _get_email(self):
        self._driver.get(self.mail_url)
        print("Your email ", self._driver.find_element_by_xpath("//*[@id=\"mail\"]").get_attribute("value"))
        self._emails.append(self._driver.find_element_by_xpath("//*[@id=\"mail\"]").get_attribute("value"))


    def _send_data(self):
        self._driver.get(self.papa_url)
        sleep(2)
        self._driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div/div/form/div/fieldset[1]/a").click()

        self._driver.find_element_by_xpath("//*[@id=\"name\"]").send_keys(self._clients[0])
        self._driver.find_element_by_xpath("//*[@id=\"phone\"]").send_keys(self._numbers[0])
        self._driver.find_element_by_xpath("//*[@id=\"email\"]").send_keys(self._emails[0])

        self._driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div/div/form/div/fieldset[2]/div[5]/div/label/span").click()
        self._driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div/div/form/div/fieldset[2]/div[6]/div/label/span[1]").click()

        self._driver.find_element_by_xpath("//*[@id=\"btn-submit\"]").click()

    def _get_voucher(self):
        self._driver.get(self.mail_url)
        sleep(10)
        self._driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/div[4]/ul/li[2]/div[1]/a/span[1]").click()
        print("Your voucher ", self._driver.find_element_by_xpath("/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[2]/div[3]/table[1]/tbody/tr[9]/td/table/tbody/tr/td/div/span[2]/span/strong").text)


# Публичный метод get() возвращает промокод(string)
    def get(self):
        self._get_data()
        self._send_data()
        sleep(2)
        return str(self._get_voucher())
