import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url='https://lk.mrgkchr.ru/unauth/statements.php'
user_agent = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) '
              'Gecko/20100101 Firefox/50.0')
driver=webdriver.Chrome()
headers={
    'referer': f'{url}',
    'User-Agent': user_agent
}

try:
    driver.get(url=url)
    input_ls = driver.find_element_by_name('ls')
    input_phone = driver.find_element_by_name('phone')
    input_statements = driver.find_element_by_name('statements')
    input_ls.clear()
    input_ls.send_keys('8601003824')
    input_statements.clear()
    input_statements.send_keys('00000')
    input_phone.clear()
    input_phone.send_keys('9280301600')
    input_phone.send_keys(Keys.ENTER)

except Exception as ex:
    print(ex)
finally:
    time.sleep(10)
    driver.close()
    driver.quit()