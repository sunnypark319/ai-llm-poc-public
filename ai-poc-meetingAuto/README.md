# 🎙️ 실시간 녹음 + 녹취록 생성 애플리케이션

이 애플리케이션은 실시간 음성 녹음, 자동 음성 인식, 그리고 AI를 활용한 녹취록 및 요약 생성을 제공합니다.

## ✨ 주요 기능

- **실시간 음성 녹음**: 고품질 WAV 형식으로 음성 녹음
- **자동 음성 인식**: OpenAI Whisper를 활용한 정확한 한국어 음성 인식
- **화자 분리**: 간단한 화자 분리 기능
- **녹취록 생성**: 타임스탬프가 포함된 구조화된 녹취록
- **AI 요약**: GPT를 활용한 회의 요약 자동 생성
- **파일 다운로드**: 녹음 파일, 녹취록, 요약 다운로드 지원

## 📁 프로젝트 구조

```
├── main.py                    # 메인 애플리케이션
├── config.py                  # 설정 및 상수
├── session_manager.py         # 세션 상태 관리
├── audio_recorder.py          # 녹음 기능
├── transcription_service.py   # 음성 인식 및 처리
├── recording_controller.py    # 녹음 제어 로직
├── ui_components.py          # UI 컴포넌트
├── requirements.txt          # 의존성 파일
├── .env.example             # 환경변수 예시
└── README.md               # 프로젝트 설명
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env.example`을 복사하여 `.env` 파일을 생성하고, OpenAI API 키를 설정합니다:

```bash
cp .env.example .env
# .env 파일을 편집하여 OPENAI_API_KEY 설정
```

### 3. 애플리케이션 실행

```bash
streamlit run main.py
```

## 📋 사용 방법

1. **"🎤 녹음 시작"** 버튼 클릭
2. **5-10초간 말하기** (회의 내용 등)
3. **"⏹️ 녹음 종료"** 버튼 클릭
4. **자동으로 음성 인식 및 녹취록/요약 생성**
5. **결과 확인 및 다운로드**

## 🏗️ 아키텍처 특징

### 모듈화된 설계
- **관심사 분리**: 각 모듈이 명확한 책임을 가짐
- **재사용성**: 독립적인 컴포넌트로 설계
- **확장성**: 새로운 기능 추가가 용이

### 주요 컴포넌트

#### 1. **Config (`config.py`)**
- 애플리케이션 설정 및 상수 관리
- 환경변수 로딩
- 중앙집중식 설정 관리

#### 2. **SessionManager (`session_manager.py`)**
- Streamlit 세션 상태 관리
- 타입 안전한 상태 접근
- 상태 초기화 및 정리

#### 3. **PerfectRecorder (`audio_recorder.py`)**
- 멀티스레드 기반 오디오 녹음
- WAV 파일 생성 및 관리
- 에러 처리 및 리소스 정리

  
<img width="5012" height="1393" alt="그림1" src="https://github.com/user-attachments/assets/3ff52c64-4cc2-43dd-a30f-ac0c98c909bc" />

#### 4. **TranscriptionService (`transcription_service.py`)**
- OpenAI API 통합
- 음성 인식 및 화자 분리
- 녹취록 및 요약 생성

#### 5. **RecordingController (`recording_controller.py`)**
- 녹음 프로세스 전체 제어
- 상태 관리 및 에러 처리
- 자동 처리 파이프라인

#### 6. **UIComponents (`ui_components.py`)**
- 재사용 가능한 UI 컴포넌트
- 상태에 따른 동적 UI
- 사용자 경험 최적화

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Audio Processing**: PyAudio, Wave
- **AI Services**: OpenAI (Whisper, GPT-3.5)
- **Language**: Python 3.8+

## 🚀 개선 사항 (기존 모놀리스 대비)

### 1. **코드 구조 개선**
- 1000줄+ 단일 파일 → 8개 모듈로 분리
- 명확한 책임 분리
- 재사용 가능한 컴포넌트

### 2. **유지보수성 향상**
- 독립적인 테스트 가능
- 기능별 수정 영향 최소화
- 새로운 기능 추가 용이

### 3. **확장성 개선**
- 새로운 음성 인식 서비스 추가 용이
- UI 컴포넌트 재사용 가능
- 설정 변경 중앙집중화

### 4. **에러 처리 강화**
- 각 레이어별 에러 처리
- 사용자 친화적 오류 메시지
- 안정적인 상태 관리

## 🔮 향후 개선 계획

- [ ] 실시간 화자 분리 고도화
- [ ] 다양한 음성 인식 엔진 지원
- [ ] 클라우드 저장소 연동
- [ ] 회의 템플릿 기능
- [ ] 다국어 지원 확장
