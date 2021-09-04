# ObsCure_DB-Video
## 소개
##### CCTV 시스템 동작 및 동작시 발생하는 영상과 스크린샷의 관리를 위해 설계된 클래스 개발입니다.  
##### opencv-python을 이용하여 카메라별 스트림과 영상 저장, 스크린샷 기능을 포함하는 클래스를 제작하였고,  
##### 스트림 시 저장되는 영상과 스크린샷을 sqlite3 를 이용하여 DB파일에 영상, 스크린샷 정보 및 저장 경로를 관리합니다.  
## 주요기능
### 1. Stream 클래스
> ##### PC에 연결된 웹캠을 스트리밍해주는 클래스입니다.  
  - 객체 생성 시 카메라 번호를 입력으로 하여 해당 번호의 카메라 영상을 출력해줍니다.  
  - 00시 기준으로 촬영된 영상을 저장하고 상황 발생 시 스크린샷을 촬영할 수 있도록 구현하였습니다.  
  - [Main](https://github.com/SSU-DC-DCWZ/ObsCure_Main)에서는 실제로 사용되지는 않고 [Model](https://github.com/SSU-DC-DCWZ/ObsCure_Main/tree/main/Detect/falldetect.py) 클래스 구현 시 구조를 참고하였습니다.  
### 2. DBvideo 클래스
> ##### 저장된 영상을 관리하는 클래스입니다.   
  - 영상 저장 시 카메라 번호, 일자, 경로를 입력으로 하여 레코드를 생성하고 저장기한을 관리하는 클래스 입니다.  
  - 카메라 번호, 일자를 입력으로 하여 입력받은 정보에 해당하는 영상의 경로를 찾아주는 역할도 합니다.  
  - [Stream](https://github.com/SSU-DC-DCWZ/ObsCure_DB-Video/tree/main/Stream) 클래스에서 영상 저장 시 바로 video.db에 레코드가 생성되도록 합니다.  
  - [Main](https://github.com/SSU-DC-DCWZ/ObsCure_Main)에서는 [Model](https://github.com/SSU-DC-DCWZ/ObsCure_Main/tree/main/Detect/falldetect.py) 클래스에서 영상 저장 시 사용되고 [WindowClass](https://github.com/SSU-DC-DCWZ/ObsCure_Main/blob/main/ui/play_ui.py) 클래스에서 저장된 영상의 경로 출력 시 사용됩니다.  
### 3. DBlog 클래스
> ##### 상황 발생 시 스크린샷의 관리를 위한 클래스입니다. 
  - 관측하려는 상황이 발생하였을 때 카메라번호, 일자, 경로, 상황을 입력으로 하여 레코드를 생성하고 저장기한을 관리하는 클래스 입니다.  
  - 카메라 번호, 상황번호, 일자를 입력으로 하여 입력받은 정보에 해당하는 스크린샷의 경로를 찾아주는 역할도 합니다.  
  - 현재는 [Main](https://github.com/SSU-DC-DCWZ/ObsCure_Main)에서 사용되지 않으나 추후에 출력한 알림에 해당하는 상황의 스크린샷을 보여주는 용도로 사용할 예정입니다.  
## Requirement
```
Python==3.8.10  
opencv-python==4.2.0.34  
sqlite3==3.31.1  
```
## 개발 환경
#### PyCharm 2021.1.13 (Professional Edition) @11.0.11
#### Ubuntu 20.04.3 LTS (GNU/Linux 5.11.0-25-generic x86_64)
## 기여자
#### **이찬서**(Lfollow-CS) : DB,Stream 관리 및 개별 프로젝트 통합
## 라이선스
#### 이 프로젝트는 [GNU General Public License v3.0](https://github.com/SSU-DC-DCWZ/ObsCure_DB-Video/blob/main/LICENSE)을 사용합니다.
