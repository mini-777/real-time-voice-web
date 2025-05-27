# 🎤 실시간 음성 인식 앱 (Whisper + Flask + React)

OpenAI Whisper를 사용한 실시간 음성 인식 웹 애플리케이션입니다. Flask 백엔드와 React 프론트엔드로 구성되어 있으며, Vercel에서 서버리스 함수로 배포됩니다.

## ✨ 주요 기능

- 🎙️ **실시간 음성 녹음**: 브라우저의 MediaRecorder API 사용
- 🧠 **AI 음성 인식**: OpenAI Whisper 모델을 통한 정확한 음성-텍스트 변환
- 🌐 **다국어 지원**: Whisper의 다국어 인식 기능
- 📱 **반응형 디자인**: 모바일과 데스크톱 모두 지원
- ⚡ **실시간 처리**: 빠른 음성 처리 및 결과 표시

## 🛠️ 기술 스택

### 백엔드

- **Flask 3.0.3**: 웹 프레임워크
- **OpenAI Whisper**: 음성 인식 AI 모델
- **PyTorch**: 딥러닝 프레임워크
- **Flask-CORS**: CORS 지원

### 프론트엔드

- **React 18**: UI 라이브러리
- **Vanilla CSS**: 스타일링
- **MediaRecorder API**: 음성 녹음

### 배포

- **Vercel**: 서버리스 배포 플랫폼
- **Python Runtime**: 서버리스 함수

## 🚀 로컬 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 개발 서버 실행

```bash
# Vercel CLI 설치 (처음 한 번만)
npm i -g vercel

# 개발 서버 시작
vercel dev
```

애플리케이션이 `http://localhost:3000`에서 실행됩니다.

## 📋 API 엔드포인트

### `POST /transcribe`

음성 데이터를 받아 텍스트로 변환합니다.

**요청 본문:**

```json
{
  "audio": "base64_encoded_audio_data"
}
```

**응답:**

```json
{
  "success": true,
  "text": "인식된 텍스트",
  "language": "ko"
}
```

### `GET /health`

서버 상태를 확인합니다.

**응답:**

```json
{
  "status": "healthy",
  "model": "whisper-base"
}
```

## 🎯 사용 방법

1. 웹 페이지에 접속
2. 마이크 권한 허용
3. 🎤 녹음 버튼 클릭하여 음성 녹음 시작
4. ⏹️ 중지 버튼 클릭하여 녹음 종료
5. AI가 음성을 텍스트로 변환하여 결과 표시

## 🔧 설정

### Whisper 모델 변경

`api/index.py`에서 모델을 변경할 수 있습니다:

```python
# 더 정확하지만 느린 모델
model = whisper.load_model("large")

# 더 빠르지만 덜 정확한 모델
model = whisper.load_model("tiny")
```

사용 가능한 모델: `tiny`, `base`, `small`, `medium`, `large`

## 📦 배포

### Vercel 배포

```bash
vercel --prod
```

또는 GitHub 연동을 통한 자동 배포를 설정할 수 있습니다.

## 🔒 보안 고려사항

- 음성 데이터는 임시 파일로만 저장되며 처리 후 즉시 삭제됩니다
- CORS가 활성화되어 있어 브라우저에서 안전하게 접근 가능합니다
- 마이크 권한은 사용자가 명시적으로 허용해야 합니다

## 🐛 문제 해결

### 마이크 접근 오류

- HTTPS 환경에서만 마이크 접근이 가능합니다
- 브라우저 설정에서 마이크 권한을 확인하세요

### 음성 인식 오류

- 조용한 환경에서 명확하게 발음하세요
- 인터넷 연결 상태를 확인하세요

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
