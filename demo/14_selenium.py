import time
from lib2to3.pgen2 import driver

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("")

driver.switch_to()  # frame 和 iframe 使用下面的切换方式，其他 frame 按元素对待


driver.find_element_by_id("form_email").send_keys("")
driver.find_element_by_id("form_password").send_keys("")
time.sleep(3)

driver.find_element_by_class_name("bn-submit").click()

cookies = {i["name"]: i["value"] for i in driver.get_cookies()}
# driver.delete_cookie("CookieName")
# driver.delete_all_cookies()
print(cookies)

time.sleep(3)

driver.quit()
