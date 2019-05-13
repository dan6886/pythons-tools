from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.binary_location = '/path/to/chrome.exe'
driver = webdriver.Chrome(executable_path='D:\chromedriver_win32-74.3729\chromedriver.exe',
                          chrome_options=options)
driver.get('http://www.baidu.com/')
# driver.quit();
text = driver.find_element_by_id('kw')
text.clear()
text.send_keys('吴玮霖')
button = driver.find_element_by_id('su')
# 接着还是通过find_element_by_id（）方法找到提按钮，
button.submit()
# driver.get('http://10.10.1.66:81/zentao/user-login.html')
# account = driver.find_element_by_id('account')
# account.send_keys('cx.dan1')
# password = driver.find_element_by_name('password')
# password.send_keys('123456')
# button = driver.find_element_by_id('submit')
# button.submit()
