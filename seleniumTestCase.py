
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class First_Test(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.facebook.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_Facebook_On(self):
        driver = self.driver
        driver.get("http://facebook.com")
        self.assertIn("Facebook", driver.title)
        driver.find_element_by_id("u_0_m").click()
        driver.find_element_by_id("u_0_m").click()
        driver.find_element_by_name("Testtesttest").click()
        driver.find_element_by_xpath("(//button[@value='1'])[7]").click()
        driver.find_element_by_xpath("(//button[@value='1'])[7]").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    if __name__ == "__main__":
        unittest.main()
