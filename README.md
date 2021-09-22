# 혼자서도 괜찮아 :) :ok_hand:
### 스마트 도어벨  SMART DOORBELL 
___________
## :star: 구성도

### 기능 1 : 얼굴인식 및 분류 
<br/>

<img src="https://user-images.githubusercontent.com/86276347/130423489-becd515b-0f2e-42ff-b7de-ebae4c99256c.png" width="640px" height="380px" title="33" alt="33"></img><br/>
<br/>

### 기능 2 : 스토킹 대처 및 방지
<br/>

<img src="https://user-images.githubusercontent.com/86276347/130436870-b67a5ade-9307-4578-8fae-cf75d17a2d56.png" width="710px" height="250px" title="33" alt="33"></img><br/>
_____________
## :star: 배경

* 코로나 19 확산으로 1인 가구의 배달 및 택배에 대한 수요 증가
* 외부인과의 비대면 접촉 상황 증가
* 마스크 착용이 의무화되면서 외부인 신원파악 어려움
* 1인 가구에 대한 스토킹 및 주거침입 범죄 증가
* 1인 가구를 대상으로 한 범죄 증가에 따른 여성들의 불안감 증가
____________________
## :star: 개선 방안

### 기능 1 : 얼굴인식 및 분류

- 라즈베리파이를 활용하여 사람의 눈을 인식하는 초인종 개발
- 초인종을 누르는 즉시 외부인을 인식하여 이미지 저장
- 모니터(인터폰)에 현재 문 앞 상황과 저장된 이미지 동시에 띄우기
- 사전 이미지 학습을 통해 신원을 아는 사람은 외부인에서 제외
- 인터폰 기능 종료 후 사용자에게 외부인 이미지 및 신원 전송

#### :zap: 순서 및 흐름
<img src="https://user-images.githubusercontent.com/86276347/129696940-8cb7bb53-4e5c-493e-a9c2-b6673673f73d.jpg" width="500px" height="220px" title="33" alt="33"></img><br/>
- 외부인이 초인종을 누르면 카메라 + openCV 작동
- 카메라가 작동된 직후 임의로 영상 캡쳐 및 저장 (who.jpg)
- HaarCascade 방식을 통해 사람의 눈 인식 후 이미지 캡쳐 및 저장 (recognize.jpg)
- 인터폰에 현재 문 앞 상황 + 저장해 놓은 이미지 송출
  - 눈이 제대로 인식되지 않았을 경우, who.jpg 를 송출
  - 눈이 제대로 인식되었을 경우, recognize.jpg 를 송출 
- 일정 시간(15초) 이후 카메라 기능 종료 + 인터넷 로드 시작
- 사용자의 카카오 채널에 ‘초인종 누름’ 및 외부인 이미지 전송
  - 눈이 제대로 인식되지 않았을 경우, who.jpg 를 전송
  - 눈이 인식되었을 경우, recognize.jpg 를 전송 + 이미지 분류 시작
     - 새롭게 입력된 외부인 이미지와 이전 학습된 이미지를 비교 분석
     - trainer파일로부터 id, confidence 추출 및 사용자에게 전송
     - 이전에 미리 학습된 인물이 아닐 경우, 신원(id) = ‘unknown’

#### :zap: 구현 예시
<img src="https://user-images.githubusercontent.com/86276347/130420364-23f13960-d4ef-4c07-9e03-7730d2ab301f.JPG" width="280px" height="188px" title="33" alt="33"></img> <br/>
그림 1) 눈 인식 성공 + 학습 안 된 인물 <br/>  
<img src="https://user-images.githubusercontent.com/86276347/130420371-0ad5531a-503c-423a-8332-91060dd6e17d.JPG" width="280px" height="188px" title="33" alt="33"></img> <br/>
그림 2) 눈 인식 성공 + 미리 학습된 인물 <br/>
<br/>


___________________
### 기능 2 : 스토킹 대처 및 방지

- 라즈베리파이를 활용하여 스토킹 및 주거침입 방지 초인종 개발
- 외부인의 접근이 일정 시간 이상 지속될 경우 영상 촬영 및 저장
- 실시간 영상 스트리밍 기능을 통해 문 앞 상황 확인 가능
- 사용자에게 짧은 영상 및 스트리밍 주소 전달

#### :zap: 순서 및 흐름
- 초음파 센서로 (초인종으로부터) 일정 거리 안에 접근한 외부인 감지
- 이후 카메라 촬영을 통해 사람이 존재하는지 확인
  - openCV의 HaarCascade 방식을 이용해 full body / upper body / eye 인식 
- 일정 시간 이상 외부인이 인식될 경우 video.avi 파일에 비디오 녹화 시작
- video.avi 파일을 video.mp4 파일로 변환
- 사용자의 카카오 채널에 ‘움직임 감지’ + 저장된 영상 전송 

#### :zap: 구현 예시
<img src="https://user-images.githubusercontent.com/86276347/130436879-a116f1e2-421c-4015-bf81-28842d33455a.jpg" width="280px" height="120px" title="33" alt="33"></img><br/>
그림 3) 움직임 감지 + 녹화 영상 전송
<br/>

_____________
## :star: 적용 기술
 
#### :zap: openCV – 사람의 눈, 몸, 상체 인식 
<img src="https://user-images.githubusercontent.com/86276347/130432439-f2465d01-ae3d-4b40-8217-d66e15a8dc0d.jpg" width="500px" height="180px" title="33" alt="33"></img> <br/>
- 초인종을 누르거나 문 앞에서 서성이는 경우 실행
- 영상 혹은 이미지를 greyscale로 변경하여 HaarCascade적용
  * 밝기의 변화를 토대로 각 신체 부위별 특징 추출
  * .xml 파일 내의 데이터와 greyscale 영상을 비교 분석하여 신체 인식
- 해당 신체 부위가 인식되면 네모박스로 표시

#### :zap: LBP (Local Binary Patterns) - 이미지 학습 
<img src="https://user-images.githubusercontent.com/86276347/130432354-4ee99c31-a6b6-4f3a-a4d2-e9635a274f5f.png" width="500px" height="140px" title="33" alt="33"></img> <br/>
- (마스크 착용 의무화) 눈 부분만 인식하여 분석하기 위해서 LBP 방식 고려 
- 학습하고 싶은 이미지를 HaarCascade 방식으로 눈 인식 후 저장
  * 다양한 구도, 환경, 조명에서 이미지를 저장하는 것이 중요
- greyscale로 변환된 해당 이미지들을 픽셀별 이진수로 다시 나타냄
- LBP 히스토그램을 기반으로 인물별 특징 추출 및 학습
- 이후 새롭게 입력된 이미지와 비교 분석하여 id, confidence 추출

#### :zap: selenium - 웹 자동화
- 웹 자동화 및 테스트를 위한 프레임워크
- 라즈베리파이 기기 자체에서 바로 인터넷 연결을 위해 적용
- 크롬 드라이버 로드 후 카카오 메인 페이지로 이동
- 코드에 입력된 정보를 토대로 자동 로그인 후 카카오 채널 접근 
- 사용자 채팅방을 로드하여 알림 메시지 및 필요한 정보 전달 

_____________
## :star: 특장점

* 외부인이 벨을 누르고 얼굴을 카메라 앞에 항상 대기하고 있지 않기 때문에 발생하는 신원파악 문제를 쉽게 해결
* 미리 학습된 인물 간의 비교를 통해 외부인의 정보 및 신원 빠르게 인식 가능
* 접근성이 좋은 카카오톡 플랫폼을 도입하여 사용자의 편리함 증가
* 웹 자동화 시스템으로 알고리즘 간편화 및 속도 증가
* 라즈베리파이 모니터를 인터폰으로 활용함으로써 효율성 증가
_______________
## :star: 활용 분야

#### COVID-19상황에 따른 비대면 접촉 방식에 적용
- 모니터(인터폰)에 송출되는 이미지를 통해 빠르게 외부인 정보 확인
  * 외부인이 화면 앞에서 사라져도 저장된 이미지를 통해 정보 획득
  * 마스크를 착용한 상황에서도 적용 가능 
- 이미지 학습을 통해 얻은 신원(id)을 토대로 외부인 정체 신속 파악
- 접근 알림과 저장된 이미지 전송을 통해 외부인 신원 가시화  

#### 혼자 살아가는 1인 가구 대상 범죄 예방
- 초인종을 누른 직후 자동 저장되는 이미지를 통해 벨튀 예방
  * 벨튀 : 벨을 누르고 도망치는 수법
- 사용자의 지인과 외부인 간의 차별점을 두어 범죄 인지 및 예방  
- 녹화된 영상을 스토킹 및 주거침입 증거물로 활용 
- 외출 시에도 외부인 방문 및 접근 인지 가능
__________
## :star: 사용 방법 - 수정예정

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
5. *dataset* 파일을 통해 학습시키고 싶은 인물 이미지 촬영
>다양한 환경, 조명, 각도에서 촬영하는 것이 유리
6. *trainer* 파일을 작동시켜 인물 별 특징 추출 및 학습
7. 
8. 1+2_main.py 파일을 실행
