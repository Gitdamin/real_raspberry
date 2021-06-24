#크롬으로 접속 & 네이버에 '영등포구 양평동3가' 의 날씨 검색 후 캡쳐
#카카오 로그인 & 저장 된 사진을 카카오 챗봇으로 글자와 함께 전송

from selenium import webdriver
from datetime import datetime
from PIL import Image
import time
import configparser
import urllib

myCity = '영등포구 양평동3가'
naver_input = urllib.parse.quote(myCity + ' 날씨')
WeatherURL = 'https://search.naver.com/search.naver?ie=utf8&query='+ naver_input
AlertTime = 8 #매일 날씨를 알려줄 시간 (오전 여덟시)

while True:
    
    if (datetime.now().hour > AlertTime) :  
 
        #알리기
        #Config = configparser.ConfigParser()
 
        #카카오 아이디, 비밀번호 불러옴
        #Config.read('info.conf')
        #Config = Config['MAIN']
        
        #driver = webdriver.Chrome('chromedriver')
        #driver.get('https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/')

        id = ''
        pw = ''

        KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
        ChatRoom = 'https://center-pf.kakao.com/_xfxcRGs/chats/4814011526591515'
        options = webdriver.ChromeOptions()
 
 
        #user-agent 변경
        options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.187")
 
        #크롬 드라이버 로드
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)
        driver.implicitly_wait(3)
 
 
        #날씨 페이지 로드
        driver.get(WeatherURL)
 
 
        #스크린샷 저장
        screenshot_name = "/home/pi/Documents/kakao_robot/weather.png"
        driver.save_screenshot(screenshot_name)
 
        #스크린샷 불러오기
        img = Image.open('/home/pi/Documents/kakao_robot/weather.png')
        cutted_img = img.crop((39,210,622,677))
        cutted_img.save('/home/pi/Documents/kakao_robot/weather.png')
 
 
        #카카오 메인 페이지 로드
        driver.get(KaKaoURL)
        time.sleep(3)
        
        #iframes = driver.find_elements_by_tag_name('iframe')
        #driver.switch_to.frame(len(iframes))
        #html = driver.page_source
        #soup = BeautifulSoup(html, 'html.parser')
        #soup.find()
        #soup.find_all()
        #driver.switch_to.default_content()
 
        #로그인
        #driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
        # time.sleep(1)
        #driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")
        # time.sleep(1)
        #driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
        
        
        driver.find_element_by_id('id_email_2').send_keys(id)
        driver.find_element_by_id('id_password_3').send_keys(pw)
        driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[8]/button[1]').click()
        #driver.find_element_by_id('move_to_qr').find_element_by_xpath("//button[@type='button']").click()
        
        #driver.find_element_by_id('move_to_qr').find_element_by_xpath("//*[@id="login-form"]/fieldset/div[8]/button[1]").click()
        #//*[@id="login-form"]/fieldset/div[8]/button[1]
        time.sleep(3)
        
        #채팅방 로드
        driver.get(ChatRoom)
        time.sleep(3)
        
       
 
        #글 작성
        driver.find_element_by_id('chatWrite').send_keys('라즈베리로봇 테스트 메시지입니다')  #메시지 작성
        driver.find_element_by_xpath("//div[@class='box_tf']//button[@type='button']").click()  #전송버튼
        driver.find_element_by_xpath("//input[@class='custom uploadInput']").send_keys('/home/pi/Documents/kakao_robot/weather.png') #날씨 사진 전송
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='wrap_inp']//button[@type='button']").click()  #전송버튼
   
        driver.quit()
        time.sleep(60)
        break
