# -*- coding: utf8 -*-
# __author__ = "Vadim Toptunov"
import ConfigParser
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import unittest

'''
The script takes values from a config, opens Chrome browser, logins to mail.ru,
sets 'To:', 'CC:', 'BCC:' fields and the letter itself, then sends the letter and
checks the letter is successfully sent. If itb is - the information is written down the log file,
if it is not not - the negative information is written down.
Then the script opens a new tab, goes to mail.yandex.ru and does the same as before.
Then both tabs are closed.

To run the script you should have:

1. Python 2.7 (run the script with it!);
2. Installed Selenium Webdriver;
3. Installed Chromedriver for Python;
4. The Chromedriver should be written it the PATH of your computer;
5. 'To', 'CC' and 'BCC' fields opened in mail.ru's letter form;
6. A config to run the script.
'''

class MailAndYandexTest(unittest.TestCase):
    def setUp(self):
        config = raw_input("Please, cpecify a config file (Ex.: C:\user\directory\File.cfg): ")
        time.sleep(20)
        log_directory = raw_input("Please, specify a directory for a log file: ")
        time.sleep(20)
        self.driver = webdriver.Chrome() # Switch on Chrome
        self.driver.implicitly_wait(30)
        self.conf = ConfigParser.RawConfigParser() # Switch on config parser
        conf = self.conf
        conf.read(config) # Config is here!
        self.login = conf.get("credentials", "login") # Read login from the config
        self.password = conf.get("credentials", "password") # Read password from the config
        self.to = conf.get("credentials", "to") # Read to, cc and bcc from config
        self.cc = conf.get("credentials", "cc")
        self.bcc = conf.get("credentials", "bcc")
        self.message = conf.get("credentials", "message") # Read message from config
        self.directory = log_directory # Directory for the log
        self.name = "app_log" # name of the log
        self.filename = self.directory + self.name + ".txt" # log file

    def test_Mail_Ru_and_Yandex_Ru(self):
        driver = self.driver # Run Selenium WebDriver
        login = self.login # Set variables
        password = self.password
        to = self.to
        cc = self.cc
        bcc = self.bcc
        message = self.message
        filename = self.filename
        driver.get('https://www.mail.ru/') # Go to Mail.ru
        login_box = driver.find_element_by_id("mailbox__login")
        # Find login box and password box to insert login and password
        password_box = driver.find_element_by_id("mailbox__password")
        # Check if the page is ok
        self.assertEqual(u"Mail.Ru: почта, поиск в интернете, новости, игры", driver.title)
        login_box.send_keys(login) # Login
        password_box.send_keys(password) # Password
        auth_button = driver.find_element_by_id("mailbox__auth__button") # Sign In
        auth_button.click()
        src = driver.page_source
        text_found = re.search(login, src) # Check login present on the page like login@mail.ru
        wr_letter = driver.find_element_by_xpath("//span[@class='b-toolbar__btn__text b-toolbar__btn__text_pad']")
        wr_letter.click() # Click on 'Написать письмо'
        WebDriverWait(driver, 5)
        # Insert To, CC and BCC lines
        el = driver.find_element_by_css_selector("textarea.js-input.compose__labels__input")
        el.click()
        el.send_keys(to)
        letter_cc = driver.find_element_by_xpath("//div[@id='compose__header__content']/div[3]/div[2]/div/textarea[2]")
        letter_cc.send_keys(cc)
        letter_bcc = driver.find_element_by_xpath("//div[@id='compose__header__content']/div[4]/div[2]/div/textarea[2]")
        letter_bcc.send_keys(bcc)
        # Insert message into the letter body
        letter_body = driver.find_element_by_css_selector('iframe[id*="compose"]')
        letter_body.click()
        letter_body.send_keys(message)
        # Send message
        send = driver.find_element_by_xpath("//span[@class='b-toolbar__btn__text']")
        send.click()
        # Check if the letter is successfully sent and write down the log
        try:
            self.assertEqual(u"Ваше письмо отправлено. Перейти во Входящие",
                             driver.find_element_by_css_selector("div.message-sent__title").text)
            with open(filename, "w") as app_log:
                app_log.writelines("Resource: mail.ru \n")
                app_log.writelines("Outbox: + \n")
                app_log.writelines("Inbox: \n")
            app_log.close()

        except AssertionError as e:
            with open(filename, "w") as app_log:
                app_log.writelines("Resource: mail.ru \n")
                app_log.writelines("Outbox: - \n")
                app_log.writelines("Inbox: \n")
            app_log.close()
            print e
        WebDriverWait(driver, 10)
        # Open a new tab with mail.yandex.ru
        newtab = driver.execute_script("window.open('https://mail.yandex.ru/','_blank');")
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        # switch windows
        driver.switch_to_window(driver.window_handles[1])
        # wait to make sure the new window is loaded
        WebDriverWait(driver, 10).until(lambda d: d.title != "")
        #driver.switch_to.window
        WebDriverWait(driver, 10)
        # Make sure the page is successfully loaded
        self.assertEqual(u"Яндекс.Почта — бесплатная электронная почта", driver.title)
        # Find login and password boxes and type login and password into them
        login_box = driver.find_element_by_xpath("//input[@name='login']")
        login_box.click()
        login_box.send_keys(login)
        password_box = driver.find_element_by_xpath("//input[@name='passwd']")
        password_box.click()
        password_box.send_keys(password)
        # Sign In
        submit = driver.find_element_by_xpath("//button[@type='submit']")
        submit.click()
        WebDriverWait(driver, 10)
        # Find element "Compose" and click it
        driver.find_element_by_css_selector("img.b-ico.b-ico_compose").click()
        # Find To, CC, BCC and message and fill the boxes
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[3]/td[2]/div[2]/div/div/input").click()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[3]/td[2]/div[2]/div/div/input").clear()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[3]/td[2]/div[2]/div/div/input").send_keys(to)
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[3]/td[2]/div/span[2]").click()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[4]/td[2]/div/div/div/input").click()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[4]/td[2]/div/div/div/input").clear()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[4]/td[2]/div/div/div/input").send_keys(cc)
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[3]/td[2]/div/span[3]").click()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[5]/td[2]/div/div/div/input").click()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[5]/td[2]/div/div/div/input").clear()
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr[5]/td[2]/div/div/div/input").send_keys(bcc)
        driver.find_element_by_xpath("//input[contains(@data-class-suggest,'s mail-compose-suggest-wrapper')]")

        text = driver.find_element_by_css_selector('iframe[id*="compose"]')
        text.click()
        text.send_keys(message)
        # Click "Send message" button
        driver.find_element_by_xpath(
            "//div[@id='js-page']/div/div[5]/div/div[3]/div/div[3]/div/div/div/div[2]/div/div/form/table/tbody/tr/td/span/span/button").click()

        WebDriverWait(driver, 10)
        # Check the letter is successfully sent and the log result is written into the log
        try:
            self.assertEqual(u"Письмо успешно отправлено.", driver.find_element_by_css_selector("div.b-done-title").text)
            with open(filename, "a") as app_log:
                app_log.writelines("Resource: mail.yandex.ru \n")
                app_log.writelines("Outbox: + \n")
                app_log.writelines("Inbox: \n")
            app_log.close()
        except AssertionError as e:
            with open(filename, "a") as app_log:
                app_log.writelines("Resource: mail.yandex.ru \n")
                app_log.writelines("Outbox: - \n")
                app_log.writelines("Inbox: \n")
            app_log.close()
            print e

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()