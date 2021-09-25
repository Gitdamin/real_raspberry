# 혼자서도 괜찮아 :) :ok_hand:
### 스마트 도어벨  SMART DOORBELL 
___________
## :star: 구성도

### 기능 1 : 얼굴인식 및 분류 
<br/>

<img src="https://user-images.githubusercontent.com/86276347/130423489-becd515b-0f2e-42ff-b7de-ebae4c99256c.png" width="640px" height="380px" title="33" alt="33"></img><br/>
<br/>

### 기능 2 : 스토킹 대처 및 방지 - 수정
<br/>

<img src="https://user-images.githubusercontent.com/86276347/130436870-b67a5ade-9307-4578-8fae-cf75d17a2d56.png" width="710px" height="250px" title="33" alt="33"></img><br/>
_____________
## :star: 배경

* 코로나 19 확산으로 1인 가구의 배달 및 택배에 대한 수요 증가
* 외부인과의 비대면 접촉 상황 증가
* 마스크 착용이 의무화되면서 외부인 신원파악 어려움
* 1인 가구에 대한 스토킹 및 주거침입 범죄 증가 
* 성범죄자의 도주 사건 증가에 따른 여성들의 불안감 증가
____________________
## :star: 개선 방안

### 기능 1 : 얼굴인식 및 분류

- 라즈베리파이를 활용하여 사람의 눈을 인식하는 초인종 개발
- 초인종을 누르는 즉시 외부인을 인식하여 이미지 저장
- 모니터(인터폰)에 현재 문 앞 상황과 저장된 이미지 동시에 띄우기
- 사전 이미지 학습을 통해 새로 입력된 외부인의 이미지 분류
- 인터폰 기능 종료 후 사용자에게 외부인 이미지 및 신원 전송

#### :zap: 순서 및 흐름
<img src="https://user-images.githubusercontent.com/86276347/129696940-8cb7bb53-4e5c-493e-a9c2-b6673673f73d.jpg" width="500px" height="220px" title="33" alt="33"></img><br/>
- 외부인이 초인종을 누르면 카메라 + openCV 작동
- 카메라가 작동된 직후 임의로 영상 캡쳐 및 저장 (who.jpg)
- HaarCascade 방식을 통해 사람의 눈 인식 후 이미지 캡쳐 및 저장 (recognize.jpg)
- 인터폰에 현재 문 앞 상황 + 저장해 놓은 이미지 송출
  - 눈이 제대로 인식되지 않았을 경우, who.jpg 를 송출  
  > 'Captured Image'
  - 눈이 제대로 인식되었을 경우, recognize.jpg 를 송출 
  > 'Recognized Image'
- 일정 시간(10초) 이후 카메라 기능 종료 + 인터넷 로드 시작
- 사용자의 카카오 채널에 ‘초인종 누름’ 및 외부인 이미지 전송
  - 눈이 제대로 인식되지 않았을 경우, who.jpg 를 전송
  - 눈이 인식되었을 경우, recognize.jpg 를 전송 + 이미지 분류 시작
     - 새롭게 입력된 외부인 이미지와 이전 학습된 이미지를 비교 분석
     - trainer파일로부터 id, confidence 추출 및 사용자에게 전송
     - 이전에 미리 학습된 인물이 아닐 경우, 신원(id) = ‘unknown’

___________________
### 기능 2 : 스토킹 대처 및 방지

- 라즈베리파이를 활용하여 스토킹 및 주거침입 방지 초인종 개발
- 외부인의 접근이 일정 시간 이상 지속될 경우 영상 촬영 및 저장
- 초음파센서와 openCV 기능을 결합하여 수상한 움직임 감지
- 문 앞 상황에 대해 영상을 저장 후 사용자에게 전송

#### :zap: 순서 및 흐름
- 처음 코드를 작동시키면 맞은 편 벽과 문 사이의 거리를 측정 (기준값 지정)
- 초음파 센서를 통해 기준치보다(벽 사이 거리보다) -25cm 이내로 접근 시 count 증가 (변수 a)
- 변수값이 지정된 값 이상으로 증가 시 카메라 활성화
- openCV의 HaarCascade 방식을 이용해 full body / upper body / eyes 인식 
  - 인식이 안 될 경우, nodetected 변수 증가
    - nodetected가 1000 이상이 될 경우, 변수 a = 0 으로 초기화/ 다시 거리 측정
  - 인식에 성공 할 경우, detected 변수 증가
    - detected가 5이상이 될 경우, 영상 녹화 시작 (프레임 저장)
    - detected가 50이 넘어가면 인식 자동 종료, 영상 녹화 종료 및 저장
    - video.avi 파일을 video.mp4 파일로 변환
    - 사용자의 카카오 채널에 ‘움직임 감지’ + 저장된 영상 전송 

_____________
## :star: 적용 기술
 
#### :zap: 센서
<img src="https://user-images.githubusercontent.com/86276347/134758452-d990360f-46c4-4063-9329-5beaf7e00edd.jpg" width="435px" height="290px" title="33" alt="33"></img> <br/>
- 초음파 : 거리 측정을 통해 일정 거리 이내의 외부인 접근 확인
- LED : 카메라를 통한 이미지 촬영 과정에서 조명 역할 /정상 동작 확인용
- 스위치 : 초인종 입력 버튼

#### :zap: openCV – 사람의 눈, 몸, 상체 인식 
<img src="https://user-images.githubusercontent.com/86276347/130432439-f2465d01-ae3d-4b40-8217-d66e15a8dc0d.jpg" width="500px" height="180px" title="33" alt="33"></img> <br/>
- 초인종을 누르거나 문 앞에서 서성이는 경우 실행
- 영상 혹은 이미지를 greyscale로 변경하여 HaarCascade적용
  * 밝기의 변화를 토대로 각 신체 부위별 특징 추출
  * .xml 파일 내의 데이터와 greyscale 영상을 비교 분석하여 신체 인식
- 해당 신체 부위가 인식되면 네모박스로 표시
 
#### :zap: openCV – 이미지 삽입 
<img src="https://user-images.githubusercontent.com/86276347/134758418-2564c30a-06b7-4360-ad10-d173fbd9b685.JPG" width="250px" height="260px" title="33" alt="33"></img> 
<img src="https://user-images.githubusercontent.com/86276347/134760428-26871ac4-1cd6-4c75-b641-7ccae557857d.JPG" width="250px" height="260px" title="33" alt="33"></img> <br/>
- 주어진 이미지의 갯수가 한정되어 있을 경우 적용 
> ex. 공공데이터를 통해 제공받은 성범죄자의 정면 이미지 & 지인의 정면 이미지
- 코로나 19에 맞추어 색상별 마스크, 모양별 안경 이미지 삽입
- openCV의 정면 얼굴 인식(frontal face.xml)을 통해 얼굴의 랜드마크 추적
- 얼굴의 x, y ,w, h 값을 찾아내어 삽입 이미지가 들어갈 위치 조정
- 이후 추가로 정교한 위치 수정

#### :zap: openCV – 배열을 통한 밝기 변환
<img src="https://user-images.githubusercontent.com/86276347/134760364-789d7ba7-71ed-48e2-baec-b05373f6f895.JPG" width="250px" height="260px" title="33" alt="33"></img>
<img src="https://user-images.githubusercontent.com/86276347/134760366-4d41ffc0-2cba-4f61-a518-6d2eefe8a8f3.JPG" width="250px" height="260px" title="33" alt="33"></img> <br/>
- 주어진 이미지의 갯수가 한정되어 있을 경우 적용
- 이미지를 RGB 세 가지 색상에 대한 배열로 나타내어 값을 변화
- 기본 이미지를 기준으로 값을 더하여 밝게 변환
- 기본 이미지를 기준으로 값을 빼 어둡게 변환
- 기본 + 밝음 + 어두움 세 가지 버전으로 이미지 dataset 수집

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
## :star: 실제 구현
<img src="https://user-images.githubusercontent.com/86276347/134760283-e5253996-cc55-4af7-8368-450c7b625410.JPG" width="740px" height="300px" title="33" alt="33"></img> <br/>
<img src="https://user-images.githubusercontent.com/86276347/134760284-8de67a1c-b1c5-410c-89e3-a911178a9b5b.JPG" width="740px" height="300px" title="33" alt="33"></img> <br/>


______________
## :star: 특장점

* 인물 학습과정 중 한정된 자료에 이미지 추가 및 조명 변화를 주어 정확도 증가
* 눈을 중심으로 사람을 인식한 후 해당 인물별 공통점 및 특징 추출 
* 초인종을 누른 후 바로 떠나는 외부인에 대한 최대한의 정보 획득
* 미리 학습된 인물 간의 비교분석을 통해 외부인의 신원 및 정보 추출
* 접근성이 좋은 카카오톡 플랫폼을 도입하여 사용자의 편리함 증가
* 웹 자동화 시스템으로 알고리즘 간편화 및 속도 증가 & 사용자의 코드 수정 편리
* 상대적 부실한 환경을 가지는 1인 가구에서 사용하기 경제적 방안
_______________
## :star: 활용 분야

#### COVID-19상황에 따른 비대면 접촉 방식에 적용
- 모니터(인터폰)에 송출되는 이미지를 통해 빠르게 외부인 정보 확인
  * 외부인이 화면 앞에서 사라져도 저장된 이미지를 통해 정보 획득
  * 마스크를 착용한 상황에서도 적용 가능 (눈 인식을 통해) 
- 이미지 학습을 통해 얻은 신원(id)을 토대로 외부인 정확한 신원 파악
- 접근 알림과 저장된 이미지 전송을 통해 외부인 신원 가시화  

#### 혼자 살아가는 1인 가구 대상 범죄 예방
- 초인종을 누른 직후 자동 저장되는 이미지를 통해 벨튀 예방
  * 벨튀 : 벨을 누르고 도망치는 수법
- 사용자의 지인과 외부인 간의 차별점을 두어 범죄 인지 및 예방  
- 녹화된 영상을 스토킹 및 주거침입 증거물로 활용 
- 외출 시에도 알림을 통해 외부인 방문 및 접근 빠르게 인지
- 스토킹, 주거 침입, 성범죄 등에 대한 뻐른 대처 및 증거 수집 가능
__________
## :star: 사용 방법 

- openCV, 크롬 드라이버 설치
- https://github.com/opencv/opencv/tree/master/data/haarcascades
에 접속하여 필요한 ```.xml``` 파일 다운 (full & upper body, eyes)
- 사용자의 라즈베리파이에 ```face_detection``` 디렉토리 생성 후 해당 파일에 ```main``` code, ```.xml```파일 저장
- https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/
에 접속하여 개인 카카오 채널 생성
- ```main``` code의 ```kakao1, 2()```에서 개인 아이디, 비밀번호, 채팅방 주소 수정
```python
 def kakao1, 2():
    
    # 예시
    # kakao_setting
    id = '~'  #개인 아이디
    pw = '~'  #개인 비밀번호

    KaKaoURL = 'https://accounts.kakao.com/login/kakaoforbusiness?continue=https://center-pf.kakao.com/'
    ChatRoom = '~'  #개인 채팅방 주소
    options = webdriver.ChromeOptions()
    
```
- 마스크 및 안경 이미지를 깃허브의 ```face_detection```에서 다운받아 ```main``` code에 저장
- ```dataset_v1, 2``` 파일을 통해 학습시키고 싶은 인물 이미지 데이터 수집
> 직접 카메라 앞에서 촬영이 가능할 경우, v1 사용 (다양한 환경, 조명, 각도에서 촬영하는 것이 유리) <br/>
> 주어진 데이터가 한정적(사진 1장) 일 경우, v2 사용
- ```trainer``` 파일을 작동시켜 인물 별 특징 추출 및 학습
- 영상 전송 시 .mp4파일로 변환하기 위한 ```subprocess``` 라이브러리 설치
- ```main``` code내 default되어 있는 경로들을 자신의 파일에 맞는 경로로 수정  
