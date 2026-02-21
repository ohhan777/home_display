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

예제 환경 파일을 복사하고 본인의 인증 정보로 편집하세요:

```bash
cp .env.example .env
nano .env
```

필수 설정 항목:
- `SMARTTHINGS_TOKEN`: SmartThings Personal Access Token
- `KMA_API_KEY`: 기상청 API 키 (인코딩된 값)
- `WEATHER_GRID_NX`, `WEATHER_GRID_NY`: 위치의 격자 좌표
- `AIR_QUALITY_STATION`: 가장 가까운 미세먼지 측정소 이름

### 4. 수동 실행 (테스트용)

```bash
python3 home_display.py
```

### 5. 부팅 시 자동 실행 설정 (권장)

systemd 서비스를 사용하여 부팅 시 자동으로 실행되도록 설정:

```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/home-display.service
```

다음 내용을 추가:

```ini
[Unit]
Description=Home Display Smart Clock
After=graphical.target
Wants=graphical.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/home_display
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/home/pi/home_display/start_display.sh
Restart=always
RestartSec=10

[Install]
WantedBy=graphical.target
```

서비스 활성화 및 시작:

```bash
sudo systemctl daemon-reload
sudo systemctl enable home-display.service
sudo systemctl start home-display.service
```

서비스 상태 확인:

```bash
sudo systemctl status home-display.service
```

## 서비스 관리 명령어

```bash
# 서비스 상태 확인
sudo systemctl status home-display.service

# 서비스 시작
sudo systemctl start home-display.service

# 서비스 중지
sudo systemctl stop home-display.service

# 서비스 재시작
sudo systemctl restart home-display.service

# 자동 시작 비활성화
sudo systemctl disable home-display.service
```

## 설정

### 디스플레이 스케줄

`.env` 파일에서 화면이 켜질 수 있는 시간대를 설정할 수 있습니다:

- 평일 아침: 오전 6시 - 오전 10시
- 평일 저녁: 오후 4시 - 자정
- 주말: 오전 6시 - 자정

### 동작 센서 타임아웃

동작이 감지되지 않을 때 화면이 꺼지는 시간:
- 근무 시간: 900초 (15분)
- 기타 시간: 600초 (10분)

## 파일 구조

```
home_display/
├── home_display.py          # 메인 진입점
├── start_display.sh         # 시작 스크립트 (DPMS 비활성화 포함)
├── gui_main.py              # GUI 및 디스플레이 제어
├── global_vars.py           # 스레드 안전 공유 변수
├── .env                     # 환경 변수 (git 제외)
├── .env.example             # 환경 변수 템플릿
├── requirements.txt         # Python 의존성
├── README.md                # 프로젝트 문서
├── gui_clocks/
│   ├── clocks.py           # 시계 디스플레이 구현
│   └── *.png               # 배경 이미지
└── info/
    ├── smartthings.py      # SmartThings 연동
    ├── weather.py          # 날씨 데이터
    ├── weather_forecast.py # 날씨 예보
    ├── air_dust.py         # 미세먼지 데이터
    └── sun_moon.py         # 일출/일몰 계산
```

## 문제 해결

### 디스플레이가 꺼진 후 켜지지 않을 때

DPMS (Display Power Management)가 방해할 수 있습니다. `start_display.sh` 스크립트가 자동으로 비활성화하지만, 수동으로도 가능합니다:

```bash
export DISPLAY=:0
xset -dpms
xset s off
xset s noblank
```

### 날씨 데이터가 업데이트되지 않을 때

1. `.env` 파일의 `KMA_API_KEY` 확인
2. 격자 좌표(`WEATHER_GRID_NX`, `WEATHER_GRID_NY`) 확인
3. 로그에서 API 오류 확인

### SmartThings 연결 문제

1. `.env` 파일의 `SMARTTHINGS_TOKEN` 확인
2. SmartThings 앱에서 센서 이름이 "Motion Sensor"인지 확인
3. 네트워크 연결 상태 확인

## 로그 확인

### 애플리케이션 로그
```bash
tail -f /home/pi/home_display/home_display.log
```

### systemd 서비스 로그
```bash
sudo journalctl -u home-display.service -f
```

## API 키 발급 방법

### SmartThings Personal Access Token

1. https://account.smartthings.com/tokens 접속
2. 디바이스 읽기 권한으로 새 토큰 생성
3. `.env` 파일에 복사

### 기상청 API 키

1. https://www.data.go.kr/ 접속
2. 회원가입 후 기상청 단기예보 API 신청
3. 발급받은 인코딩 키를 `.env` 파일에 복사

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트는 언제든지 환영합니다!
