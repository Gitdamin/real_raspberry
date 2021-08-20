## Test web crawling ##
# Reference

from selenium import webdriver
from datetime import datetime
from PIL import Image
import time
import configparser
import urllib


ID = ''
pw = ''

KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
options = webdriver.ChromeOptions()

driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)

driver.get(KaKaoURL)
time.sleep(3)


driver.find_element_by_id('loginEmail').send_keys(ID)
driver.find_element_by_id('loginPw').send_keys(pw)
driver.find_element_by_id('countryCodeRequired').find_element_by_xpath("//button[@type='submit']").click()
time.sleep(3)

iframes = driver.find_elements_by_tag_name('iframe')
print('iframe=%d', len(iframes))

