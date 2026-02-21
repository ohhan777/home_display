# Home Display - 라즈베리파이 스마트 디지털 시계

SmartThings 동작 센서, 날씨 데이터, 미세먼지 정보가 통합된 라즈베리파이 스마트 디지털 시계입니다.

## 주요 기능

- 🕐 다양한 시계 디스플레이 스타일 (Original, Neo, Rain, Graphic)
- 🏠 SmartThings 동작 센서 연동으로 자동 화면 켜기/끄기
- 🌤️ 기상청 실시간 날씨 정보
- 💨 미세먼지(PM10, PM2.5) 모니터링
- 🌅 일출/일몰 시간 기반 낮/밤 테마 자동 전환
- 📊 디버깅을 위한 상세 로깅
- 🔒 환경 변수를 통한 안전한 인증 정보 관리

## 필요 사항

- Raspberry Pi (3/4 모델 권장)
- Python 3.7+
- HDMI로 연결된 디스플레이
- 인터넷 연결
- SmartThings 계정 및 동작 센서

## 설치 방법

### 1. 프로젝트 클론
```bash
git clone https://github.com/ohhan777/home_display.git
cd home_display
```

### 2. 의존성 설치
```bash
pip3 install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
cp .env.example .env
nano .env
```

필수 설정 항목:
- SMARTTHINGS_TOKEN: SmartThings Personal Access Token
- KMA_API_KEY: 기상청 API 키
- WEATHER_GRID_NX, WEATHER_GRID_NY: 위치의 격자 좌표
- AIR_QUALITY_STATION: 가장 가까운 미세먼지 측정소 이름

### 4. 실행
```bash
python3 home_display.py
```

## API 키 발급 방법

### SmartThings Personal Access Token
1. https://account.smartthings.com/tokens 접속
2. 디바이스 읽기 권한으로 새 토큰 생성

### 기상청 API 키
1. https://www.data.go.kr/ 접속
2. 회원가입 후 기상청 단기예보 API 신청

## 문제 해결

로그 파일 확인:
```bash
tail -f /home/pi/home_display/home_display.log
```

## 라이선스

MIT License
