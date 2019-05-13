from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def open_new_window(dr, url):
    js = "window.open('{url}')".format(url=url)
    print(js)
    dr.execute_script(js)
    pass


options = Options()
# options.binary_location = '/path/to/chrome.exe'

prefs = {
    "profile.managed_default_content_settings.images": 1,
    "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
    "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,

}

options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(executable_path='D:\chromedriver_win32-74.3729\chromedriver.exe',
                          chrome_options=options)
# # test
# driver.get('https://www.baidu.com/')
# open_new_window(driver, "https://www.baidu.com/")
# # test end


driver.get('http://www2.xtdx.superchutou.com:8002/Login')
account = driver.find_element_by_id('cardnumber')
account.send_keys('51382219890829678X')
password = driver.find_element_by_id('password')
password.send_keys('xt123456')
imgCode = driver.find_element_by_id('passimgCode')

imgCodeStr = input("输入验证码：")
imgCode.send_keys(imgCodeStr)
button = driver.find_element_by_id('Button1')
button.click()
time.sleep(5)
classOne = driver.find_element_by_xpath('//*[@id="containerafter_new_has"]/tr[1]/td[3]/a')
time.sleep(1)
classOne.click()
time.sleep(5)
print("hello")
lessions = driver.find_elements_by_xpath(
    '//*[@id="chapters"]/div[@class="chapter-item"]/ul[@class="video"]/li/a')
for l in lessions:
    print(l.get_attribute("href"))
open_new_window(driver, lessions[0].get_attribute("href"))
