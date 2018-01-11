from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time

user_name = ''
user_pwd = ''

setting_url = 'https://github.com/%s/settings'
delete_text = '//*[@id="%s-description"]/form/p/input'
delete_url = '//*[@id="%s-description"]/form/button'

driver = webdriver.Chrome()
driver.get('https://github.com/login')
login_field = driver.find_element_by_id('login_field')
password = driver.find_element_by_id('password')
commit = driver.find_element_by_name('commit')

login_field.clear()
login_field.send_keys(user_name)
password.clear()
password.send_keys(user_pwd)
commit.send_keys('go', Keys.ENTER)

driver.get('https://github.com/settings/repositories')
user_target = driver.find_element_by_name('octolytics-actor-login').get_attribute('content')
print('即将删除用GitHub[%s]下所有的仓库'%user_target)
listgroup = driver.find_element_by_class_name('listgroup')

delete_repository_list = []
for target_a in listgroup.find_elements_by_tag_name('a'):
    if target_a.text.startswith(user_target + '/'):
        delete_repository_list.append((target_a.text, setting_url%(target_a.text),))
print(delete_repository_list)
for delete_repository_index in delete_repository_list:
    driver.get(delete_repository_index[1])
    delete_button = driver.find_element_by_xpath('//*[@id="options_bucket"]/div[10]/ul/li[4]/button')
    hash_id = delete_button.get_attribute('data-box-overlay-id')
    print(delete_text%(hash_id))
    delete_button.send_keys('delete', Keys.ENTER)
    delete_text_c = driver.find_element_by_xpath(delete_text%(hash_id))
    delete_text_c.clear()
    delete_text_c.send_keys(delete_repository_index[0])
    delete_url_c = driver.find_element_by_xpath(delete_url%(hash_id))
    delete_url_c.send_keys('delete', Keys.ENTER)

    
