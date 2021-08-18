# 혼자서도 괜찮아 :) :ok_hand:
### 스마트 도어벨  SMART DOORBELL 
___________
## :small_orange_diamond: 소개
* 라즈베리파이를 이용하여 벨을 누른 사람이 카메라 화면에 잡히지 않아도 벨을 누른 순간에 저장된 이미지와 함께 모니터에 송출되어 그 사람의 정보를 얻을 수 있다.
* 수상한 외부인이 문 앞에서 주기적으로 서성이는 움직임을 포착하여 알림 및 영상 전송을 통해 1인 가구 대상 범죄 예방이 가능하다. 
<br/>

<img src="https://user-images.githubusercontent.com/86276347/129713360-dbe360da-44ed-40d6-b7fb-a79cb70e0e7d.jpg" width="640px" height="180px" title="33" alt="33"></img><br/>
_____________
## :small_orange_diamond: 배경
* 일반적으로 초인종을 누른 외부인은 카메라 앞에서 가만히 대기하고 있지 않음
* 집 내부에서 외부인의 신원 및 정보를 제대로 파악하는 것이 어려움
* 사용자가 집 외부에 있을 때도 외부인의 정보를 받아보고 싶은 경우
* 알 수 없는 외부인이 집 밖에서 주기적으로 서성이고 있는 경우 
* 스토킹이 의심되는 경우 이를 빠르게 해결 또는 대처하고 싶음
* 스토킹이나 주거침입에 관련한 증거를 수집하고 싶음
____________________
##  :small_orange_diamond: 기능 1 
### :small_blue_diamond: 외부인 인식 + 학습된 이미지와 비교 분석 + 결과 알림전송
<img src="https://user-images.githubusercontent.com/86276347/129696940-8cb7bb53-4e5c-493e-a9c2-b6673673f73d.jpg" width="610px" height="260px" title="33" alt="33"></img><br/>
>그림 1) 
<br/>

* 외부인이 초인종을 누르고 빠르게 사라져도 이전에 미리 저장한 이미지를 함께 띄워줌으로서 사용자에게 충분한 정보 제공
* 벨이 눌린 후 신속하게 모니터를 바로 보지 못했거나, 집 내부에 인터폰이 없어 외부인을 인식하기 어려웠던 상황에 적용 
* 사용자가 집 외부에 있어도 카카오 알림을 통해 외부인의 접근 인지 가능
>접근성과 편리성이 높아 사용자가 이용하기 적합
* 미리 학습된 인물이 아닌 수상한 외부인의 방문일 경우, 사용자는 빠르게 인식 후 대처 가능
<br/>

####  :small_red_triangle_down: 순서 및 흐름

1. 외부인이 초인종을 누르면 화면 앞 이미지 캡쳐 <br/>
2. 이후 ```openCV``` 를 통해 사람의 눈 인식
>마스크 착용 의무화에 의한 얼굴 전체 랜드마크 인식 불가
3. 인식된 이미지 5장 임의로 캡쳐 및 저장
4. 모니터(인터폰)에 현재 문 앞 영상과 저장한 이미지 동시에 송출
>만약 외부인의 눈이 인식되지 않아 5장의 이미지를 저장하지 못했다면 *1.* 의 이미지를 대신 송출
6. 임의로 지정한 시간(10초)이 지나면 얼굴 인식 자동 종료
7. 웹크롤링을 통해 라즈베리파이 자체에서 인터넷(크롬) 연결 + 카카오 채널 접속
8. '초인종을 눌렀습니다' 및 저장된 사진 전송
>만약 외부인의 눈이 인식되지 않아 5장의 이미지를 저장하지 못했다면 *1.* 의 이미지를 대신 전송 
9. 만약 눈이 인식되었다면 해당 이미지를 통해 미리 학습된 이미지와 비교 분석하여 사용자에게 신원(id)에 관한 메시지 전달<br/>
<br/>

<img src="https://user-images.githubusercontent.com/86276347/129705728-45ff55df-a777-4cc8-8db5-faf86117c84a.JPG" width="280px" height="200px" title="33" alt="33"></img>
<img src="https://user-images.githubusercontent.com/86276347/129705749-64015f00-6b56-42b8-9eee-dea485a10667.JPG" width="280px" height="200px" title="33" alt="33"></img><br/>
>그림 2) <br/>
<br/>

####  :small_red_triangle_down: 이미지 학습 및 분석

<img src="https://user-images.githubusercontent.com/86276347/129713368-254d8095-fcb6-4109-a908-b84d85abb86c.jpg" width="320px" height="250px" title="33" alt="33"></img><br/>

* 이미 신원 및 정보를 파악하고 있는 외부인과 처음보는 외부인 간의 차별점을 두기 위해 얼굴 학습 및 분석 기능 추가
* 수상한 외부인 접근에 대해 더 빠르게 대처 가능
* 사용자는 외부인의 신원을 빠르게 인지 가능
* 다양한 환경에서 이미지를 학습시킬 수록 정확도가 올라감
<br/>

1. 사람의 눈을 ```Haar Cascade```방식으로 인식한 뒤 이미지 저장
2. 다양한 각도, 조명, 환경에서 촬영한 이미지들을 ```LBP(Local binary patterns)``` 기반으로 특징 추출 (학습)
3. 이후 새롭게 저장된 이미지를 학습된 이미지와 비교 분석하여 신원 및 정보를 파악함
>속도가 느려지는 단점

<br/>


## :small_orange_diamond: 기능 2
###  :small_blue_diamond: 스토킹 대처 및 방지
<br/>

* 초인종으로부터 일정 거리 안에 일정 시간 이상 동안 움직임이 발생하면 이를 초음파 센서가 감지하여 1차 확인
* 이후 카메라로 촬영을 시작하여 외부인의 실루엣 인식을 통해 2차 확인
>```openCV```를 이용해 ```full body``` 혹은 ```upper body``` 인식 
* 지속해서 사람의 움직임이 인식될 경우 영상 녹화 시작
* 웹크롤링 방식을 통해 카카오 채널에 자동 접속하여 수상한 외부인 접근 알림 및 실시간 스트리밍 주소와 저장된 영상 전달  
>라즈베리파이 기기 자체에서 자동화된 소프트웨어를 통해 인터넷 및 카카오 채널 접근
* 영상자료를 스토킹이나 주거침입의 증거로 활용 가능
 _____________
 ## :small_orange_diamond: 특장점
* 외부인이 벨을 누르고 얼굴을 카메라 앞에 항상 대기하고 있지 않기 때문에 발생하는 신원파악 문제를 쉽게 해결 가능
* 카카오 플랫폼을 도입하여 사용자의 접근성 증가
* 라즈베리파이 모니터를 인터폰으로 바로 사용할 수 있기 때문에 효율성 증가
* 기존 도어벨을 활용하여 새로운 기능을 추가했기 때문에 실현 가능성이 높음
_______________
## :small_orange_diamond: 활용 분야
* 혼자 사는 여성을 대상으로 한 범죄를 예방하는 데 효과적
* 스토킹 관련 증거 수집에 사용 가능
* COVID-19 상황으로 인한 비대면 접촉 방식에 사용하기 적합
__________
## :small_orange_diamond: 사용 방법
1. https://github.com/opencv/opencv/tree/master/data/haarcascades
에 접속하여 필요한 ```.xml``` 파일 다운
2. *main code*가 있는 위치에 함께 저장
3. https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/
에 접속하여 개인 카카오 채널 생성
4. *main code*의 ```kakao()```에서 개인 아이디, 비밀번호, 채팅방 주소 수정
```python
 def kakao():
    
    #kakao_setting
    id = '~'  #개인 아이디
    pw = '~'  #개인 비밀번호

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = '~'  #개인 채팅방 주소
    options = webdriver.ChromeOptions()
    
```
>사용자의 정보로 변경하여 입력
